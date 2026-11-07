"""PocketPilot AI engine.

Uses Groq as the primary provider and Gemini as a fallback.
Only the financial summary supplied by the app is sent to the AI provider;
raw transaction rows and API keys should never be placed in the prompt.
"""

from __future__ import annotations

import json
import os
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"
DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"
REQUEST_TIMEOUT_SECONDS = 35


class AIEngineError(Exception):
    """Raised when no configured AI provider can answer the request."""


def _get_secret(name: str) -> str | None:
    """Read a key from environment variables first, then Streamlit secrets."""
    value = os.getenv(name)
    if value:
        return value.strip()

    try:
        import streamlit as st

        value = st.secrets.get(name)
        if value:
            return str(value).strip()
    except Exception:
        # Streamlit secrets may not exist during local tests or deployment setup.
        pass

    return None


def configured_providers() -> list[str]:
    """Return configured providers in fallback order."""
    providers = []
    if _get_secret("GROQ_API_KEY"):
        providers.append("Groq")
    if _get_secret("GEMINI_API_KEY"):
        providers.append("Gemini")
    return providers


def _build_system_prompt() -> str:
    return (
        "You are PocketPilot, a friendly financial wellness coach for young adults in India. "
        "Answer in clear, simple language. Use INR (₹) for money. "
        "Use only the supplied financial summary for personal financial facts; never invent "
        "balances, transactions, budgets, dates, or calculations. If information is missing, "
        "say so and ask one useful follow-up. Give practical, realistic, non-judgmental steps. "
        "Do not request bank passwords, OTPs, card numbers, or other sensitive credentials. "
        "You are an educational assistant, not a SEBI-registered investment adviser; do not "
        "recommend specific securities or promise returns. Keep the answer concise and make "
        "clear that projections are estimates."
    )


def _post_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            response_text = response.read().decode("utf-8")
            return json.loads(response_text)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise AIEngineError(f"Provider returned HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError) as exc:
        raise AIEngineError(f"Could not connect to the AI provider: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise AIEngineError("The AI provider returned an unreadable response.") from exc


def _ask_groq(question: str, financial_context: Mapping[str, Any]) -> str:
    api_key = _get_secret("GROQ_API_KEY")
    if not api_key:
        raise AIEngineError("GROQ_API_KEY is not configured.")

    model = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL)
    user_message = (
        f"User question:\n{question.strip()}\n\n"
        "Verified financial summary (JSON):\n"
        f"{json.dumps(dict(financial_context), ensure_ascii=False, default=str)}"
    )
    result = _post_json(
        GROQ_API_URL,
        {
            "model": model,
            "messages": [
                {"role": "system", "content": _build_system_prompt()},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.4,
            "max_tokens": 700,
        },
        {"Authorization": f"Bearer {api_key}"},
    )

    try:
        answer = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AIEngineError("Groq returned an unexpected response format.") from exc

    if not isinstance(answer, str) or not answer.strip():
        raise AIEngineError("Groq returned an empty answer.")
    return answer.strip()


def _ask_gemini(question: str, financial_context: Mapping[str, Any]) -> str:
    api_key = _get_secret("GEMINI_API_KEY")
    if not api_key:
        raise AIEngineError("GEMINI_API_KEY is not configured.")

    model = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    url = GEMINI_API_URL.format(model=model)
    user_message = (
        f"{_build_system_prompt()}\n\n"
        f"User question:\n{question.strip()}\n\n"
        "Verified financial summary (JSON):\n"
        f"{json.dumps(dict(financial_context), ensure_ascii=False, default=str)}"
    )
    result = _post_json(
        url,
        {
            "contents": [{"parts": [{"text": user_message}]}],
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 700},
        },
        {"x-goog-api-key": api_key},
    )

    try:
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AIEngineError("Gemini returned an unexpected response format.") from exc

    if not isinstance(answer, str) or not answer.strip():
        raise AIEngineError("Gemini returned an empty answer.")
    return answer.strip()


def ask_financial_coach(
    question: str,
    financial_context: Mapping[str, Any],
) -> dict[str, str]:
    """Answer a question using Groq first and Gemini as a fallback.

    Args:
        question: The user's question about their finances.
        financial_context: Aggregated, verified figures prepared by app.py.
            Pass category totals and budget/forecast summaries, not raw rows.

    Returns:
        A dictionary with ``answer`` and ``provider`` keys.

    Raises:
        ValueError: If the question or context is empty/invalid.
        AIEngineError: If no configured provider can answer.
    """
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Please enter a question for PocketPilot.")
    if not isinstance(financial_context, Mapping) or not financial_context:
        raise ValueError("Financial context is missing. Please load transaction data first.")

    providers = []
    if _get_secret("GROQ_API_KEY"):
        providers.append(("Groq", _ask_groq))
    if _get_secret("GEMINI_API_KEY"):
        providers.append(("Gemini", _ask_gemini))

    if not providers:
        raise AIEngineError(
            "No AI API key found. Add GROQ_API_KEY or GEMINI_API_KEY to your local "
            "environment or Streamlit secrets."
        )

    errors = []
    for provider_name, provider_function in providers:
        try:
            answer = provider_function(question, financial_context)
            return {"answer": answer, "provider": provider_name}
        except AIEngineError as exc:
            errors.append(f"{provider_name}: {exc}")

    raise AIEngineError("All configured AI providers failed. " + " | ".join(errors))
