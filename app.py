from __future__ import annotations

from datetime import date, timedelta
import calendar

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ai_engine import AIEngineError, ask_financial_coach, configured_providers

# Consistent chart palette for the futuristic PocketPilot identity.
px.defaults.color_discrete_sequence = ["#9B72FF", "#45DDF2", "#35D6A0", "#FF9A62", "#668BFF", "#D47CFF"]


# ============================================================
# PocketPilot — AI-powered financial wellness for young Indians
# ============================================================
st.set_page_config(
    page_title="PocketPilot | Money Wellness",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- PocketPilot dark-only tech theme ----------
THEME = {
    "bg": "#080B18", "surface": "#11172B", "surface_alt": "#171F38",
    "text": "#F4F6FF", "muted": "#9AA6C4", "border": "#252E50",
    "sidebar": "#0B1022", "sidebar_text": "#F4F6FF", "metric": "#F4F6FF",
    "grid": "#273052", "hero_text": "#FFFFFF",
}

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root {{
        --pp-bg: {THEME['bg']}; --pp-surface: {THEME['surface']};
        --pp-surface-alt: {THEME['surface_alt']}; --pp-text: {THEME['text']};
        --pp-muted: {THEME['muted']}; --pp-border: {THEME['border']};
        --pp-sidebar: {THEME['sidebar']}; --pp-sidebar-text: {THEME['sidebar_text']};
        --pp-purple: #9B72FF; --pp-cyan: #45DDF2; --pp-green: #35D6A0; --pp-red: #FF647C;
    }}
    html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        background: radial-gradient(ellipse at 72% -12%, rgba(105,69,220,.16), transparent 38%),
                    radial-gradient(ellipse at 5% 45%, rgba(30,143,190,.07), transparent 32%), var(--pp-bg) !important;
        color: var(--pp-text) !important;
    }}
    [data-testid="stSidebar"] {{ background: linear-gradient(180deg,#0D1328 0%,#090E1D 100%) !important; border-right:1px solid var(--pp-border); }}
    [data-testid="stSidebar"] * {{ color:var(--pp-sidebar-text); }}
    [data-testid="stSidebar"] .stCaption {{ color:var(--pp-muted) !important; }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color:var(--pp-sidebar-text); }}
    .block-container {{ padding-top:1.45rem; padding-bottom:3rem; max-width:1540px; }}
    h1,h2,h3,h4,h5,h6 {{ font-family:'Manrope',sans-serif !important; color:var(--pp-text) !important; letter-spacing:-.035em; }}
    h1 {{ letter-spacing:-.055em; }}
    p,li,label,[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li {{ color:var(--pp-text); }}
    [data-testid="stCaptionContainer"] p,.small-note {{ color:var(--pp-muted) !important; }}
    [data-testid="stSidebar"] h2 {{ font-weight:800 !important; letter-spacing:-.06em; background:linear-gradient(90deg,#FFF 10%,#BBA7FF 58%,#54DFF0 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
    [data-testid="stSidebar"] div[data-testid="stRadio"] > label {{ display:none; }}
    [data-testid="stSidebar"] div[role="radiogroup"] {{ gap:7px; }}
    [data-testid="stSidebar"] div[role="radiogroup"] label {{ background:transparent; border:1px solid transparent; border-radius:12px; padding:9px 11px; transition:all .18s ease; }}
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {{ background:rgba(155,114,255,.10); border-color:rgba(155,114,255,.22); }}
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{ background:linear-gradient(100deg,rgba(133,83,255,.28),rgba(69,221,242,.08)); border:1px solid rgba(155,114,255,.52); box-shadow:0 0 22px rgba(126,83,255,.15),inset 3px 0 #A27CFF; }}
    div[data-testid="stMetric"],.pp-card {{ background:linear-gradient(145deg,rgba(23,31,57,.96),rgba(15,21,41,.98)) !important; border:1px solid var(--pp-border) !important; border-radius:19px; color:var(--pp-text) !important; box-shadow:0 10px 28px rgba(0,0,0,.18); }}
    div[data-testid="stMetric"] {{ padding:18px 20px; transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease; }}
    div[data-testid="stMetric"]:hover,.pp-card:hover {{ border-color:rgba(155,114,255,.55) !important; box-shadow:0 12px 32px rgba(80,52,180,.14); transform:translateY(-2px); }}
    div[data-testid="stMetricLabel"],div[data-testid="stMetricLabel"] * {{ color:var(--pp-muted) !important; -webkit-text-fill-color:var(--pp-muted) !important; font-weight:700 !important; letter-spacing:.035em; }}
    div[data-testid="stMetricValue"],div[data-testid="stMetricValue"] * {{ color:var(--pp-text) !important; -webkit-text-fill-color:var(--pp-text) !important; font-weight:800 !important; font-family:'Manrope',sans-serif; }}
    div[data-testid="stMetricDelta"] {{ font-size:.78rem; }}
    .pp-hero {{ background:radial-gradient(circle at 82% 15%,rgba(69,221,242,.20),transparent 22%),radial-gradient(circle at 68% 105%,rgba(155,114,255,.30),transparent 35%),linear-gradient(115deg,#11172E 0%,#1A1B45 56%,#182C50 100%); border:1px solid rgba(139,119,255,.32); border-radius:26px; padding:35px 38px; color:white; margin:0 0 27px 0; box-shadow:0 18px 48px rgba(40,28,110,.20); position:relative; overflow:hidden; }}
    .pp-hero:after {{ content:"✦"; position:absolute; right:7%; top:9%; color:rgba(91,222,246,.85); font-size:2.2rem; text-shadow:0 0 24px rgba(69,221,242,.8); }}
    .pp-eyebrow {{ color:#B9A7FF; font-weight:800; letter-spacing:.17em; font-size:.70rem; margin-bottom:13px; }}
    .pp-hero h1 {{ color:white !important; font-size:clamp(2rem,4vw,3.2rem); line-height:1.08; margin:0 0 12px 0; }}
    .pp-hero p {{ color:#C5D0E8 !important; font-size:1rem; max-width:650px; line-height:1.65; margin-bottom:20px; }}
    .pp-hero-tag {{ display:inline-block; border:1px solid rgba(185,167,255,.48); color:#E0D8FF; background:rgba(155,114,255,.13); border-radius:999px; padding:7px 12px; font-size:.78rem; font-weight:700; }}
    .pp-theme-label {{ color:var(--pp-muted); font-size:.66rem; font-weight:800; letter-spacing:.16em; margin:12px 0 7px; }}
    .pp-dark-mode-pill {{ display:flex; align-items:center; gap:9px; width:max-content; padding:8px 13px; border:1px solid rgba(155,114,255,.38); border-radius:999px; background:linear-gradient(110deg,rgba(155,114,255,.18),rgba(69,221,242,.09)); color:#E2DCFF; font-size:.72rem; font-weight:800; letter-spacing:.12em; box-shadow:0 0 22px rgba(125,86,255,.10); }}
    .pp-moon {{ display:inline-flex; align-items:center; justify-content:center; width:25px; height:25px; border-radius:50%; background:#8B68F2; color:#FFF; font-size:1rem; box-shadow:0 0 16px rgba(139,104,242,.45); }}
    .pp-section-kicker {{ color:#A88CFF; font-size:.68rem; font-weight:800; letter-spacing:.17em; margin:10px 0 5px; }}
    .pp-section-title {{ color:var(--pp-text) !important; font-family:'Manrope',sans-serif; font-size:1.7rem; font-weight:800; letter-spacing:-.055em; margin-bottom:3px; }}
    .pp-section-subtitle {{ color:var(--pp-muted) !important; margin-bottom:17px; font-size:.91rem; }}
    .pp-card {{ padding:20px 22px; height:100%; }}
    .pp-card-label {{ color:var(--pp-muted); font-size:.69rem; font-weight:800; letter-spacing:.12em; }}
    .pp-card-value {{ color:var(--pp-text); font-family:'Manrope',sans-serif; font-size:1.62rem; font-weight:800; margin:7px 0 3px; }}
    .pp-card-note {{ color:var(--pp-muted); font-size:.82rem; }}
    .pp-pill {{ display:inline-block; border-radius:999px; padding:5px 9px; background:rgba(155,114,255,.16); border:1px solid rgba(155,114,255,.28); color:#CBBEFF; font-size:.73rem; font-weight:800; }}
    .pp-divider {{ height:1px; background:linear-gradient(90deg,transparent,var(--pp-border),transparent); margin:25px 0; }}
    div.stButton > button,div[data-testid="stFormSubmitButton"] > button {{ border-radius:11px; font-weight:700; border:1px solid rgba(155,114,255,.28); padding:.58rem 1rem; transition:all .18s ease; }}
    div.stButton > button[kind="primary"],div[data-testid="stFormSubmitButton"] > button[kind="primary"] {{ background:linear-gradient(110deg,#8757F5,#5B6FEA 65%,#279DBB); color:#FFF; border:0; box-shadow:0 7px 20px rgba(105,80,225,.22); }}
    div.stButton > button[kind="primary"]:hover,div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {{ filter:brightness(1.12); box-shadow:0 9px 25px rgba(105,80,225,.34); transform:translateY(-1px); }}
    div.stButton > button[kind="secondary"] {{ background:#151C34; color:var(--pp-text); border-color:var(--pp-border); }}
    input,textarea,[data-baseweb="input"] > div,[data-baseweb="select"] > div {{ background:#11182D !important; color:var(--pp-text) !important; border-color:#303B60 !important; border-radius:10px !important; }}
    .stSelectbox label,.stRadio label,.stNumberInput label,.stDateInput label,.stTextInput label,.stMultiSelect label {{ color:var(--pp-muted) !important; font-weight:600; }}
    [data-baseweb="select"] *,[data-baseweb="input"] *,[data-baseweb="textarea"] * {{ color:var(--pp-text) !important; }}
    [data-testid="stDataFrame"],[data-testid="stTable"] {{ border:1px solid var(--pp-border); border-radius:14px; overflow:hidden; }}
    [data-testid="stAlert"] {{ border-radius:14px; border:1px solid var(--pp-border); }}
    .js-plotly-plot .plotly text,.js-plotly-plot .plotly .legendtext,.js-plotly-plot .plotly .xtick text,.js-plotly-plot .plotly .ytick text,.js-plotly-plot .plotly .gtitle,.js-plotly-plot .plotly .annotation-text {{ fill:var(--pp-text) !important; color:var(--pp-text) !important; }}
    .js-plotly-plot .plotly .gridlayer path {{ stroke:var(--pp-border) !important; }}
    @media(max-width:700px) {{ .pp-hero {{ padding:25px 22px; }} .block-container {{ padding-top:1rem; }} .pp-section-title {{ font-size:1.4rem; }} }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 📊PocketPilot")
    st.caption("PLAN  •  TRACK  •  THRIVE")
    st.markdown("---")
    st.markdown("### Your workspace")
    page = st.radio(
        "Navigate",
        ["Overview", "Spending analysis", "Monthly comparison", "Forecast & goals", "AI Financial Coach", "Transactions"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### Set up your month")
    monthly_budget = st.number_input(
        "Monthly spending budget (₹)", min_value=0, value=12000, step=500, key="monthly_budget"
    )
    monthly_income_target = st.number_input(
        "Expected monthly income (₹)", min_value=0, value=15000, step=500, key="income_target"
    )
    city = st.selectbox(
        "City for cost-of-living context",
        ["Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Pune", "Chandigarh", "Karnal", "Other"],
        index=2,
    )
    st.markdown("---")
    st.caption("🔒 Privacy-first by design")
    st.caption("No bank or UPI connection. Your uploaded CSV is processed in this app session.")


# ---------- Sample transaction data ----------
today = date.today()
month_start = today.replace(day=1)

# Demo transactions are distributed across elapsed days only. This prevents
# the sample dataset from accidentally containing future-dated purchases.
def sample_day(offset: int) -> date:
    elapsed_days_for_sample = max(1, today.day)
    return month_start + timedelta(days=offset % elapsed_days_for_sample)

sample_rows = [
    (sample_day(0), "Pocket money", "Income", 12000, "Other", "Monthly allowance"),
    (sample_day(1), "Hostel / rent", "Expense", 3500, "Housing", "Fixed"),
    (sample_day(2), "Groceries", "Expense", 650, "Food & groceries", "Variable"),
    (sample_day(3), "Metro / bus", "Expense", 240, "Transport", "Variable"),
    (sample_day(4), "Coffee with friends", "Expense", 180, "Eating out", "Lifestyle"),
    (sample_day(5), "Mobile recharge", "Expense", 299, "Bills & utilities", "Fixed"),
    (sample_day(6), "Online course", "Expense", 4099, "Education", "Growth"),
    (sample_day(7), "Groceries", "Expense", 430, "Food & groceries", "Variable"),
    (sample_day(8), "Cab", "Expense", 210, "Transport", "Variable"),
    (sample_day(9), "Lunch", "Expense", 160, "Eating out", "Lifestyle"),
    (sample_day(10), "Freelance task", "Income", 1800, "Freelance", "Extra income"),
    (sample_day(11), "Stationery", "Expense", 220, "Education", "Study"),
    (sample_day(12), "Movie", "Expense", 350, "Entertainment", "Lifestyle"),
    (sample_day(13), "Electricity share", "Expense", 400, "Bills & utilities", "Fixed"),
    (sample_day(14), "Groceries", "Expense", 520, "Food & groceries", "Variable"),
]
sample_df = pd.DataFrame(
    sample_rows,
    columns=["date", "description", "type", "amount", "category", "notes"],
)
sample_df["date"] = pd.to_datetime(sample_df["date"])

# ---------- CSV upload and validation ----------
st.sidebar.markdown("### Import transactions")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
use_sample = st.sidebar.toggle("Use sample transactions", value=uploaded_file is None)

REQUIRED_COLUMNS = {"date", "description", "type", "amount", "category"}
df = sample_df.copy()
upload_error = None

if uploaded_file is not None and not use_sample:
    try:
        uploaded_df = pd.read_csv(uploaded_file)
        uploaded_df.columns = [str(c).strip().lower() for c in uploaded_df.columns]
        missing = REQUIRED_COLUMNS - set(uploaded_df.columns)
        if missing:
            upload_error = (
                "Your CSV is missing required columns: "
                + ", ".join(sorted(missing))
                + ". Required columns: date, description, type, amount, category. "
                "Optional column: notes."
            )
        else:
            uploaded_df["date"] = pd.to_datetime(uploaded_df["date"], errors="coerce")
            uploaded_df["amount"] = pd.to_numeric(uploaded_df["amount"], errors="coerce")
            uploaded_df["type"] = uploaded_df["type"].astype(str).str.strip().str.title()
            uploaded_df["category"] = uploaded_df["category"].astype(str).str.strip()
            uploaded_df["description"] = uploaded_df["description"].astype(str).str.strip()
            if "notes" not in uploaded_df.columns:
                uploaded_df["notes"] = ""
            uploaded_df["notes"] = uploaded_df["notes"].fillna("").astype(str)
            uploaded_df = uploaded_df.dropna(subset=["date", "amount"])
            uploaded_df = uploaded_df[uploaded_df["type"].isin(["Income", "Expense"])]
            uploaded_df = uploaded_df[uploaded_df["amount"] >= 0]
            uploaded_df["date"] = pd.to_datetime(uploaded_df["date"])
            if uploaded_df.empty:
                upload_error = "No valid rows found. Check your date, amount, and type columns."
            else:
                df = uploaded_df[["date", "description", "type", "amount", "category", "notes"]].copy()
    except Exception as exc:
        upload_error = f"Could not read the CSV: {exc}"

if upload_error:
    st.sidebar.error(upload_error)
    st.sidebar.caption("Showing sample transactions until the CSV is corrected.")
    df = sample_df.copy()

# Manual transactions remain available during the current app session.
if "manual_transactions" not in st.session_state:
    st.session_state.manual_transactions = []

with st.sidebar.expander("➕ Add a transaction manually", expanded=False):
    with st.form("manual_transaction_form", clear_on_submit=True):
        manual_type = st.selectbox("Transaction type", ["Expense", "Income"])
        manual_amount = st.number_input("Amount (₹)", min_value=1, step=50, value=500)
        manual_date = st.date_input("Transaction date", value=today)
        manual_description = st.text_input("Description", placeholder="e.g. Salary, groceries")
        manual_category = st.selectbox(
            "Category",
            ["Food & groceries", "Housing", "Transport", "Education", "Bills & utilities",
             "Healthcare", "Eating out", "Entertainment", "Shopping", "Freelance", "Salary", "Other"],
        )
        manual_notes = st.text_input("Notes (optional)")
        if st.form_submit_button("Add transaction", type="primary"):
            if manual_description.strip():
                st.session_state.manual_transactions.append({
                    "date": pd.Timestamp(manual_date),
                    "description": manual_description.strip(),
                    "type": manual_type,
                    "amount": float(manual_amount),
                    "category": manual_category,
                    "notes": manual_notes.strip(),
                })
                st.sidebar.success(f"{manual_type} of ₹{manual_amount:,.0f} added.")
                st.rerun()
            else:
                st.sidebar.error("Please enter a description.")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0).clip(lower=0)
df["type"] = df["type"].astype(str).str.strip().str.title()
df["category"] = df["category"].fillna("Uncategorized").astype(str).str.strip()
df["description"] = df["description"].fillna("Transaction").astype(str)
df["notes"] = df["notes"].fillna("").astype(str)
df = df.dropna(subset=["date"])
df = df[df["type"].isin(["Income", "Expense"])].copy()
if st.session_state.manual_transactions:
    manual_df = pd.DataFrame(st.session_state.manual_transactions)
    manual_df["date"] = pd.to_datetime(manual_df["date"], errors="coerce")
    df = pd.concat([df, manual_df[["date", "description", "type", "amount", "category", "notes"]]], ignore_index=True)
df = df.sort_values("date")

# ---------- Flexible analysis period ----------
available_months = sorted(df["date"].dt.to_period("M").astype(str).unique())
default_month = f"{today.year}-{today.month:02d}"
if default_month not in available_months:
    default_month = available_months[-1] if available_months else default_month

st.sidebar.markdown("### Choose analysis period")
period_choice = st.sidebar.selectbox(
    "Show transactions for",
    ["Month to date", "Today", "Full month", "Last 30 days", "All transactions", "Custom date range"],
    index=4,
)

selected_month = default_month
if period_choice == "Full month":
    selected_month = st.sidebar.selectbox(
        "Select month",
        options=available_months if available_months else [default_month],
        index=(available_months.index(default_month) if default_month in available_months else 0),
    )
    month_period = pd.Period(selected_month, freq="M")
    period_start = month_period.start_time.date()
    period_end = month_period.end_time.date()
elif period_choice == "Today":
    period_start = today
    period_end = today
    month_period = pd.Period(today, freq="M")
elif period_choice == "Month to date":
    period_start = today.replace(day=1)
    period_end = today
    month_period = pd.Period(today, freq="M")
elif period_choice == "Last 30 days":
    period_start = today - timedelta(days=29)
    period_end = today
    month_period = pd.Period(today, freq="M")
elif period_choice == "Custom date range":
    min_date = df["date"].min().date() if not df.empty else today
    max_date = max(today, df["date"].max().date()) if not df.empty else today
    chosen_dates = st.sidebar.date_input(
        "Choose start and end dates",
        value=(max(min_date, today - timedelta(days=29)), max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if isinstance(chosen_dates, (tuple, list)) and len(chosen_dates) == 2:
        period_start, period_end = chosen_dates
    else:
        period_start = chosen_dates if isinstance(chosen_dates, date) else min_date
        period_end = period_start
    month_period = pd.Period(period_end, freq="M")
else:  # All transactions
    period_start = df["date"].min().date() if not df.empty else today
    period_end = df["date"].max().date() if not df.empty else today
    month_period = pd.Period(period_end, freq="M")

if period_choice == "All transactions":
    month_df = df.copy()
else:
    month_df = df[(df["date"].dt.date >= period_start) & (df["date"].dt.date <= period_end)].copy()
all_month_df = df.copy()

# Overall totals follow the selected analysis period (including All transactions).
income = float(month_df.loc[month_df["type"] == "Income", "amount"].sum())
expenses = float(month_df.loc[month_df["type"] == "Expense", "amount"].sum())
balance = income - expenses

# ---------- Current-month budget and smart forecast ----------
# This forecast always uses the current calendar month, regardless of
# the analysis-period filter selected in the sidebar.
current_month_period = pd.Period(today, freq="M")
current_month_df = df[
    (df["date"].dt.to_period("M") == current_month_period)
    & (df["date"].dt.date <= today)
].copy()

current_month_income = float(
    current_month_df.loc[
        current_month_df["type"] == "Income", "amount"
    ].sum()
)
current_month_expenses = float(
    current_month_df.loc[
        current_month_df["type"] == "Expense", "amount"
    ].sum()
)
current_month_balance = current_month_income - current_month_expenses

# Budget calculations
budget_left = float(monthly_budget - current_month_expenses)
budget_used_pct = (
    current_month_expenses / monthly_budget * 100
    if monthly_budget > 0 else 0.0
)

# Calendar days elapsed and remaining in this month
days_in_month = calendar.monthrange(today.year, today.month)[1]
elapsed_days = max(1, min(today.day, days_in_month))
days_left = max(0, days_in_month - elapsed_days)

# Do not show a misleading projection when there are no expenses this month.
forecast_has_data = not current_month_df[
    current_month_df["type"] == "Expense"
].empty

if forecast_has_data:
    daily_expense_rate = current_month_expenses / elapsed_days
    forecast_expenses = (
        current_month_expenses + daily_expense_rate * days_left
    )
else:
    daily_expense_rate = 0.0
    forecast_expenses = 0.0

forecast_budget_buffer = monthly_budget - forecast_expenses
forecast_budget_overrun = forecast_expenses - monthly_budget
forecast_balance = current_month_income - forecast_expenses

# Remaining budget spread evenly across the remaining calendar days.
if monthly_budget > 0 and days_left > 0:
    safe_daily_allowance = max(0.0, budget_left / days_left)
else:
    safe_daily_allowance = 0.0

# Simple, explainable budget-risk label.
if monthly_budget <= 0:
    forecast_risk = "Set a monthly budget"
elif not forecast_has_data:
    forecast_risk = "Not enough spending data"
elif forecast_budget_buffer < 0:
    forecast_risk = "Likely over budget"
elif forecast_expenses >= monthly_budget * 0.90:
    forecast_risk = "Budget at risk"
else:
    forecast_risk = "On track"

# ---------- Helper functions ----------
def rupees(value: float) -> str:
    return f"₹{value:,.0f}"

def section_heading(kicker: str, title: str, subtitle: str = "") -> None:
    st.markdown(
        f'<div class="pp-section-kicker">{kicker}</div>'
        f'<div class="pp-section-title">{title}</div>'
        f'<div class="pp-section-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )

def empty_state(message: str) -> None:
    st.info(message)

# ---------- Hero ----------
st.markdown(
    """
    <div class="pp-hero">
        <div class="pp-eyebrow">AI-POWERED FINANCIAL WELLNESS</div>
        <h1>Your money.<br>Your mission.</h1>
        <p>
            Track your spending, uncover patterns, and make smarter money moves
            with a clearer view of what is happening now and what comes next.
        </p>
        <div class="pp-hero-tag">✦ Navigate your financial future</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Main dashboard pages ----------
if page == "Overview":
    section_heading(
        "YOUR MONEY AT A GLANCE",
        "Your financial snapshot",
        f"Income, expenses and balance: {period_choice.lower()} · {period_start.strftime('%d %b %Y')} to {period_end.strftime('%d %b %Y')}. Budget and forecast: current calendar month.",
    )
    m1, m2, m3, m4 = st.columns(4, gap="medium")
    with m1:
        st.metric("TOTAL INCOME", rupees(income), "Money received")
    with m2:
        st.metric("TOTAL EXPENSES", rupees(expenses), "Money spent so far")
    with m3:
        st.metric("NET BALANCE", rupees(balance), "Income minus expenses")
    with m4:
        st.metric(
            "THIS MONTH'S BUDGET LEFT",
            rupees(budget_left),
            "Over budget" if budget_left < 0 else "Within budget",
            delta_color="inverse" if budget_left < 0 else "normal",
        )

    if monthly_budget <= 0:
        st.info("Set a monthly spending budget to see your budget usage.")
    elif budget_used_pct > 100:
        st.warning(f"⚠️ You've used {budget_used_pct:.0f}% of your monthly budget and are {rupees(abs(budget_left))} over budget. Review your spending.")
    elif budget_used_pct >= 80:
        st.warning(f"👀 You've used {budget_used_pct:.0f}% of your monthly budget. Keep an eye on the remaining amount.")
    elif budget_used_pct >= 50:
        st.info(f"📊 You've used {budget_used_pct:.0f}% of your monthly budget. Keep tracking your spending.")
    else:
        st.success(f"🌱 You've used {budget_used_pct:.0f}% of your monthly budget. Every transaction helps build a clearer picture.")

    st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.35, 1], gap="large")
    with left:
        section_heading("SPENDING BREAKDOWN", "Where your money goes", "Expense totals by category.")
        category_df = month_df[month_df["type"] == "Expense"].groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
        if category_df.empty:
            empty_state("No expenses recorded for this month yet.")
        else:
            fig = px.pie(
                category_df, names="category", values="amount", hole=0.68,
                color_discrete_sequence=["#9B7BFF", "#45D6E8", "#6F83C9", "#A78BFA", "#4EABC0", "#C08CFF", "#71809B"],
            )
            # Keep the percentage on the donut, and show exact rupee amounts in a list below it.
            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                texttemplate="%{percent}",
                hovertemplate="%{label}<br>Amount spent: ₹%{value:,.0f}<br>Share: %{percent}<extra></extra>",
            )
            fig.update_layout(
                # Hide Plotly's built-in legend: it was squeezing category names
                # against/inside the donut on some screen widths. Categories are
                # listed clearly in the table underneath instead.
                showlegend=False,
                margin=dict(t=12, b=12, l=12, r=12), height=340,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                annotations=[dict(text=rupees(expenses), x=0.5, y=0.5, font_size=22, font_color=THEME["text"], showarrow=False)],
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                f'<div style="font-weight:800; font-size:.88rem; margin:8px 0 10px; color:{THEME["text"]};">Exact amount by category</div>',
                unsafe_allow_html=True,
            )
            amount_breakdown = category_df.copy()
            total_for_share = float(category_df["amount"].sum()) or 1.0
            amount_breakdown["Share"] = (amount_breakdown["amount"] / total_for_share * 100).map(lambda x: f"{x:.1f}%")
            amount_breakdown["amount"] = amount_breakdown["amount"].map(rupees)
            amount_breakdown.columns = ["Category", "Amount spent", "Share"]
            st.dataframe(amount_breakdown, use_container_width=True, hide_index=True, column_config={
                "Category": st.column_config.TextColumn("Category", width="medium"),
                "Amount spent": st.column_config.TextColumn("Amount spent", width="medium"),
                "Share": st.column_config.TextColumn("Share of spending", width="small"),
            })
    with right:
        section_heading(
            "MONTH-END OUTLOOK",
            "A simple forecast",
            "Current-month estimate based on recorded expenses, regardless of the analysis filter.",
        )
        if not forecast_has_data:
            st.info("No current-month expenses recorded yet. Add transactions to generate a forecast.")
        else:
            budget_position_text = (
                f"{rupees(abs(forecast_budget_overrun))} over budget"
                if forecast_budget_overrun > 0
                else f"{rupees(abs(forecast_budget_overrun))} under budget"
            )
            st.markdown(
                f"""
                <div class="pp-card">
                    <div class="pp-card-label">PROJECTED MONTH-END EXPENSES</div>
                    <div class="pp-card-value">{rupees(forecast_expenses)}</div>
                    <div class="pp-card-note">Average recorded spending: {rupees(daily_expense_rate)} per elapsed day.</div>
                    <div style="height:14px"></div>
                    <div class="pp-card-label">PROJECTED BUDGET POSITION</div>
                    <div class="pp-card-value" style="color:{'#FF647C' if forecast_budget_overrun > 0 else '#9B7BFF'}">
                        {budget_position_text}
                    </div>
                    <div class="pp-card-note">A rule-based estimate, not a guarantee. It assumes all expenses so far have been recorded.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")
            if monthly_budget <= 0:
                st.info("Set a monthly budget to assess your forecast.")
            elif forecast_budget_overrun > 0:
                st.warning("Try reducing flexible spending for the rest of the month.")
            elif forecast_risk == "Budget at risk":
                st.warning("Your current pace is close to the budget limit. Monitor the remaining days.")
            else:
                st.success("Your current pace is projected to stay within budget.")

    # Extra breathing room after the breakdown/outlook, before the next section.
    st.markdown('<div class="pp-divider"></div><div style="height:72px"></div>', unsafe_allow_html=True)
    section_heading("NEXT BEST ACTION", "Small steps that can help", "Practical suggestions based on the transactions shown.")
    suggestions = []
    expense_df = month_df[month_df["type"] == "Expense"]
    if monthly_budget > 0 and current_month_expenses / monthly_budget >= 0.8:
        suggestions.append(("Watch your pace", "You've used at least 80% of this month's budget. Pause non-essential purchases until you review the remaining days."))
    if not expense_df.empty:
        top_category = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False)
        if len(top_category):
            suggestions.append(("Review your biggest category", f"{top_category.index[0]} is your largest expense category at {rupees(top_category.iloc[0])}. Check whether any upcoming costs can be reduced."))
        eating_out = expense_df[expense_df["category"].str.lower().str.contains("eating|restaurant|cafe|food delivery", regex=True)]["amount"].sum()
        if eating_out > 0:
            suggestions.append(("Plan meals ahead", f"You've recorded {rupees(eating_out)} in eating-out purchases. A weekly meal plan may help you manage this category."))
    if balance > 0:
        suggestions.append(("Give your surplus a purpose", f"Your recorded net balance is {rupees(balance)}. Consider assigning part of it to savings before spending it elsewhere."))
    if not suggestions:
        suggestions.append(("Start with one habit", "Record each transaction and check your budget once a week. Consistency is more useful than perfection."))
    cards = st.columns(min(3, len(suggestions)), gap="medium")
    for i, (title, body) in enumerate(suggestions[:3]):
        with cards[i]:
            st.markdown(f'<div class="pp-card"><div class="pp-card-label">ACTION {i+1:02d}</div><div style="font-size:1.08rem;font-weight:800;margin:10px 0;color:{THEME["text"]}">{title}</div><div class="pp-card-note" style="font-size:.9rem;line-height:1.6">{body}</div></div>', unsafe_allow_html=True)

    # ---------- User-defined category budgets ----------
    st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
    section_heading(
        "PERSONAL CATEGORY LIMITS",
        "Set your own spending limits",
        "Choose a monthly limit for each category. Leave a category at ₹0 if you do not want to track a limit for it.",
    )

    default_budget_categories = [
        "Food & groceries", "Eating out", "Transport", "Shopping",
        "Entertainment", "Housing", "Education", "Bills & utilities",
        "Healthcare", "Other",
    ]
    categories_in_data = sorted(
        df.loc[df["type"] == "Expense", "category"].dropna().astype(str).unique().tolist()
    )
    category_budget_options = list(dict.fromkeys(default_budget_categories + categories_in_data))

    if "category_budgets" not in st.session_state:
        st.session_state.category_budgets = {}

    with st.form("category_budget_form"):
        st.markdown("**Monthly category limits (₹)**")
        budget_columns = st.columns(2, gap="medium")
        submitted_category_limits = {}
        for index, category_name in enumerate(category_budget_options):
            with budget_columns[index % 2]:
                submitted_category_limits[category_name] = st.number_input(
                    category_name,
                    min_value=0,
                    max_value=10000000,
                    value=int(st.session_state.category_budgets.get(category_name, 0)),
                    step=250,
                    key=f"category_limit_input_{category_name}",
                    help="Enter 0 to leave this category without a monthly limit.",
                )
        save_category_limits = st.form_submit_button("Save category limits", type="primary")

    if save_category_limits:
        st.session_state.category_budgets = {
            name: int(limit)
            for name, limit in submitted_category_limits.items()
            if int(limit) > 0
        }
        st.success("Your category limits have been saved for this app session.")

    # Compare current-month recorded spending against each saved category limit.
    current_category_spend = (
        current_month_df[current_month_df["type"] == "Expense"]
        .groupby("category")["amount"].sum().to_dict()
    )
    active_category_limits = st.session_state.category_budgets

    if not active_category_limits:
        st.info("Set one or more category limits above to unlock personalized category alerts.")
    else:
        st.markdown("### Category budget status")
        for category_name, category_limit in active_category_limits.items():
            category_spent = float(current_category_spend.get(category_name, 0.0))
            category_used_pct = (category_spent / category_limit * 100) if category_limit > 0 else 0
            status_col, amount_col = st.columns([2, 1], gap="medium")
            with status_col:
                st.markdown(f"**{category_name}**")
                st.progress(min(category_used_pct / 100, 1.0))
                if category_spent > category_limit:
                    st.error(
                        f"Over limit by {rupees(category_spent - category_limit)}. "
                        "Pause or reduce spending in this category."
                    )
                elif category_used_pct >= 80:
                    st.warning(
                        f"You've used {category_used_pct:.0f}% of this limit. "
                        f"{rupees(category_limit - category_spent)} left."
                    )
                else:
                    st.success(
                        f"{category_used_pct:.0f}% used · "
                        f"{rupees(category_limit - category_spent)} remaining."
                    )
            with amount_col:
                st.metric("SPENT / LIMIT", f"{rupees(category_spent)} / {rupees(category_limit)}")

        # Actionable category insights based on the largest current-month spends.
        limited_categories = [
            (name, float(current_category_spend.get(name, 0.0)), float(limit))
            for name, limit in active_category_limits.items()
        ]
        over_limit_categories = [item for item in limited_categories if item[1] > item[2]]
        near_limit_categories = [
            item for item in limited_categories
            if item[2] > 0 and item[2] * 0.8 <= item[1] <= item[2]
        ]
        if over_limit_categories:
            worst_category = max(over_limit_categories, key=lambda item: item[1] - item[2])
            st.info(
                f"💡 **Suggested action:** {worst_category[0]} is over its limit by "
                f"{rupees(worst_category[1] - worst_category[2])}. Consider pausing "
                "non-essential purchases in this category for the rest of the month."
            )
        elif near_limit_categories:
            closest_category = max(near_limit_categories, key=lambda item: item[1] / item[2])
            st.info(
                f"💡 **Suggested action:** {closest_category[0]} is nearing its limit. "
                "Check upcoming needs before making another purchase."
            )
        else:
            st.info("💡 **Good progress:** Your spending is currently below 80% of every saved category limit.")

elif page == "Spending analysis":
    section_heading("UNDERSTAND THE PATTERN", "Spending analysis", "Explore your expenses by category and over time.")
    expenses_df = month_df[month_df["type"] == "Expense"].copy()
    if expenses_df.empty:
        empty_state("No expenses available for the selected month.")
    else:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            cat = expenses_df.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=True)
            fig = px.bar(cat, x="amount", y="category", orientation="h", text="amount", color="amount", color_continuous_scale=["#EAD8C2", "#9B7BFF"])
            fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside", cliponaxis=False)
            fig.update_layout(title="Expenses by category", height=390, margin=dict(l=10, r=45, t=55, b=10), showlegend=False, coloraxis_showscale=False, xaxis_title="", yaxis_title="", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=THEME["text"], family="DM Sans"), colorway=["#9B7BFF", "#45D6E8", "#6F83C9", "#A78BFA", "#4EABC0"])
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            daily = expenses_df.groupby(expenses_df["date"].dt.date, as_index=False)["amount"].sum()
            daily.columns = ["date", "amount"]
            fig = px.line(daily, x="date", y="amount", markers=True, title="Daily spending")
            fig.update_traces(line_color="#9B7BFF", marker_color="#79685A", hovertemplate="%{x}<br>₹%{y:,.0f}<extra></extra>")
            fig.update_layout(height=390, margin=dict(l=10, r=10, t=55, b=10), xaxis_title="", yaxis_title="Amount (₹)", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=THEME["text"], family="DM Sans"), colorway=["#9B7BFF", "#45D6E8", "#6F83C9", "#A78BFA", "#4EABC0"])
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
        section_heading("CATEGORY DETAILS", "Your expense mix", "Share of total expenses and average transaction size.")
        summary = expenses_df.groupby("category").agg(total=("amount", "sum"), transactions=("amount", "count"), average=("amount", "mean")).reset_index()
        summary["share"] = summary["total"] / summary["total"].sum() * 100
        summary = summary.sort_values("total", ascending=False)
        summary["total"] = summary["total"].map(rupees)
        summary["average"] = summary["average"].map(rupees)
        summary["share"] = summary["share"].map(lambda x: f"{x:.1f}%")
        summary.columns = ["Category", "Total spent", "Transactions", "Average transaction", "Share of expenses"]
        st.dataframe(summary, use_container_width=True, hide_index=True)

    st.caption("Cost-of-living note: local costs vary substantially by neighbourhood and lifestyle. Treat city context as background, not a personalized benchmark.")
    city_cost_data = {
        "Delhi": "Urban transport, rent, and eating out can vary widely by locality.",
        "Mumbai": "Housing and commute choices often make a large difference to monthly costs.",
        "Bengaluru": "Housing, transport, and food delivery can be important categories to track.",
        "Hyderabad": "Compare housing and commute costs alongside discretionary spending.",
        "Pune": "Housing, commuting, and student lifestyle costs vary by area.",
        "Chandigarh": "Transport and housing choices can change the monthly picture.",
        "Karnal": "A smaller-city budget may look different from a metro; use your own records first.",
        "Other": "Use your own transaction history as the most relevant starting point.",
    }
    st.markdown(f'<div class="pp-card"><div class="pp-card-label">CITY CONTEXT · {city.upper()}</div><div style="margin-top:10px;color:{THEME["muted"]};line-height:1.65">{city_cost_data[city]}</div></div>', unsafe_allow_html=True)

elif page == "Monthly comparison":
    section_heading(
        "SEE THE BIGGER PICTURE",
        "Monthly comparison",
        "Compare income, expenses, and net balance across every month in your uploaded history.",
    )
    comparison_df = df.copy()
    comparison_df["month"] = comparison_df["date"].dt.to_period("M").astype(str)
    monthly = comparison_df.pivot_table(
        index="month", columns="type", values="amount", aggfunc="sum", fill_value=0
    ).reset_index()
    for col in ["Income", "Expense"]:
        if col not in monthly.columns:
            monthly[col] = 0.0
    monthly["Net balance"] = monthly["Income"] - monthly["Expense"]
    monthly["Monthly budget"] = float(monthly_budget)
    monthly["Budget remaining"] = monthly["Monthly budget"] - monthly["Expense"]
    monthly = monthly.sort_values("month")

    if monthly.empty:
        empty_state("Upload transactions from at least one month to see a comparison.")
    else:
        # Mark the current month as partial when the data ends before month-end.
        monthly["Month label"] = monthly["month"].map(
            lambda value: pd.Period(value, freq="M").strftime("%b %Y")
        )
        current_key = f"{today.year}-{today.month:02d}"
        if current_key in monthly["month"].values:
            monthly.loc[monthly["month"] == current_key, "Month label"] += " (month to date)"

        metric_months = monthly[monthly["month"] != current_key]
        if current_key in monthly["month"].values:
            latest = monthly[monthly["month"] == current_key].iloc[0]
        else:
            latest = monthly.iloc[-1]
        c1, c2, c3 = st.columns(3, gap="medium")
        c1.metric("LATEST MONTH INCOME", rupees(float(latest["Income"])))
        c2.metric("LATEST MONTH EXPENSES", rupees(float(latest["Expense"])))
        c3.metric("LATEST MONTH NET", rupees(float(latest["Net balance"])))

        st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
        compare_metric = st.selectbox(
            "Choose what to compare",
            ["Income", "Expense", "Net balance", "Budget remaining"],
            index=1,
            key="monthly_compare_metric",
        )
        fig = px.bar(
            monthly,
            x="Month label",
            y=compare_metric,
            title=f"Month-wise {compare_metric.lower()}",
            text_auto=".2s",
        )
        if compare_metric == "Expense":
            fig.add_hline(
                y=float(monthly_budget),
                line_dash="dash",
                line_color="#45DDF2",
                annotation_text=f"Monthly budget · {rupees(monthly_budget)}",
                annotation_position="top left",
            )
        fig.update_layout(
            height=390, margin=dict(l=10, r=10, t=55, b=10),
            xaxis_title="Month", yaxis_title="Amount (₹)",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=THEME["text"], family="DM Sans"),
            xaxis=dict(gridcolor=THEME["grid"], zerolinecolor=THEME["grid"]),
            yaxis=dict(gridcolor=THEME["grid"], zerolinecolor=THEME["grid"]),
        )
        st.plotly_chart(fig, use_container_width=True)

        trend_fig = px.line(
            monthly, x="Month label", y=["Income", "Expense", "Net balance"],
            markers=True, title="Income, expenses and net balance trend",
        )
        trend_fig.update_layout(
            height=420, margin=dict(l=10, r=10, t=55, b=10),
            xaxis_title="Month", yaxis_title="Amount (₹)",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(trend_fig, use_container_width=True)

        st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
        section_heading("MONTH-BY-MONTH NUMBERS", "Detailed comparison", "Use the table to compare totals and spot changes between months.")
        table = monthly[["Month label", "Income", "Expense", "Net balance", "Monthly budget", "Budget remaining"]].copy()
        table["Change in expenses"] = table["Expense"].diff()
        table["Change in expenses (%)"] = table["Expense"].pct_change() * 100
        for col in ["Income", "Expense", "Net balance", "Monthly budget", "Budget remaining", "Change in expenses"]:
            table[col] = table[col].map(rupees)
        table["Change in expenses (%)"] = table["Change in expenses (%)"].map(
            lambda value: "—" if pd.isna(value) else f"{value:+.1f}%"
        )
        table = table.rename(columns={"Month label": "Month"})
        st.dataframe(table, use_container_width=True, hide_index=True)

        st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
        section_heading("CATEGORY COMPARISON", "Which categories changed?", "Choose a category to compare its monthly expense pattern.")
        expense_rows = comparison_df[comparison_df["type"] == "Expense"].copy()
        category_list = sorted(expense_rows["category"].dropna().unique().tolist())
        if category_list:
            chosen_category = st.selectbox("Expense category", category_list, key="comparison_category")
            category_monthly = expense_rows[expense_rows["category"] == chosen_category].copy()
            category_monthly["Month"] = category_monthly["date"].dt.to_period("M").astype(str)
            category_monthly = category_monthly.groupby("Month", as_index=False)["amount"].sum()
            category_monthly["Month label"] = category_monthly["Month"].map(
                lambda value: pd.Period(value, freq="M").strftime("%b %Y")
            )
            cat_fig = px.bar(
                category_monthly, x="Month label", y="amount", text_auto=".2s",
                title=f"{chosen_category}: month-wise spending",
            )
            cat_fig.update_layout(
                height=340, margin=dict(l=10, r=10, t=55, b=10),
                xaxis_title="Month", yaxis_title="Amount (₹)",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(cat_fig, use_container_width=True)
        else:
            empty_state("No expense categories are available yet.")

        st.caption("The current month is marked as month to date when applicable. Compare it carefully with completed months because it may contain fewer days of transactions.")

elif page == "Forecast & goals":
    section_heading("PLAN AHEAD", "Forecast & savings goals", "A lightweight forecast plus a goal tracker to help you plan.")
    f1, f2, f3, f4 = st.columns(4, gap="medium")
    f1.metric("SPENT SO FAR", rupees(current_month_expenses))
    f2.metric(
        "PROJECTED MONTH-END",
        rupees(forecast_expenses) if forecast_has_data else "N/A",
    )
    f3.metric("DAYS REMAINING", days_left)
    f4.metric("SAFE DAILY ALLOWANCE", rupees(safe_daily_allowance))

    st.markdown("### Monthly budget outlook")
    if not forecast_has_data:
        st.info(
            "No current-month expense records found. "
            "Add transactions to generate a forecast."
        )
    elif monthly_budget <= 0:
        st.warning("Set a monthly budget to assess budget risk.")
    elif forecast_risk == "Likely over budget":
        st.error(
            f"Your projected spending exceeds your budget by "
            f"{rupees(abs(forecast_budget_buffer))}."
        )
    elif forecast_risk == "Budget at risk":
        st.warning(
            f"Your projected budget buffer is "
            f"{rupees(forecast_budget_buffer)}. Monitor your remaining spending."
        )
    else:
        st.success(
            f"Your projected spending is within budget. "
            f"Estimated buffer: {rupees(forecast_budget_buffer)}."
        )

    st.caption(
        f"Average daily spending: {rupees(daily_expense_rate)}. "
        f"Based on {elapsed_days} elapsed calendar days and "
        f"{days_left} remaining days. This assumes all expenses so far "
        f"have been entered."
        if forecast_has_data
        else "Forecasts appear once current-month expenses are recorded."
    )

    st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
    section_heading("SAVINGS GOAL", "Give your money a target", "Set a goal and track progress. This is a planning aid, not a bank account.")
    if "goal_name" not in st.session_state:
        st.session_state.goal_name = "Emergency fund"
    if "goal_target" not in st.session_state:
        st.session_state.goal_target = 10000
    if "goal_saved" not in st.session_state:
        st.session_state.goal_saved = 1500

    with st.form("goal_form"):
        goal_name = st.text_input("Goal name", value=st.session_state.goal_name)
        g1, g2 = st.columns(2)
        with g1:
            goal_target = st.number_input("Target amount (₹)", min_value=1, value=int(st.session_state.goal_target), step=500)
        with g2:
            goal_saved = st.number_input("Already saved (₹)", min_value=0, value=int(st.session_state.goal_saved), step=250)
        goal_submit = st.form_submit_button("Update goal", type="primary")
    if goal_submit:
        st.session_state.goal_name = goal_name.strip() or "My savings goal"
        st.session_state.goal_target = int(goal_target)
        st.session_state.goal_saved = int(goal_saved)
        st.success("Savings goal updated.")
    target = max(1, int(st.session_state.goal_target))
    saved = max(0, int(st.session_state.goal_saved))
    progress = min(saved / target, 1.0)
    st.markdown(f"**{st.session_state.goal_name}**")
    st.progress(progress)
    st.write(f"{rupees(saved)} saved out of {rupees(target)} · {progress*100:.1f}% complete")
    remaining_goal = max(0, target - saved)
    if remaining_goal:
        st.info(f"You need {rupees(remaining_goal)} more to reach this goal. For example, saving {rupees(remaining_goal / 5)} per week for five weeks would cover the gap.")
    else:
        st.success("Goal reached! You can set a new target or keep building your buffer.")

    st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
    section_heading("BUDGET SCENARIOS", "What if you cut spending?", "Illustrative scenarios based on recorded expenses so far.")
    scenario_cut = st.slider("Potential reduction in remaining flexible spending", min_value=0, max_value=40, value=10, step=5)
    projected_saving = max(0, forecast_expenses - current_month_expenses) * scenario_cut / 100
    adjusted_forecast = forecast_expenses - projected_saving
    s1, s2 = st.columns(2, gap="medium")
    with s1:
        st.metric("Scenario month-end spend", rupees(adjusted_forecast), f"{rupees(projected_saving)} lower")
    with s2:
        st.metric("Scenario budget position", rupees(monthly_budget - adjusted_forecast), "Remaining" if monthly_budget - adjusted_forecast >= 0 else "Over budget")

    st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
    section_heading("RECURRING BILLS", "Keep regular costs visible", "Track expected bills here; these are reminders, not automatic payments.")
    if "bills" not in st.session_state:
        st.session_state.bills = [
            {"name": "Mobile recharge", "amount": 299, "due_day": 5, "category": "Bills & utilities"},
            {"name": "Hostel / rent", "amount": 3500, "due_day": 1, "category": "Housing"},
        ]
    with st.form("bill_form", clear_on_submit=True):
        b1, b2 = st.columns([1.2, 1])
        with b1:
            bill_name = st.text_input("Bill name")
            bill_category = st.selectbox("Category", ["Housing", "Bills & utilities", "Education", "Transport", "Other"])
        with b2:
            bill_amount = st.number_input("Amount (₹)", min_value=0, value=0, step=50)
            bill_due = st.number_input("Due day of month", min_value=1, max_value=31, value=5, step=1)
        add_bill = st.form_submit_button("Add bill", type="primary")
    if add_bill:
        if bill_name.strip() and bill_amount > 0:
            st.session_state.bills.append({"name": bill_name.strip(), "amount": int(bill_amount), "due_day": int(bill_due), "category": bill_category})
            st.success(f"Added {bill_name.strip()}.")
        else:
            st.error("Enter a bill name and an amount greater than zero.")
    if st.session_state.bills:
        bills_df = pd.DataFrame(st.session_state.bills)
        bills_df.columns = ["Bill", "Amount (₹)", "Due day", "Category"]
        st.dataframe(bills_df, use_container_width=True, hide_index=True)
        st.caption(f"Total planned recurring bills: {rupees(sum(int(b['amount']) for b in st.session_state.bills))} per month.")
    else:
        empty_state("No recurring bills added yet.")

elif page == "AI Financial Coach":
    section_heading(
        "YOUR PERSONAL MONEY GUIDE",
        "AI Financial Coach",
        "Ask questions about your spending, budget, savings goals and monthly forecast.",
    )

    # Build a compact context from verified calculations already made by Python.
    # Never send the underlying transaction table to the AI provider.
    coach_category_spend = (
        current_month_df[current_month_df["type"] == "Expense"]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    coach_category_limits = st.session_state.get("category_budgets", {})

    coach_category_status = {}
    for category_name, category_limit in coach_category_limits.items():
        category_spent = float(coach_category_spend.get(category_name, 0.0))
        limit_value = float(category_limit)
        coach_category_status[category_name] = {
            "spent": round(category_spent, 2),
            "monthly_limit": round(limit_value, 2),
            "used_percent": round(
                (category_spent / limit_value * 100) if limit_value > 0 else 0.0,
                1,
            ),
            "remaining": round(limit_value - category_spent, 2),
        }

    coach_context = {
        "currency": "INR",
        "analysis_period": {
            "selection": period_choice,
            "start_date": str(period_start),
            "end_date": str(period_end),
            "income": round(income, 2),
            "expenses": round(expenses, 2),
            "net_balance": round(balance, 2),
            "transaction_count": int(len(month_df)),
        },
        "current_month": {
            "month": str(current_month_period),
            "income_recorded": round(current_month_income, 2),
            "expenses_recorded": round(current_month_expenses, 2),
            "net_balance_recorded": round(current_month_balance, 2),
            "monthly_budget": round(float(monthly_budget), 2),
            "budget_left": round(budget_left, 2),
            "budget_used_percent": round(budget_used_pct, 1),
        },
        "forecast": {
            "has_expense_data": bool(forecast_has_data),
            "projected_month_end_expenses": (
                round(forecast_expenses, 2) if forecast_has_data else None
            ),
            "projected_month_end_balance": (
                round(forecast_balance, 2) if forecast_has_data else None
            ),
            "average_daily_spending": round(daily_expense_rate, 2),
            "days_elapsed": int(elapsed_days),
            "days_remaining": int(days_left),
            "safe_daily_allowance": round(safe_daily_allowance, 2),
            "budget_risk": forecast_risk,
        },
        "current_month_category_spending": {
            str(category): round(float(amount), 2)
            for category, amount in coach_category_spend.items()
        },
        "category_monthly_limits": {
            str(category): round(float(limit), 2)
            for category, limit in coach_category_limits.items()
        },
        "category_budget_status": coach_category_status,
        "savings_goal": {
            "name": st.session_state.get("goal_name"),
            "target": st.session_state.get("goal_target"),
            "saved": st.session_state.get("goal_saved"),
        },
        "planned_recurring_bills_total": round(
            sum(float(bill.get("amount", 0)) for bill in st.session_state.get("bills", [])),
            2,
        ),
    }

    st.markdown("### Ask PocketPilot")
    st.markdown("**Not sure what to ask? Try one of these:**")

    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []

    # Build relevant suggestions from the user's current financial summary.
    suggestion_questions = [
        "Where am I spending the most?",
        "How can I reduce my spending this month?",
        "Am I on track with my monthly budget?",
        "How much can I safely spend per day?",
    ]
    if coach_category_spend.empty:
        suggestion_questions[0] = "How do I add transactions to PocketPilot?"
    elif len(coach_category_spend) > 1:
        top_spending_category = str(coach_category_spend.index[0])
        suggestion_questions[1] = f"How can I reduce my spending on {top_spending_category}?"
    if coach_category_limits:
        suggestion_questions[2] = "Which of my categories are over budget?"
    if st.session_state.get("goal_target"):
        suggestion_questions[3] = "Am I on track to reach my savings goal?"

    suggestion_cols = st.columns(2)
    for index, suggested_question in enumerate(suggestion_questions):
        with suggestion_cols[index % 2]:
            if st.button(suggested_question, key=f"ai_suggestion_{index}", use_container_width=True):
                st.session_state.pending_ai_question = suggested_question
                st.rerun()

    chat_controls = st.columns([1, 5])
    with chat_controls[0]:
        if st.button("Clear chat", key="clear_ai_chat"):
            st.session_state.ai_chat_history = []
            st.rerun()

    for chat_message in st.session_state.ai_chat_history:
        with st.chat_message(chat_message["role"]):
            st.markdown(chat_message["content"])

    prompt = st.session_state.pop("pending_ai_question", None)
    typed_prompt = st.chat_input(
        "Ask a question about your finances...",
        max_chars=1000,
        key="pocketpilot_ai_question",
    )
    if typed_prompt:
        prompt = typed_prompt

    if prompt:
        previous_messages = st.session_state.ai_chat_history[-8:]
        conversation_text = ""
        if previous_messages:
            conversation_text = "Recent conversation (for continuity):\\n" + "\n".join(
                f"{'User' if item['role'] == 'user' else 'PocketPilot'}: {item['content']}"
                for item in previous_messages
            ) + "\n\n"

        st.session_state.ai_chat_history.append(
            {"role": "user", "content": prompt.strip()}
        )
        with st.chat_message("user"):
            st.markdown(prompt.strip())

        with st.chat_message("assistant"):
            with st.spinner("PocketPilot is thinking..."):
                try:
                    if not configured_providers():
                        raise AIEngineError("AI provider unavailable")
                    result = ask_financial_coach(
                        question=conversation_text + "Current question: " + prompt.strip(),
                        financial_context=coach_context,
                    )
                    assistant_answer = result["answer"]
                except (AIEngineError, ValueError):
                    # Context-aware local fallback. Keep answers specific to the question
                    # rather than repeating the same top-category recommendation.
                    category_totals = coach_context.get("current_month_category_spending", {})
                    ranked = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)
                    total_spend = sum(category_totals.values())
                    question_lower = prompt.strip().lower()
                    top_category, top_amount = ranked[0] if ranked else ("", 0)
                    selected_category = next(
                        (name for name in category_totals if name.lower() in question_lower),
                        None,
                    )

                    if any(term in question_lower for term in ("10%", "10 percent", "reduce expenses by", "cut expenses by", "if i reduce")):
                        reduction_match = __import__("re").search(r"(\\d+(?:\\.\\d+)?)\\s*%?", question_lower)
                        reduction_pct = float(reduction_match.group(1)) if reduction_match else 10.0
                        reduction_pct = min(max(reduction_pct, 0), 100)
                        saving = total_spend * reduction_pct / 100
                        assistant_answer = (
                            f"If you reduce your recorded category spending by **{reduction_pct:g}%**, "
                            f"you would save approximately **₹{saving:,.0f}** over the selected period. "
                            f"Your spending would fall from **₹{total_spend:,.0f}** to about "
                            f"**₹{total_spend - saving:,.0f}**. This is an estimate based on the transactions currently loaded."
                        ) if total_spend else "I need recorded expenses for this period before I can calculate a savings scenario."

                    elif any(term in question_lower for term in ("enough money", "money left", "left this month", "month end", "end of the month")):
                        projected_balance = coach_context.get("forecast", {}).get("projected_month_end_balance")
                        projected_expenses = coach_context.get("forecast", {}).get("projected_month_end_expenses")
                        if projected_balance is not None:
                            outlook = "positive" if projected_balance >= 0 else "negative"
                            assistant_answer = (
                                f"Based on your current spending pace, your projected month-end balance is "
                                f"**₹{projected_balance:,.0f}** ({outlook}). Estimated month-end expenses are "
                                f"**₹{projected_expenses:,.0f}**. Treat this as a forecast, not a guarantee."
                            )
                        else:
                            assistant_answer = "I don't have enough current-month expense data to estimate your month-end balance yet."

                    elif any(term in question_lower for term in ("compare", "compared", "since", "last month", "previous month", "changed")):
                        assistant_answer = (
                            f"For the selected analysis period, recorded income is **₹{income:,.0f}**, "
                            f"expenses are **₹{expenses:,.0f}**, and the net is **₹{balance:,.0f}**. "
                            "Choose a different month or comparison period in the sidebar to compare periods."
                        )

                    elif any(term in question_lower for term in ("over budget", "within budget", "budget", "category limit", "limits")):
                        if coach_category_status:
                            over = [
                                (name, info) for name, info in coach_category_status.items()
                                if info["spent"] > info["monthly_limit"]
                            ]
                            if over:
                                assistant_answer = "These tracked categories are over their limits: " + "; ".join(
                                    f"**{name}** by **₹{info['spent'] - info['monthly_limit']:,.0f}**"
                                    for name, info in over
                                ) + "."
                            else:
                                assistant_answer = "Your tracked categories are currently within their set limits. Keep checking them during the month so small overspending doesn't build up."
                        else:
                            assistant_answer = (
                                f"You have recorded **₹{expenses:,.0f}** in expenses against a monthly budget "
                                f"of **₹{monthly_budget:,.0f}**. That leaves **₹{budget_left:,.0f}** "
                                f"({budget_used_pct:.1f}% of the budget used)."
                            )

                    elif any(term in question_lower for term in ("daily", "per day", "safely spend", "daily allowance")):
                        assistant_answer = (
                            f"Your calculated safe daily allowance is **₹{safe_daily_allowance:,.0f}** "
                            f"for the remaining **{days_left} days** of this month, based on the budget and spending recorded so far. "
                            "Keep essential bills in mind before treating the full amount as flexible."
                        )

                    elif any(term in question_lower for term in ("most", "highest", "largest", "where am i spending", "top category")):
                        if ranked:
                            share = top_amount / total_spend * 100 if total_spend else 0
                            runner_up = ranked[1] if len(ranked) > 1 else None
                            extra = (
                                f" The next largest category is **{runner_up[0]}** at **₹{runner_up[1]:,.0f}**."
                                if runner_up else ""
                            )
                            assistant_answer = (
                                f"Your highest spending category is **{top_category}** at **₹{top_amount:,.0f}**, "
                                f"which is **{share:.1f}%** of your recorded category spending.{extra}"
                            )
                        else:
                            assistant_answer = "I need expense transactions to identify your highest-spending category."

                    elif any(term in question_lower for term in ("reduce", "save", "cut", "spending less", "spend less")):
                        focus_category = selected_category or top_category
                        focus_amount = category_totals.get(focus_category, 0) if focus_category else 0
                        if focus_category:
                            possible_saving = focus_amount * 0.10
                            assistant_answer = (
                                f"To lower **{focus_category}** spending (currently **₹{focus_amount:,.0f}**), "
                                f"try a 10% reduction first—that would free up about **₹{possible_saving:,.0f}**. "
                                "Choose one practical change: set a weekly cap, compare prices before buying, "
                                "and postpone non-urgent purchases for 24 hours."
                            )
                        else:
                            assistant_answer = "Add a few expense transactions first, and I can identify a realistic area to reduce."

                    elif any(term in question_lower for term in ("goal", "savings target", "on track to reach")):
                        goal = coach_context.get("savings_goal", {})
                        target, saved = goal.get("target"), goal.get("saved")
                        if target is not None and saved is not None:
                            remaining = max(float(target) - float(saved), 0)
                            assistant_answer = (
                                f"Your **{goal.get('name') or 'savings'}** goal is **₹{float(target):,.0f}** "
                                f"and you've saved **₹{float(saved):,.0f}**. You have **₹{remaining:,.0f}** left to reach it."
                            )
                        else:
                            assistant_answer = "You haven't set a savings goal yet. Add a target and current saved amount in Forecast & goals, then ask me again."

                    elif any(term in question_lower for term in ("three habits", "3 habits", "habits i should", "habits should i", "habits to change", "habits can i change")):
                        habits = []
                        if ranked:
                            habits.append(
                                f"**1. Plan for your biggest category ({top_category}).** "
                                f"You recorded ₹{top_amount:,.0f} there; set a weekly limit and review it every Sunday."
                            )
                        eating_out = next((v for k, v in category_totals.items() if k.lower() in ("eating out", "restaurants", "food delivery")), 0)
                        shopping = next((v for k, v in category_totals.items() if k.lower() in ("shopping", "personal shopping")), 0)
                        transport = next((v for k, v in category_totals.items() if k.lower() in ("transport", "travel")), 0)
                        if eating_out:
                            habits.append(
                                f"**2. Reduce impulse food purchases.** You recorded ₹{eating_out:,.0f} on eating out; decide in advance how many café or delivery meals fit your weekly budget."
                            )
                        elif shopping:
                            habits.append(
                                f"**2. Add a 24-hour pause before non-essential shopping.** Your shopping total is ₹{shopping:,.0f}; wishlist items first and buy only what still feels necessary the next day."
                            )
                        elif transport:
                            habits.append(
                                f"**2. Group short trips where practical.** You recorded ₹{transport:,.0f} on transport; plan errands together and compare public transport with individual rides."
                            )
                        else:
                            habits.append(
                                "**2. Record small purchases on the same day.** This makes cash and low-value spending easier to spot before it adds up."
                            )
                        habits.append(
                            "**3. Do a 10-minute weekly money check-in.** Review category totals, upcoming bills and your remaining budget; choose one adjustment for the next week."
                        )
                        assistant_answer = "Based on the transactions currently loaded, here are three habits worth trying:\n\n" + "\n\n".join(habits)

                    elif any(term in question_lower for term in ("summarize my financial health", "summarise my financial health", "financial health", "overall financial", "financial summary")):
                        savings_rate = (balance / income * 100) if income > 0 else None
                        expense_ratio = (expenses / income * 100) if income > 0 else None
                        health_bits = [
                            f"You recorded **₹{income:,.0f} income** and **₹{expenses:,.0f} expenses**, leaving a net balance of **₹{balance:,.0f}** for the selected period."
                        ]
                        if savings_rate is not None:
                            health_bits.append(
                                f"Your net balance is **{savings_rate:.1f}% of recorded income** (expenses use {expense_ratio:.1f}% of income)."
                            )
                        if ranked:
                            health_bits.append(
                                f"Your largest expense category is **{top_category}** at **₹{top_amount:,.0f}**."
                            )
                        if balance < 0:
                            health_bits.append("**Priority:** expenses exceed income, so pause non-essential spending and review recurring costs first.")
                        elif savings_rate is not None and savings_rate >= 20:
                            health_bits.append("**Good sign:** you have a positive surplus. Protect part of it by moving your planned savings aside when income arrives.")
                        else:
                            health_bits.append("**Next step:** keep a small buffer for unexpected costs and set a realistic savings target before discretionary spending.")
                        assistant_answer = "## Your financial health snapshot\n\n" + "\n\n".join(health_bits) + "\n\nThis is based only on the transactions in the selected period, not a full assessment of your finances."

                    else:
                        assistant_answer = (
                            f"Here's your current snapshot: income **₹{income:,.0f}**, expenses "
                            f"**₹{expenses:,.0f}**, and net balance **₹{balance:,.0f}** for the selected period. "
                            "Try asking about your highest category, budget limits, daily allowance, a savings goal, or a percentage-reduction scenario."
                        )

                st.markdown(assistant_answer)
                st.session_state.ai_chat_history.append(
                    {"role": "assistant", "content": assistant_answer}
                )

elif page == "Transactions":
    section_heading("YOUR MONEY LOG", "Transaction history", "Search, filter, and inspect the transactions in your selected analysis period.")
    search_term = st.text_input("Search description or category", placeholder="e.g. groceries, transport...")
    type_filter = st.multiselect("Transaction type", ["Income", "Expense"], default=["Income", "Expense"])

    # The transaction table must follow the same period selected in the sidebar.
    # For Full month, month_df contains every transaction in that selected month.
    period_transactions = month_df.copy()
    category_options = sorted(period_transactions["category"].dropna().unique().tolist())
    category_filter = st.multiselect("Categories", category_options, default=category_options)

    if not period_transactions.empty:
        date_min = period_transactions["date"].min().date()
        date_max = period_transactions["date"].max().date()
        date_range = st.date_input(
            "Date range",
            value=(date_min, date_max),
            min_value=date_min,
            max_value=date_max,
        )
    else:
        date_range = None

    filtered = period_transactions.copy()
    filtered = filtered[filtered["type"].isin(type_filter)]
    filtered = filtered[filtered["category"].isin(category_filter)]
    if search_term.strip():
        pattern = search_term.strip()
        filtered = filtered[
            filtered["description"].str.contains(pattern, case=False, na=False)
            | filtered["category"].str.contains(pattern, case=False, na=False)
        ]
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[(filtered["date"].dt.date >= start_date) & (filtered["date"].dt.date <= end_date)]

    shown = filtered.copy()
    shown["date"] = shown["date"].dt.strftime("%d %b %Y")
    shown["amount"] = shown["amount"].map(rupees)
    shown = shown[["date", "description", "type", "category", "amount", "notes"]]
    shown.columns = ["Date", "Description", "Type", "Category", "Amount", "Notes"]
    st.dataframe(shown, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(filtered)} of {len(period_transactions)} transactions in the selected analysis period.")
    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered transactions as CSV", data=csv_bytes, file_name="pocketpilot_transactions.csv", mime="text/csv")

# ---------- Footer ----------
st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
st.caption(
    "Forecasts are simple estimates based on the transactions provided and may be inaccurate. "
    "No bank or UPI integration is used."
)
