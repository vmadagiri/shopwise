
"""Customer Analytics dashboard powered by UCI Online Retail transactions."""

import streamlit as st
import plotly.express as px

from analytics import country_performance, monthly_sales, summarize_sales
from shared import page_header


st.set_page_config(
    page_title="Online Retail | Customer Analytics",
    page_icon="🛍️",
    layout="wide",
)

# --------------------------------------------------
# Dashboard theme
# --------------------------------------------------

NAVY = "#20243A"
PURPLE = "#7664D8"
TEAL = "#279E98"
BACKGROUND = "#F7F6FC"
MUTED = "#657087"

st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background-color: #F7F6FC;
        color: #20243A;
    }

    [data-testid="stMainBlockContainer"] {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* Headings */
    .stApp h1,
    .stApp h2,
    .stApp h3 {
        color: #20243A !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    .stApp h1 {
        font-size: 2.4rem;
    }

    /* Main page text */
    [data-testid="stMain"] p,
    [data-testid="stMain"] label {
        color: #657087;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E8E5F2;
    }

    [data-testid="stSidebar"] * {
        color: #20243A;
    }

    [data-testid="stSidebar"] a {
        color: #5142A0 !important;
    }

    [data-testid="stSidebar"] a[aria-current="page"] {
        color: #20243A !important;
        font-weight: 700;
    }

    /* Sidebar inputs */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] [data-baseweb="select"],
    [data-testid="stSidebar"] [data-baseweb="input"] {
        background-color: #F7F6FC;
        color: #20243A;
        border-radius: 9px;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 22px 18px;
        border-radius: 16px;
        border: 1px solid #E8E5F2;
        box-shadow: 0 3px 12px rgba(40, 35, 90, 0.04);
    }

    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricLabel"] {
        color: #657087 !important;
        font-size: 0.88rem;
        font-weight: 500;
    }

    [data-testid="stMetricValue"] *,
    [data-testid="stMetricValue"] {
        color: #20243A !important;
        font-weight: 700;
    }

    /* Info message */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Dividers */
    hr {
        border-color: #E8E5F2;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Load dashboard data and filters
# --------------------------------------------------

transactions = page_header(
    "🛍️ Online Retail Analytics",
    "Explore real shopping transactions, customer behavior, and sales trends using the UCI Online Retail dataset.",
)

if transactions.empty:
    st.warning(
        "No transactions match your filters. "
        "Try a wider date range or different selections."
    )
    st.stop()

# --------------------------------------------------
# KPI overview
# --------------------------------------------------

st.markdown("### Sales at a glance")

kpis = summarize_sales(transactions)

first, second, third, fourth, fifth = st.columns(5)

first.metric("Total Revenue", f"£{kpis['revenue_gbp']:,.0f}")
second.metric("Unique Orders", f"{kpis['unique_invoices']:,}")
third.metric(
    "Average Order Value",
    f"£{kpis['average_order_value_gbp']:,.2f}",
)
fourth.metric("Customers", f"{kpis['customers']:,}")
fifth.metric(
    "Repeat Purchase Rate",
    f"{kpis['repeat_purchase_rate_pct']:.1f}%",
)

st.caption(
    "Orders are counted using unique invoice numbers. "
    "Repeat purchase rate represents customers with two or more "
    "distinct invoices within the selected filters."
)

st.write("")

# --------------------------------------------------
# Consistent Plotly chart styling
# --------------------------------------------------

def style_chart(fig):
    """Apply a consistent light theme to Plotly charts."""

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial, sans-serif",
            color=NAVY,
            size=12,
        ),
        title=dict(
            font=dict(size=16, color=NAVY),
            x=0.03,
        ),
        margin=dict(l=30, r=25, t=65, b=35),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_color=NAVY,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#E8E5F2",
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )

    fig.update_yaxes(
        gridcolor="#EEEAF5",
        zeroline=False,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )

    return fig


# --------------------------------------------------
# Sales and country charts
# --------------------------------------------------

left, right = st.columns([1.6, 1], gap="large")

with left:
    st.subheader("Monthly Sales Trend")

    by_month = monthly_sales(transactions)

    fig = px.line(
        by_month,
        x="Month",
        y="Revenue",
        markers=True,
        title="Revenue by Month",
    )

    fig.update_traces(
        line_color=PURPLE,
        line_width=3,
        marker=dict(size=8, color=PURPLE),
        hovertemplate=(
            "%{x|%b %Y}<br>"
            "Revenue: £%{y:,.2f}<extra></extra>"
        ),
    )

    fig.update_layout(
        yaxis_title="Revenue (£)",
        xaxis_title="",
        hovermode="x unified",
    )

    fig = style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)


with right:
    st.subheader("Top Countries")

    countries = (
        country_performance(transactions)
        .head(10)
        .sort_values("RevenueGBP")
    )

    fig = px.bar(
        countries,
        x="RevenueGBP",
        y="Country",
        orientation="h",
        title="Revenue by Country",
    )

    fig.update_traces(
        marker_color=TEAL,
        marker_line_width=0,
        hovertemplate=(
            "%{y}<br>"
            "Revenue: £%{x:,.2f}<extra></extra>"
        ),
    )

    fig.update_layout(
        xaxis_title="Revenue (£)",
        yaxis_title="",
        bargap=0.35,
    )

    fig = style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# Dataset context
# --------------------------------------------------

st.info(
    "**About this analysis:** These results come from the real "
    "UCI Online Retail dataset after applying the documented "
    "cleaning rules. Revenue represents sales, not profit. "
    "The dataset does not include website behavior or marketing exposure."
)

st.caption(
    "Data source: UCI Machine Learning Repository | "
    "Online Retail Dataset | December 2010 – December 2011"
)
