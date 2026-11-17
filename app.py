
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# MUST BE THE FIRST STREAMLIT COMMAND
# ============================================================

st.set_page_config(
    page_title="Bank AnomalyIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. COLOUR PALETTE
# ============================================================

NAVY = "#061A24"
DARK_BLUE = "#0B3A53"
TEAL = "#0FA3B1"
LIGHT_BLUE = "#B5E2FA"
BACKGROUND = "#F3FAFF"
GREEN = "#22C55E"
WHITE = "#FFFFFF"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

SCORED_DATA_PATH = DATA_DIR / "scored_transactions.csv"
MERCHANT_DATA_PATH = DATA_DIR / "merchant_intelligence.csv"
CHANNEL_DATA_PATH = DATA_DIR / "channel_intelligence.csv"


# ============================================================
# 3. CUSTOM DASHBOARD DESIGN SYSTEM
# ============================================================

st.markdown(
    f"""
    <style>

    /* =========================================
       GLOBAL APPLICATION
    ========================================= */

    .stApp {{
        background-color: {BACKGROUND};
        color: {NAVY};
        font-family: Inter, "Segoe UI", Arial, sans-serif;
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: {BACKGROUND};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1550px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        animation: fadeUp 0.65s ease-out;
    }}

    /* =========================================
       TYPOGRAPHY
    ========================================= */

    h1, h2, h3, h4 {{
        color: {NAVY} !important;
        font-family: Inter, "Segoe UI", Arial, sans-serif !important;
        font-weight: 750 !important;
    }}

    h1 {{
        letter-spacing: -1px;
    }}

    h4 {{
        color: {DARK_BLUE} !important;
    }}

    p, label, li {{
        color: {NAVY};
    }}

    [data-testid="stMarkdownContainer"] p {{
        color: {NAVY};
    }}

    /* =========================================
       SIDEBAR
    ========================================= */

    [data-testid="stSidebar"] {{
        background: linear-gradient(
            165deg,
            {NAVY} 0%,
            {DARK_BLUE} 55%,
            {TEAL} 130%
        );
        border-right: 1px solid rgba(181, 226, 250, 0.15);
    }}

    [data-testid="stSidebar"] > div:first-child {{
        background: transparent;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] label {{
        color: {BACKGROUND} !important;
    }}

    [data-testid="stSidebar"] p {{
        color: {LIGHT_BLUE} !important;
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: {WHITE} !important;
    }}

    [data-testid="stSidebar"] hr {{
        border-color: rgba(181, 226, 250, 0.25);
    }}

    /* Sidebar brand */
    .sidebar-brand {{
        padding: 20px 15px;
        margin-bottom: 15px;
        background: rgba(181, 226, 250, 0.08);
        border: 1px solid rgba(181, 226, 250, 0.15);
        border-radius: 14px;
    }}

    .sidebar-brand-name {{
        font-size: 23px;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: {WHITE};
    }}

    .sidebar-brand-name span {{
        color: {GREEN};
    }}

    .sidebar-brand-caption {{
        margin-top: 5px;
        color: {LIGHT_BLUE};
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.5px;
    }}

    /* Sidebar radio navigation */
    [data-testid="stSidebar"] [role="radiogroup"] {{
        gap: 7px;
    }}

    [data-testid="stSidebar"] [role="radiogroup"] label {{
        background: rgba(181, 226, 250, 0.055);
        border: 1px solid rgba(181, 226, 250, 0.12);
        border-radius: 9px;
        padding: 9px 12px;
        transition: all 0.22s ease;
    }}

    [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
        background: rgba(15, 163, 177, 0.30);
        border-color: {TEAL};
        transform: translateX(3px);
    }}

    [data-testid="stSidebar"] [role="radiogroup"] label:has(
        input:checked
    ) {{
        background: rgba(15, 163, 177, 0.28);
        border-color: {GREEN};
    }}

    /* Sidebar inputs */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background-color: rgba(243, 250, 255, 0.10);
        border-color: rgba(181, 226, 250, 0.35);
        color: {WHITE};
    }}

    [data-testid="stSidebar"] [data-baseweb="select"] input {{
        color: {WHITE};
    }}

    [data-testid="stSidebar"] [data-baseweb="input"] input {{
        color: {NAVY};
    }}

    /* =========================================
       DASHBOARD HERO HEADER
    ========================================= */

    .dashboard-hero {{
        position: relative;
        overflow: hidden;
        padding: 34px 38px;
        margin-bottom: 24px;
        border-radius: 18px;

        background: linear-gradient(
            110deg,
            {NAVY} 0%,
            {DARK_BLUE} 60%,
            {TEAL} 125%
        );

        box-shadow: 0 10px 30px rgba(6, 26, 36, 0.16);
    }}

    .dashboard-hero::after {{
        content: "";
        position: absolute;
        width: 350px;
        height: 350px;
        right: -100px;
        top: -200px;
        border-radius: 50%;

        background: radial-gradient(
            circle,
            rgba(34, 197, 94, 0.32),
            transparent 70%
        );

        animation: heroDrift 7s ease-in-out infinite alternate;
        pointer-events: none;
    }}

    .hero-kicker {{
        position: relative;
        z-index: 1;
        color: {LIGHT_BLUE};
        font-size: 10px;
        font-weight: 750;
        letter-spacing: 2.5px;
        margin-bottom: 12px;
    }}

    .hero-title {{
        position: relative;
        z-index: 1;
        color: {WHITE};
        font-family: Inter, "Segoe UI", Arial, sans-serif;
        font-size: clamp(30px, 4vw, 44px);
        font-weight: 850;
        letter-spacing: -1.7px;
        line-height: 1.15;
        margin-bottom: 9px;
    }}

    .hero-title span {{
        color: {GREEN};
    }}

    .hero-description {{
        position: relative;
        z-index: 1;
        color: {LIGHT_BLUE};
        font-size: 13px;
        max-width: 700px;
        line-height: 1.7;
    }}

    .hero-accent {{
        position: relative;
        z-index: 1;
        width: 55px;
        height: 4px;
        background: {GREEN};
        border-radius: 10px;
        margin-top: 20px;
    }}

    /* =========================================
       ANIMATIONS
    ========================================= */

    @keyframes heroDrift {{
        from {{
            transform: translate(-15px, 0);
        }}

        to {{
            transform: translate(18px, 25px);
        }}
    }}

    @keyframes fadeUp {{
        from {{
            opacity: 0;
            transform: translateY(13px);
        }}

        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes glowPulse {{
        0% {{
            box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.0);
        }}

        50% {{
            box-shadow: 0 0 14px 2px rgba(34, 197, 94, 0.16);
        }}

        100% {{
            box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.0);
        }}
    }}

    /* =========================================
       METRIC CARDS
    ========================================= */

    [data-testid="stMetric"] {{
        background: {WHITE};
        border: 1px solid {LIGHT_BLUE};
        border-radius: 14px;
        padding: 18px 19px;
        box-shadow: 0 4px 14px rgba(6, 26, 36, 0.045);
        transition: all 0.25s ease;
    }}

    [data-testid="stMetric"]:hover {{
        transform: translateY(-4px);
        border-color: {TEAL};
        box-shadow: 0 9px 22px rgba(15, 163, 177, 0.13);
    }}

    [data-testid="stMetricLabel"] {{
        color: {DARK_BLUE} !important;
        font-size: 12px !important;
        font-weight: 700 !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {NAVY} !important;
        font-weight: 850 !important;
    }}

    /* =========================================
       CHART CONTAINERS
    ========================================= */

    [data-testid="stPlotlyChart"] {{
        background: {WHITE};
        border: 1px solid {LIGHT_BLUE};
        border-radius: 15px;
        padding: 9px;
        box-shadow: 0 4px 13px rgba(6, 26, 36, 0.04);
        transition: all 0.25s ease;
    }}

    [data-testid="stPlotlyChart"]:hover {{
        border-color: {TEAL};
        box-shadow: 0 8px 22px rgba(15, 163, 177, 0.10);
    }}

    /* =========================================
       TABLES
    ========================================= */

    [data-testid="stDataFrame"] {{
        background: {WHITE};
        border: 1px solid {LIGHT_BLUE};
        border-radius: 12px;
        overflow: hidden;
    }}

    /* =========================================
       BUTTONS
    ========================================= */

    .stButton button,
    .stDownloadButton button {{
        background: {TEAL};
        color: {WHITE};
        border: 1px solid {TEAL};
        border-radius: 9px;
        font-weight: 700;
        transition: all 0.22s ease;
    }}

    .stButton button:hover,
    .stDownloadButton button:hover {{
        background: {DARK_BLUE};
        border-color: {DARK_BLUE};
        color: {WHITE};
        transform: translateY(-2px);
    }}

    /* =========================================
       EXPANDERS AND ALERTS
    ========================================= */

    [data-testid="stExpander"] {{
        background: {WHITE};
        border: 1px solid {LIGHT_BLUE};
        border-radius: 12px;
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    /* =========================================
       DIVIDERS AND INPUTS
    ========================================= */

    hr {{
        border-color: {LIGHT_BLUE};
    }}

    [data-baseweb="select"] > div {{
        border-radius: 9px;
    }}

    /* Respect reduced motion preferences */
    @media (prefers-reduced-motion: reduce) {{
        *,
        *::before,
        *::after {{
            animation-duration: 0.01ms !important;
            transition-duration: 0.01ms !important;
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. CUSTOM PLOTLY COLOUR THEME
# ============================================================

pio.templates["bank_anomaly_theme"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,

        font=dict(
            family='Inter, "Segoe UI", Arial, sans-serif',
            color=NAVY,
            size=12
        ),

        colorway=[
            TEAL,
            GREEN,
            DARK_BLUE,
            LIGHT_BLUE,
            NAVY
        ],

        margin=dict(
            l=40,
            r=25,
            t=65,
            b=40
        ),

        hoverlabel=dict(
            bgcolor=NAVY,
            font_color=WHITE,
            bordercolor=TEAL
        ),

        xaxis=dict(
            showgrid=False,
            linecolor=LIGHT_BLUE,
            zerolinecolor=LIGHT_BLUE,
            tickfont=dict(color=DARK_BLUE)
        ),

        yaxis=dict(
            gridcolor="#E3F1F8",
            linecolor=LIGHT_BLUE,
            zerolinecolor=LIGHT_BLUE,
            tickfont=dict(color=DARK_BLUE)
        ),

        legend=dict(
            bgcolor="rgba(243,250,255,0.85)",
            bordercolor=LIGHT_BLUE,
            borderwidth=1,
            font=dict(color=NAVY)
        )
    )
)

pio.templates.default = "bank_anomaly_theme"


# ============================================================
# 5. LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    required_files = [
        SCORED_DATA_PATH,
        MERCHANT_DATA_PATH,
        CHANNEL_DATA_PATH
    ]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(
                f"{file_path.name} was not found. "
                "Run the required preparation scripts first."
            )

    transactions = pd.read_csv(SCORED_DATA_PATH)
    merchant_export = pd.read_csv(MERCHANT_DATA_PATH)
    channel_export = pd.read_csv(CHANNEL_DATA_PATH)

    required_columns = [
        "TransactionID",
        "AccountID",
        "MerchantID",
        "Channel",
        "TransactionAmount",
        "TransactionDate",
        "TransactionType",
        "DeviceID",
        "IP Address",
        "TransactionDuration",
        "LoginAttempts",
        "AccountBalance",
        "AnomalyScore",
        "AnomalyFlag"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in transactions.columns
    ]

    if missing_columns:
        raise ValueError(
            f"The scored dataset is missing columns: {missing_columns}"
        )

    transactions["TransactionDate"] = pd.to_datetime(
        transactions["TransactionDate"],
        errors="coerce"
    )

    numeric_columns = [
        "TransactionAmount",
        "TransactionDuration",
        "LoginAttempts",
        "AccountBalance",
        "CustomerAge",
        "AnomalyScore",
        "TransactionHour",
        "TransactionMonth",
        "AmountBalanceRatio",
        "AnomalyPercentile"
    ]

    for column in numeric_columns:
        if column in transactions.columns:
            transactions[column] = pd.to_numeric(
                transactions[column],
                errors="coerce"
            )

    transactions["AnomalyFlag"] = (
        transactions["AnomalyFlag"].astype(str)
    )

    transactions = transactions.dropna(
        subset=["TransactionDate"]
    ).copy()

    return transactions, merchant_export, channel_export


try:
    df, merchant_export, channel_export = load_data()

except Exception as error:
    st.error(f"Unable to load dashboard data: {error}")

    st.info(
        "Check that the required CSV files are available "
        "inside data/processed/."
    )

    st.stop()


if df.empty:
    st.error("The transaction dataset contains no valid records.")
    st.stop()


# ============================================================
# 6. HELPER FUNCTIONS
# ============================================================

def anomaly_count(data):
    return (data["AnomalyFlag"] == "Anomaly").sum()


def anomaly_rate(data):

    if len(data) == 0:
        return 0.0

    return anomaly_count(data) / len(data) * 100


def format_number(value):
    return f"{value:,.0f}"


def format_amount(value):
    return f"{value:,.2f}"


def render_chart(fig, key=None):

    fig.update_layout(
        template="bank_anomaly_theme",
        transition=dict(
            duration=700,
            easing="cubic-in-out"
        ),
        hovermode="closest",
        autosize=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        theme=None,
        config={
            "displayModeBar": False,
            "responsive": True
        },
        key=key
    )


def prepare_channel_summary(data):

    summary = (
        data.groupby("Channel")
        .agg(
            TransactionCount=("TransactionID", "count"),
            UniqueAccounts=("AccountID", "nunique"),
            UniqueMerchants=("MerchantID", "nunique"),
            TotalTransactionValue=("TransactionAmount", "sum"),
            AverageTransactionValue=("TransactionAmount", "mean"),
            MedianTransactionValue=("TransactionAmount", "median"),
            AverageTransactionDuration=("TransactionDuration", "mean"),
            AverageLoginAttempts=("LoginAttempts", "mean"),
            AnomalyCount=(
                "AnomalyFlag",
                lambda x: (x == "Anomaly").sum()
            )
        )
        .reset_index()
    )

    summary["AnomalyRatePct"] = (
        summary["AnomalyCount"] /
        summary["TransactionCount"] * 100
    ).round(2)

    summary["TransactionSharePct"] = (
        summary["TransactionCount"] /
        len(data) * 100
    ).round(2)

    summary["ValueSharePct"] = (
        summary["TotalTransactionValue"] /
        data["TransactionAmount"].sum() * 100
    ).round(2)

    return summary


def prepare_merchant_summary(data):

    summary = (
        data.groupby("MerchantID")
        .agg(
            TransactionCount=("TransactionID", "count"),
            UniqueAccounts=("AccountID", "nunique"),
            TotalTransactionValue=("TransactionAmount", "sum"),
            AverageTransactionValue=("TransactionAmount", "mean"),
            MedianTransactionValue=("TransactionAmount", "median"),
            MaximumTransactionValue=("TransactionAmount", "max"),
            ChannelDiversity=("Channel", "nunique"),
            AnomalyCount=(
                "AnomalyFlag",
                lambda x: (x == "Anomaly").sum()
            ),
            AverageAnomalyScore=("AnomalyScore", "mean")
        )
        .reset_index()
    )

    summary["AnomalyRatePct"] = (
        summary["AnomalyCount"] /
        summary["TransactionCount"] * 100
    ).round(2)

    summary["TransactionSharePct"] = (
        summary["TransactionCount"] /
        len(data) * 100
    ).round(2)

    summary["ReviewEligible"] = (
        summary["TransactionCount"] >= 5
    )

    return summary


# ============================================================
# 7. SIDEBAR AND NAVIGATION
# ============================================================

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="sidebar-brand-name">
            Bank Anomaly<span>IQ</span>
        </div>
        <div class="sidebar-brand-caption">
            TRANSACTION INTELLIGENCE
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "#### Navigation"
)

page = st.sidebar.radio(
    "DASHBOARD NAVIGATION",
    [
        "Executive Overview",
        "Customer Behaviour",
        "Anomaly & Security",
        "Financial & Merchant",
        "Channel & Operations",
        "Insights & Decisions"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

st.sidebar.markdown(
    "#### Dashboard Filters"
)

min_date = df["TransactionDate"].min().date()
max_date = df["TransactionDate"].max().date()

date_range = st.sidebar.date_input(
    "Transaction date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)):

    if len(date_range) == 2:
        start_date, end_date = date_range

    elif len(date_range) == 1:
        start_date = end_date = date_range[0]

    else:
        start_date, end_date = min_date, max_date

else:
    start_date = end_date = date_range


available_channels = sorted(
    df["Channel"].dropna().unique().tolist()
)

selected_channels = st.sidebar.multiselect(
    "Banking channel",
    available_channels,
    default=available_channels
)


available_types = sorted(
    df["TransactionType"].dropna().unique().tolist()
)

selected_types = st.sidebar.multiselect(
    "Transaction type",
    available_types,
    default=available_types
)


# Apply selected filters

filtered = df[
    (df["TransactionDate"].dt.date >= start_date) &
    (df["TransactionDate"].dt.date <= end_date) &
    (df["Channel"].isin(selected_channels)) &
    (df["TransactionType"].isin(selected_types))
].copy()


st.sidebar.divider()

st.sidebar.markdown(
    "#### Data information"
)

st.sidebar.caption(
    "Source: bank_transactions_data_2.csv"
)

st.sidebar.caption(
    "2,512 original transaction records."
)

st.sidebar.caption(
    "Anomalies are investigation indicators, "
    "not confirmed fraud cases."
)


st.sidebar.divider()

st.sidebar.markdown(
    "#### Export analytical data"
)

st.sidebar.download_button(
    "Download merchant analysis",
    merchant_export.to_csv(index=False).encode("utf-8"),
    file_name="merchant_intelligence.csv",
    mime="text/csv"
)

st.sidebar.download_button(
    "Download channel analysis",
    channel_export.to_csv(index=False).encode("utf-8"),
    file_name="channel_intelligence.csv",
    mime="text/csv"
)

# ============================================================
# 8. MAIN DASHBOARD HEADER
# ============================================================

with st.container(border=True):

    st.caption("Anomaly and Fraud detection dashboard for banking transactions.")

    st.title("Bank AnomalyIQ")

    st.write(
        "Transaction monitoring, behavioural intelligence "
        "and analytical decision support using Data & AI."
    )

st.divider()



# ============================================================
# 9. EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.subheader("Executive Overview")

    st.write(
        "A consolidated view of transaction activity, "
        "account behaviour and model-generated anomalies."
    )

    total_transactions = len(filtered)
    total_anomalies = anomaly_count(filtered)
    total_accounts = filtered["AccountID"].nunique()
    total_merchants = filtered["MerchantID"].nunique()
    total_value = filtered["TransactionAmount"].sum()

    rate = anomaly_rate(filtered)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Transactions",
        format_number(total_transactions)
    )

    col2.metric(
        "Flagged anomalies",
        format_number(total_anomalies)
    )

    col3.metric(
        "Anomaly rate",
        f"{rate:.2f}%"
    )

    col4.metric(
        "Accounts analysed",
        format_number(total_accounts)
    )

    col5.metric(
        "Merchants analysed",
        format_number(total_merchants)
    )

    st.divider()

    left, right = st.columns(2)

    # Monthly transaction volume

    with left:

        st.markdown("#### Transaction activity over time")

        monthly = filtered.copy()

        monthly["Month"] = (
            monthly["TransactionDate"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

        monthly_summary = (
            monthly.groupby("Month")
            .size()
            .reset_index(name="Transactions")
        )

        fig = px.line(
            monthly_summary,
            x="Month",
            y="Transactions",
            markers=True,
            title="Monthly Transaction Volume"
        )

        fig.update_traces(
            line=dict(color=TEAL, width=3),
            marker=dict(
                color=GREEN,
                size=8,
                line=dict(color=WHITE, width=2)
            )
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Transactions"
        )

        render_chart(fig, key="executive_monthly_volume")


    # Normal vs anomaly classification

    with right:

        st.markdown("#### Transaction classification")

        status = (
            filtered["AnomalyFlag"]
            .value_counts()
            .rename_axis("Classification")
            .reset_index(name="Transactions")
        )

        fig = px.pie(
            status,
            names="Classification",
            values="Transactions",
            hole=0.58,
            title="Normal vs Flagged Transactions",
            color="Classification",
            color_discrete_map={
                "Normal": LIGHT_BLUE,
                "Anomaly": GREEN
            }
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(
                line=dict(color=WHITE, width=3)
            )
        )

        render_chart(fig, key="executive_classification")


    st.divider()

    left, right = st.columns(2)

    # Channel distribution

    with left:

        st.markdown("#### Transaction distribution by channel")

        channel_summary = prepare_channel_summary(filtered)

        fig = px.bar(
            channel_summary,
            x="Channel",
            y="TransactionCount",
            color="Channel",
            title="Transactions Across Banking Channels",
            color_discrete_map={
                "ATM": TEAL,
                "Branch": GREEN,
                "Online": DARK_BLUE
            }
        )

        fig.update_traces(
            marker_line_width=0,
            hovertemplate=(
                "Channel: %{x}<br>"
                "Transactions: %{y:,}<extra></extra>"
            )
        )

        render_chart(fig, key="executive_channel_distribution")


    # Animated monthly channel chart

    with right:

        st.markdown("#### Monthly channel activity")

        monthly_channel = filtered.copy()

        monthly_channel["Month"] = (
            monthly_channel["TransactionDate"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_channel = (
            monthly_channel.groupby(
                ["Month", "Channel"]
            )
            .size()
            .reset_index(name="Transactions")
        )

        month_order = sorted(
            monthly_channel["Month"].unique()
        )

        max_volume = monthly_channel["Transactions"].max()

        fig = px.bar(
            monthly_channel,
            x="Channel",
            y="Transactions",
            color="Channel",
            animation_frame="Month",
            animation_group="Channel",
            category_orders={
                "Month": month_order,
                "Channel": ["ATM", "Branch", "Online"]
            },
            range_y=[0, max_volume * 1.2],
            title="Channel Activity Over Time",
            color_discrete_map={
                "ATM": TEAL,
                "Branch": GREEN,
                "Online": DARK_BLUE
            }
        )

        fig.update_layout(
            transition=dict(
                duration=750,
                easing="cubic-in-out"
            ),
            xaxis_title="Banking Channel",
            yaxis_title="Transaction Volume"
        )

        render_chart(fig, key="animated_channel_activity")


    st.divider()

    st.markdown("#### Transactions requiring attention")

    top_transactions = (
        filtered.sort_values(
            "AnomalyScore",
            ascending=False
        )
        .head(10)
    )

    display_columns = [
        "TransactionID",
        "AccountID",
        "MerchantID",
        "Channel",
        "TransactionAmount",
        "LoginAttempts",
        "AnomalyScore",
        "AnomalyFlag"
    ]

    st.dataframe(
        top_transactions[display_columns],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Total transaction value in the selected period: "
        f"{format_amount(total_value)} dataset units. "
        "The source dataset does not specify a currency."
    )


# ============================================================
# 10. CUSTOMER BEHAVIOUR INTELLIGENCE
# ============================================================

elif page == "Customer Behaviour":

    st.subheader("Customer Behaviour Intelligence")

    st.write(
        "Understand how accounts transact and identify "
        "behaviour that differs from their observed patterns."
    )


    # --------------------------------------------------------
    # ACCOUNT-LEVEL BEHAVIOURAL SUMMARY
    # --------------------------------------------------------

    account_summary = (
        filtered.groupby("AccountID")
        .agg(
            TransactionCount=("TransactionID", "count"),

            AverageTransaction=("TransactionAmount", "mean"),

            MaximumTransaction=("TransactionAmount", "max"),

            UniqueDevices=("DeviceID", "nunique"),

            UniqueIPs=("IP Address", "nunique"),

            AnomalyCount=(
                "AnomalyFlag",
                lambda x: (x == "Anomaly").sum()
            ),

            HighestAnomalyScore=("AnomalyScore", "max")
        )
        .reset_index()
    )

    account_summary["AnomalyRatePct"] = (
        account_summary["AnomalyCount"] /
        account_summary["TransactionCount"] * 100
    ).round(2)


    # --------------------------------------------------------
    # IDENTIFY FLAGGED TRANSACTIONS BY ACCOUNT
    # --------------------------------------------------------

    flagged_transaction_rows = filtered[
        filtered["AnomalyFlag"] == "Anomaly"
    ].copy()

    if not flagged_transaction_rows.empty:

        flagged_details = (
            flagged_transaction_rows.groupby("AccountID")
            .agg(
                FlaggedTransactionIDs=(
                    "TransactionID",
                    lambda x: ", ".join(x.astype(str))
                ),

                LastFlaggedTransaction=(
                    "TransactionDate",
                    "max"
                )
            )
            .reset_index()
        )

        account_summary = account_summary.merge(
            flagged_details,
            on="AccountID",
            how="left"
        )

    else:

        account_summary["FlaggedTransactionIDs"] = ""

        account_summary["LastFlaggedTransaction"] = pd.NaT


    # --------------------------------------------------------
    # ACCOUNT OVERVIEW METRICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Active accounts",
        format_number(len(account_summary))
    )

    col2.metric(
        "Accounts with flagged activity",
        format_number(
            (account_summary["AnomalyCount"] > 0).sum()
        )
    )

    col3.metric(
        "Accounts using multiple devices",
        format_number(
            (account_summary["UniqueDevices"] > 1).sum()
        )
    )


    st.divider()


    # --------------------------------------------------------
    # ACCOUNTS WITH DETECTED ANOMALIES
    # --------------------------------------------------------

    st.markdown("### Accounts with Detected Anomalies")

    st.caption(
        "Accounts with one or more transactions flagged "
        "by the Isolation Forest model."
    )

    flagged_accounts = account_summary[
        account_summary["AnomalyCount"] > 0
    ].copy()

    flagged_accounts = flagged_accounts.sort_values(
        [
            "AnomalyCount",
            "AnomalyRatePct",
            "HighestAnomalyScore"
        ],
        ascending=[False, False, False]
    )

    if not flagged_accounts.empty:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Accounts requiring review",
            format_number(len(flagged_accounts))
        )

        col2.metric(
            "Flagged transactions",
            format_number(
                flagged_accounts["AnomalyCount"].sum()
            )
        )

        col3.metric(
            "Highest account anomaly rate",
            f"{flagged_accounts['AnomalyRatePct'].max():.2f}%"
        )

        account_table_columns = [
            "AccountID",
            "TransactionCount",
            "AnomalyCount",
            "AnomalyRatePct",
            "AverageTransaction",
            "UniqueDevices",
            "UniqueIPs",
            "HighestAnomalyScore",
            "LastFlaggedTransaction",
            "FlaggedTransactionIDs"
        ]

        st.dataframe(
            flagged_accounts[account_table_columns],
            use_container_width=True,
            hide_index=True,
            column_config={
                "AccountID": st.column_config.TextColumn(
                    "Account ID"
                ),
                "TransactionCount": st.column_config.NumberColumn(
                    "Total Transactions",
                    format="%d"
                ),
                "AnomalyCount": st.column_config.NumberColumn(
                    "Flagged Transactions",
                    format="%d"
                ),
                "AnomalyRatePct": st.column_config.NumberColumn(
                    "Anomaly Rate",
                    format="%.2f%%"
                ),
                "AverageTransaction": st.column_config.NumberColumn(
                    "Average Transaction",
                    format="%.2f"
                ),
                "HighestAnomalyScore": st.column_config.NumberColumn(
                    "Highest Anomaly Score",
                    format="%.4f"
                ),
                "LastFlaggedTransaction": st.column_config.DatetimeColumn(
                    "Most Recent Flagged Transaction",
                    format="YYYY-MM-DD HH:mm"
                ),
                "FlaggedTransactionIDs": st.column_config.TextColumn(
                    "Flagged Transaction IDs",
                    width="large"
                )
            }
        )

        st.download_button(
            "Download accounts with detected anomalies",
            flagged_accounts.to_csv(index=False).encode("utf-8"),
            file_name="accounts_with_detected_anomalies.csv",
            mime="text/csv"
        )

        st.info(
            "These accounts have transactions that the model "
            "considers unusual. They are prioritised for review; "
            "they are not automatically classified as fraudulent."
        )

    else:

        st.success(
            "No accounts with flagged transactions were found "
            "under the current filters."
        )


    st.divider()


    # --------------------------------------------------------
    # ACCOUNT BEHAVIOURAL VISUALISATIONS
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown("#### Most active accounts")

        top_accounts = (
            account_summary
            .nlargest(10, "TransactionCount")
        )

        fig = px.bar(
            top_accounts,
            x="AccountID",
            y="TransactionCount",
            title="Top 10 Accounts by Transaction Volume",
            color_discrete_sequence=[TEAL]
        )

        fig.update_traces(
            marker_line_width=0
        )

        render_chart(fig, key="customer_active_accounts")


    with right:

        st.markdown("#### Account anomaly concentrations")

        risky_accounts = (
            account_summary[
                (account_summary["TransactionCount"] >= 3) &
                (account_summary["AnomalyCount"] > 0)
            ]
            .sort_values(
                "AnomalyRatePct",
                ascending=False
            )
            .head(10)
        )

        if not risky_accounts.empty:

            fig = px.bar(
                risky_accounts,
                x="AccountID",
                y="AnomalyRatePct",
                title="Accounts with Highest Anomaly Rates",
                color_discrete_sequence=[GREEN]
            )

            fig.update_layout(
                yaxis_title="Anomaly rate (%)"
            )

            render_chart(fig, key="customer_anomaly_rates")

        else:

            st.info(
                "No accounts meet the minimum activity "
                "threshold with flagged transactions."
            )


    st.divider()


    # --------------------------------------------------------
    # INDIVIDUAL ACCOUNT INVESTIGATION
    # --------------------------------------------------------

    st.markdown("### Investigate an Individual Account")

    st.caption(
        "Accounts with detected anomalies are prioritised "
        "in the selector."
    )

    all_account_ids = sorted(
        filtered["AccountID"].dropna().unique().tolist()
    )

    flagged_account_ids = (
        flagged_accounts["AccountID"].dropna().tolist()
    )

    other_account_ids = [
        account for account in all_account_ids
        if account not in flagged_account_ids
    ]

    # Place accounts with anomalies first
    account_ids = flagged_account_ids + other_account_ids

    selected_account = st.selectbox(
        "Select account",
        account_ids,
        format_func=lambda account: (
            f"{account}  •  FLAGGED"
            if account in flagged_account_ids
            else account
        )
    )

    account_data = filtered[
        filtered["AccountID"] == selected_account
    ].sort_values("TransactionDate")

    account_info = account_summary[
        account_summary["AccountID"] == selected_account
    ].iloc[0]


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Transactions",
        int(account_info["TransactionCount"])
    )

    col2.metric(
        "Average transaction",
        format_amount(account_info["AverageTransaction"])
    )

    col3.metric(
        "Devices",
        int(account_info["UniqueDevices"])
    )

    col4.metric(
        "Flagged transactions",
        int(account_info["AnomalyCount"])
    )


    fig = px.scatter(
        account_data,
        x="TransactionDate",
        y="TransactionAmount",
        color="AnomalyFlag",
        hover_data=[
            "TransactionID",
            "Channel",
            "MerchantID"
        ],
        title=f"Transaction Behaviour: {selected_account}",
        color_discrete_map={
            "Normal": TEAL,
            "Anomaly": GREEN
        }
    )

    fig.update_traces(
        marker=dict(
            size=11,
            line=dict(color=WHITE, width=1)
        )
    )

    render_chart(fig, key="individual_account_behaviour")


    st.markdown("#### Account Transaction History")

    st.dataframe(
        account_data[
            [
                "TransactionID",
                "TransactionDate",
                "TransactionAmount",
                "TransactionType",
                "Channel",
                "MerchantID",
                "AnomalyScore",
                "AnomalyFlag"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # --------------------------------------------------------
    # DEVICE AND IP RELATIONSHIPS
    # --------------------------------------------------------

    st.markdown("### Device and IP Relationships")

    device_accounts = (
        filtered.groupby("DeviceID")["AccountID"]
        .nunique()
        .reset_index(name="AssociatedAccounts")
    )

    shared_devices = device_accounts[
        device_accounts["AssociatedAccounts"] > 1
    ]

    ip_accounts = (
        filtered.groupby("IP Address")["AccountID"]
        .nunique()
        .reset_index(name="AssociatedAccounts")
    )

    shared_ips = ip_accounts[
        ip_accounts["AssociatedAccounts"] > 1
    ]

    col1, col2 = st.columns(2)

    col1.metric(
        "Devices associated with multiple accounts",
        len(shared_devices)
    )

    col2.metric(
        "IP addresses associated with multiple accounts",
        len(shared_ips)
    )

    left, right = st.columns(2)

    with left:

        st.markdown("#### Shared devices")

        st.dataframe(
            shared_devices.sort_values(
                "AssociatedAccounts",
                ascending=False
            ).head(10),
            use_container_width=True,
            hide_index=True
        )

    with right:

        st.markdown("#### Shared IP addresses")

        st.dataframe(
            shared_ips.sort_values(
                "AssociatedAccounts",
                ascending=False
            ).head(10),
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "Shared devices and IP addresses can have legitimate "
        "explanations. They are not automatically suspicious."
    )


# ============================================================
# 11. ANOMALY AND SECURITY MONITORING
# ============================================================

elif page == "Anomaly & Security":

    st.subheader("Anomaly & Security Monitoring")

    st.write(
        "Explore model-generated anomalies and the transaction "
        "characteristics that may warrant further investigation."
    )

    anomalies = filtered[
        filtered["AnomalyFlag"] == "Anomaly"
    ].copy()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Flagged transactions",
        len(anomalies)
    )

    col2.metric(
        "Anomaly rate",
        f"{anomaly_rate(filtered):.2f}%"
    )

    col3.metric(
        "Accounts with anomalies",
        anomalies["AccountID"].nunique()
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.markdown("#### Transaction amount vs anomaly score")

        fig = px.scatter(
            filtered,
            x="TransactionAmount",
            y="AnomalyScore",
            color="AnomalyFlag",
            hover_data=[
                "TransactionID",
                "AccountID",
                "Channel",
                "MerchantID"
            ],
            title="Transaction Anomaly Distribution",
            color_discrete_map={
                "Normal": TEAL,
                "Anomaly": GREEN
            }
        )

        render_chart(fig, key="security_anomaly_scatter")


    with right:

        st.markdown("#### Authentication behaviour")

        login_summary = (
            filtered.groupby("LoginAttempts")
            .agg(
                TransactionCount=("TransactionID", "count"),
                AnomalyCount=(
                    "AnomalyFlag",
                    lambda x: (x == "Anomaly").sum()
                )
            )
            .reset_index()
        )

        login_summary["AnomalyRatePct"] = (
            login_summary["AnomalyCount"] /
            login_summary["TransactionCount"] * 100
        )

        fig = px.bar(
            login_summary,
            x="LoginAttempts",
            y="AnomalyRatePct",
            hover_data=[
                "TransactionCount",
                "AnomalyCount"
            ],
            title="Anomaly Rate by Number of Login Attempts",
            color_discrete_sequence=[GREEN]
        )

        fig.update_layout(
            yaxis_title="Anomaly rate (%)"
        )

        render_chart(fig, key="security_login_attempts")


    st.divider()

    st.markdown("#### Highest anomaly scores")

    top_anomalies = (
        anomalies.sort_values(
            "AnomalyScore",
            ascending=False
        )
        .head(25)
    )

    st.dataframe(
        top_anomalies[
            [
                "TransactionID",
                "AccountID",
                "TransactionDate",
                "TransactionAmount",
                "TransactionType",
                "Channel",
                "LoginAttempts",
                "AnomalyScore",
                "AnomalyPercentile"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download flagged transactions",
        anomalies.to_csv(index=False).encode("utf-8"),
        file_name="flagged_transactions.csv",
        mime="text/csv"
    )

    st.info(
        "Anomaly scores indicate relative unusualness under "
        "the trained model. They are not probabilities of fraud "
        "and do not confirm malicious activity."
    )


# ============================================================
# 12. FINANCIAL AND MERCHANT INTELLIGENCE
# ============================================================

elif page == "Financial & Merchant":

    st.subheader("Financial & Merchant Intelligence")

    st.write(
        "Examine transaction values and identify merchants "
        "with higher concentrations of model-flagged activity."
    )

    merchant_summary = prepare_merchant_summary(filtered)

    total_value = filtered["TransactionAmount"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total transaction value",
        format_amount(total_value)
    )

    col2.metric(
        "Merchants analysed",
        filtered["MerchantID"].nunique()
    )

    col3.metric(
        "Merchants with flagged transactions",
        merchant_summary[
            merchant_summary["AnomalyCount"] > 0
        ].shape[0]
    )

    st.caption(
        "Transaction values are shown in dataset units; "
        "the source does not specify a currency."
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.markdown("#### Highest merchant anomaly rates")

        eligible_merchants = merchant_summary[
            merchant_summary["ReviewEligible"]
        ].copy()

        top_merchants = (
            eligible_merchants
            .sort_values(
                ["AnomalyRatePct", "TransactionCount"],
                ascending=[False, False]
            )
            .head(10)
        )

        if not top_merchants.empty:

            fig = px.bar(
                top_merchants,
                x="MerchantID",
                y="AnomalyRatePct",
                hover_data=[
                    "TransactionCount",
                    "AnomalyCount",
                    "UniqueAccounts"
                ],
                title="Merchant Anomaly Rates (Minimum 5 Transactions)",
                color_discrete_sequence=[GREEN]
            )

            fig.update_layout(
                yaxis_title="Anomaly rate (%)"
            )

            render_chart(fig, key="merchant_anomaly_rates")

        else:

            st.info("No merchants meet the minimum transaction threshold.")


    with right:

        st.markdown("#### Merchant transaction volume")

        top_volume = (
            merchant_summary
            .nlargest(10, "TransactionCount")
        )

        fig = px.bar(
            top_volume,
            x="MerchantID",
            y="TransactionCount",
            title="Top 10 Merchants by Transaction Volume",
            color_discrete_sequence=[TEAL]
        )

        render_chart(fig, key="merchant_transaction_volume")


    st.divider()

    st.markdown("#### Merchant investigation table")

    st.dataframe(
        merchant_summary.sort_values(
            ["AnomalyRatePct", "AnomalyCount"],
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download filtered merchant analysis",
        merchant_summary.to_csv(index=False).encode("utf-8"),
        file_name="filtered_merchant_intelligence.csv",
        mime="text/csv"
    )


    st.divider()

    st.markdown("#### Transaction-to-balance exposure")

    if "AmountBalanceRatio" in filtered.columns:

        exposure = filtered[
            [
                "TransactionID",
                "AccountID",
                "TransactionAmount",
                "AccountBalance",
                "AmountBalanceRatio",
                "AnomalyFlag"
            ]
        ].copy()

        exposure = exposure.replace(
            [np.inf, -np.inf],
            np.nan
        ).dropna(subset=["AmountBalanceRatio"])

        if not exposure.empty:

            exposure = exposure.sort_values(
                "AmountBalanceRatio",
                ascending=False
            ).head(15)

            st.dataframe(
                exposure,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No valid transaction-to-balance ratios are available.")

    st.caption(
        "The ratio compares the recorded transaction amount "
        "with the recorded account balance. It does not establish "
        "the amount of money remaining in an account."
    )


# ============================================================
# 13. CHANNEL AND OPERATIONAL ANALYTICS
# ============================================================

elif page == "Channel & Operations":

    st.subheader("Channel & Operational Analytics")

    st.write(
        "Compare transaction activity, operational characteristics "
        "and model-generated anomaly concentrations across channels."
    )

    channel_summary = prepare_channel_summary(filtered)

    left, right = st.columns(2)

    with left:

        st.markdown("#### Transaction volume by channel")

        fig = px.bar(
            channel_summary,
            x="Channel",
            y="TransactionCount",
            color="Channel",
            title="Channel Transaction Volumes",
            color_discrete_map={
                "ATM": TEAL,
                "Branch": GREEN,
                "Online": DARK_BLUE
            }
        )

        render_chart(fig, key="channel_transaction_volume")


    with right:

        st.markdown("#### Channel anomaly rates")

        fig = px.bar(
            channel_summary,
            x="Channel",
            y="AnomalyRatePct",
            color="Channel",
            title="Anomaly Rate by Channel",
            color_discrete_map={
                "ATM": TEAL,
                "Branch": GREEN,
                "Online": DARK_BLUE
            }
        )

        fig.update_layout(
            yaxis_title="Anomaly rate (%)"
        )

        render_chart(fig, key="channel_anomaly_rate")


    st.divider()

    left, right = st.columns(2)

    with left:

        st.markdown("#### Average transaction value")

        fig = px.bar(
            channel_summary,
            x="Channel",
            y="AverageTransactionValue",
            color="Channel",
            title="Average Transaction Value by Channel",
            color_discrete_map={
                "ATM": TEAL,
                "Branch": GREEN,
                "Online": DARK_BLUE
            }
        )

        render_chart(fig, key="channel_average_value")


    with right:

        st.markdown("#### Average transaction duration")

        fig = px.bar(
            channel_summary,
            x="Channel",
            y="AverageTransactionDuration",
            color="Channel",
            title="Average Transaction Duration by Channel",
            color_discrete_map={
                "ATM": TEAL,
                "Branch": GREEN,
                "Online": DARK_BLUE
            }
        )

        render_chart(fig, key="channel_transaction_duration")


    st.divider()

    st.markdown("#### Channel performance table")

    st.dataframe(
        channel_summary,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download filtered channel analysis",
        channel_summary.to_csv(index=False).encode("utf-8"),
        file_name="filtered_channel_intelligence.csv",
        mime="text/csv"
    )

    st.info(
        "The source dataset contains Branch, ATM and Online "
        "channels only. Mobile banking, USSD, agent banking "
        "and mobile money integrations are potential future "
        "extensions, not analysed channels in this prototype."
    )


# ============================================================
# 14. INSIGHTS AND DECISION SUPPORT
# ============================================================

elif page == "Insights & Decisions":

    st.subheader("Insights & Decision Support")

    st.write(
        "Translate analytical results into practical investigation "
        "priorities and potential banking decisions."
    )

    overall_rate = anomaly_rate(filtered)

    channel_summary = prepare_channel_summary(filtered)
    merchant_summary = prepare_merchant_summary(filtered)

    st.markdown("### Key analytical findings")


    # --------------------------------------------------------
    # FINDING 1: CHANNEL ANOMALY CONCENTRATION
    # --------------------------------------------------------

    if not channel_summary.empty:

        highest_channel = channel_summary.sort_values(
            "AnomalyRatePct",
            ascending=False
        ).iloc[0]

        st.markdown("#### 1. Channel anomaly concentration")

        st.write(
            f"**{highest_channel['Channel']}** has the highest "
            f"observed anomaly rate at "
            f"**{highest_channel['AnomalyRatePct']:.2f}%**, "
            f"compared with an overall filtered rate of "
            f"{overall_rate:.2f}%."
        )

        st.write(
            "This channel may warrant closer review of its "
            "transaction patterns and security controls."
        )


    # --------------------------------------------------------
    # FINDING 2: MERCHANT ANOMALY CONCENTRATION
    # --------------------------------------------------------

    eligible_merchants = merchant_summary[
        merchant_summary["TransactionCount"] >= 10
    ]

    if not eligible_merchants.empty:

        highest_merchant = eligible_merchants.sort_values(
            "AnomalyRatePct",
            ascending=False
        ).iloc[0]

        st.markdown("#### 2. Merchant anomaly concentration")

        st.write(
            f"**{highest_merchant['MerchantID']}** has an "
            f"anomaly rate of "
            f"**{highest_merchant['AnomalyRatePct']:.2f}%**, "
            f"across {int(highest_merchant['TransactionCount'])} "
            f"transactions."
        )

        st.write(
            "This merchant should be prioritised for transaction "
            "review, while considering transaction volume and "
            "customer context."
        )


    # --------------------------------------------------------
    # FINDING 3: SHARED DEVICE ACTIVITY
    # --------------------------------------------------------

    device_accounts = (
        filtered.groupby("DeviceID")["AccountID"]
        .nunique()
    )

    shared_device_count = (
        device_accounts > 1
    ).sum()

    st.markdown("#### 3. Shared-device activity")

    st.write(
        f"The filtered dataset contains **{shared_device_count} "
        "devices** associated with more than one account."
    )

    st.write(
        "Shared-device activity can be legitimate, but unusual "
        "combinations of shared devices, unfamiliar access "
        "patterns and high anomaly scores could warrant review."
    )


    # --------------------------------------------------------
    # FINDING 4: AUTHENTICATION PATTERNS
    # --------------------------------------------------------

    multiple_attempts = filtered[
        filtered["LoginAttempts"] > 1
    ]

    st.markdown("#### 4. Authentication patterns")

    st.write(
        f"**{len(multiple_attempts)} transactions** have more "
        "than one recorded login attempt."
    )

    st.write(
        "These records can be compared with device changes "
        "and anomaly scores. The dataset does not indicate "
        "whether login attempts were successful or failed."
    )


    st.divider()

    st.markdown("### Recommended banking actions")

    recommendations = [
        (
            "Prioritise investigation",
            "Review high-scoring transactions and merchants with "
            "higher anomaly concentrations. Use human review before "
            "taking action against an account or merchant."
        ),

        (
            "Strengthen channel monitoring",
            "Investigate why certain channels exhibit higher "
            "anomaly rates. Consider additional monitoring and "
            "verification controls where justified."
        ),

        (
            "Build customer behavioural baselines",
            "Use account-level transaction history to identify "
            "changes in spending, access devices and transaction "
            "frequency."
        ),

        (
            "Improve identity and device intelligence",
            "In a real banking deployment, enrich the analysis "
            "with verified device histories, authentication outcomes "
            "and appropriately protected access records."
        ),

        (
            "Introduce analyst feedback",
            "Record whether reviewed alerts are legitimate or "
            "suspicious. This can create labelled data for future "
            "supervised fraud detection models."
        )
    ]

    for title, description in recommendations:

        with st.expander(title):
            st.write(description)


    st.divider()

    st.markdown("### Limitations and interpretation")

    st.warning(
        """
        This prototype uses unsupervised anomaly detection.

        • An anomaly is not confirmed fraud.

        • The dataset contains no confirmed fraud labels.

        • Merchant IDs do not identify actual merchant names.

        • The source currency is unspecified.

        • Branch, ATM and Online are the only observed channels.

        • PreviousTransactionDate contains inconsistent chronology
          and has not been used as a historical feature.

        • Findings describe this dataset and should not be treated
          as measured performance of Kenyan banks.
        """
    )


    st.markdown(
        "### Future development for Kenyan financial institutions"
    )

    st.write(
        """
        A future version could integrate appropriately governed
        mobile banking, USSD, agency banking, card and mobile money
        transaction data. It could also incorporate transaction
        outcomes, authentication results, verified customer
        information and analyst-confirmed investigation results.
        """
    )


# ============================================================
# 15. FOOTER
# ============================================================

st.divider()

st.markdown(
    f"""
    <div style="
        padding: 12px 0;
        color: {DARK_BLUE};
        font-size: 11px;
        text-align: center;
        letter-spacing: 0.4px;
    ">
        <strong style="color: {NAVY};">Bank AnomalyIQ</strong>
        &nbsp; | &nbsp;
        Transaction Intelligence & Behavioural Analytics
        &nbsp; | &nbsp;
        Assessment Prototype
    </div>
    """,
    unsafe_allow_html=True
)
