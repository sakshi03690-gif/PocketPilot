from __future__ import annotations

from datetime import date, timedelta
import calendar

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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
    st.markdown("##  PocketPilot")
    st.caption("PLAN  •  TRACK  •  THRIVE")
    st.markdown("---")
    st.markdown("### Your workspace")
    page = st.radio(
        "Navigate",
        ["Overview", "Spending analysis", "Monthly comparison", "Forecast & goals", "Transactions"],
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
sample_rows = [
    (month_start, "Pocket money", "Income", 12000, "Other", "Monthly allowance"),
    (month_start + timedelta(days=1), "Hostel / rent", "Expense", 3500, "Housing", "Fixed"),
    (month_start + timedelta(days=2), "Groceries", "Expense", 650, "Food & groceries", "Variable"),
    (month_start + timedelta(days=3), "Metro / bus", "Expense", 240, "Transport", "Variable"),
    (month_start + timedelta(days=4), "Coffee with friends", "Expense", 180, "Eating out", "Lifestyle"),
    (month_start + timedelta(days=5), "Mobile recharge", "Expense", 299, "Bills & utilities", "Fixed"),
    (month_start + timedelta(days=6), "Online course", "Expense", 4099, "Education", "Growth"),
    (month_start + timedelta(days=7), "Groceries", "Expense", 430, "Food & groceries", "Variable"),
    (month_start + timedelta(days=8), "Cab", "Expense", 210, "Transport", "Variable"),
    (month_start + timedelta(days=9), "Lunch", "Expense", 160, "Eating out", "Lifestyle"),
    (month_start + timedelta(days=10), "Freelance task", "Income", 1800, "Freelance", "Extra income"),
    (month_start + timedelta(days=11), "Stationery", "Expense", 220, "Education", "Study"),
    (month_start + timedelta(days=12), "Movie", "Expense", 350, "Entertainment", "Lifestyle"),
    (month_start + timedelta(days=13), "Electricity share", "Expense", 400, "Bills & utilities", "Fixed"),
    (month_start + timedelta(days=14), "Groceries", "Expense", 520, "Food & groceries", "Variable"),
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

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0).clip(lower=0)
df["type"] = df["type"].astype(str).str.strip().str.title()
df["category"] = df["category"].fillna("Uncategorized").astype(str).str.strip()
df["description"] = df["description"].fillna("Transaction").astype(str)
df["notes"] = df["notes"].fillna("").astype(str)
df = df.dropna(subset=["date"])
df = df[df["type"].isin(["Income", "Expense"])].copy()
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

# Monthly budget and forecast always use the current calendar month's transactions,
# independent of the selected analysis filter above.
current_month_period = pd.Period(today, freq="M")
current_month_df = df[df["date"].dt.to_period("M") == current_month_period].copy()
current_month_income = float(
    current_month_df.loc[current_month_df["type"] == "Income", "amount"].sum()
)
current_month_expenses = float(
    current_month_df.loc[current_month_df["type"] == "Expense", "amount"].sum()
)
current_month_balance = current_month_income - current_month_expenses
budget_left = float(monthly_budget - current_month_expenses)

days_in_month = calendar.monthrange(today.year, today.month)[1]
elapsed_days = max(1, min(today.day, days_in_month))
days_left = max(0, days_in_month - elapsed_days)
daily_expense_rate = current_month_expenses / elapsed_days
forecast_expenses = current_month_expenses + daily_expense_rate * days_left
forecast_balance = current_month_income - forecast_expenses
forecast_budget_overrun = forecast_expenses - monthly_budget

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

    if budget_left < 0:
        st.warning(f"⚠️ This month's spending is {rupees(abs(budget_left))} over your entered monthly budget. Review the forecast and category breakdown below.")
    elif monthly_budget > 0 and current_month_expenses / monthly_budget >= 0.80:
        st.info("👀 You have used at least 80% of this month's budget. Keep an eye on the rest of the month.")
    else:
        st.success("🌱 Every transaction helps you build a clearer picture of your money.")

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
        section_heading("MONTH-END OUTLOOK", "A simple forecast", "Current-month estimate using your average daily spending, regardless of the analysis filter.")
        st.markdown(
            f"""
            <div class="pp-card">
                <div class="pp-card-label">PROJECTED MONTH-END EXPENSES</div>
                <div class="pp-card-value">{rupees(forecast_expenses)}</div>
                <div class="pp-card-note">Based on {rupees(daily_expense_rate)} average spending per day this month.</div>
                <div style="height:14px"></div>
                <div class="pp-card-label">PROJECTED BUDGET POSITION</div>
                <div class="pp-card-value" style="color:{'#B85C50' if forecast_budget_overrun > 0 else '#9B7BFF'}">
                    {rupees(abs(forecast_budget_overrun))} {'over' if forecast_budget_overrun > 0 else 'under'} budget
                </div>
                <div class="pp-card-note">This is a rule-based estimate, not a guarantee.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if forecast_budget_overrun > 0:
            st.warning("Try reducing flexible spending for the rest of the month.")
        else:
            st.success("Your current pace is within the budget you entered.")

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
    f1, f2, f3 = st.columns(3, gap="medium")
    with f1:
        st.metric("SPENT SO FAR", rupees(current_month_expenses), "Current calendar month")
    with f2:
        st.metric("PROJECTED MONTH-END SPEND", rupees(forecast_expenses), "Rule-based estimate")
    with f3:
        st.metric("PROJECTED BALANCE", rupees(forecast_balance))

    if days_left > 0:
        st.caption(f"Estimate uses {rupees(daily_expense_rate)} average daily spending across {elapsed_days} elapsed day(s), with {days_left} day(s) remaining.")
    else:
        st.caption("Forecast is shown as recorded spending for this selection. Choose Month to date to see a current-month projection.")

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

elif page == "Transactions":
    section_heading("YOUR MONEY LOG", "Transaction history", "Search, filter, and inspect the transactions used in your dashboard.")
    search_term = st.text_input("Search description or category", placeholder="e.g. groceries, transport...")
    type_filter = st.multiselect("Transaction type", ["Income", "Expense"], default=["Income", "Expense"])
    category_options = sorted(df["category"].dropna().unique().tolist())
    category_filter = st.multiselect("Categories", category_options, default=category_options)
    date_min = df["date"].min().date() if not df.empty else today
    date_max = df["date"].max().date() if not df.empty else today
    date_range = st.date_input("Date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)

    filtered = df.copy()
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
    st.caption(f"Showing {len(filtered)} of {len(df)} transactions.")
    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered transactions as CSV", data=csv_bytes, file_name="pocketpilot_transactions.csv", mime="text/csv")

# ---------- Footer ----------
st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
st.caption(
    "PocketPilot is an educational prototype, not financial advice. "
    "Forecasts are simple estimates based on the transactions provided and may be inaccurate. "
    "No bank or UPI integration is used."
)
