
"""Interactive analytics dashboard using real UCI Online Retail data."""

import streamlit as st
import plotly.express as px

from analytics import (
    country_performance,
    monthly_sales,
    summarize_sales,
    customer_rfm,
    product_performance,
    cohort_retention,
)
from shared import page_header


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Online Retail | Customer Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Theme colors
# --------------------------------------------------

NAVY = "#20243A"
PURPLE = "#7664D8"
TEAL = "#279E98"
MUTED = "#657087"

PALETTE = [
    "#7664D8",
    "#279E98",
    "#A38BE8",
    "#59B9AF",
    "#E4A0C0",
    "#6379B7",
    "#D5A45F",
]

# --------------------------------------------------
# Consistent light-mode theme
# --------------------------------------------------

st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
    }

    .stApp,
    [data-testid="stMain"],
    [data-testid="stHeader"] {
        background-color: #F7F6FC !important;
        color: #20243A !important;
    }

    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3 {
        color: #20243A !important;
        font-weight: 700;
        letter-spacing: -0.4px;
    }

    [data-testid="stMain"] h1 {
        font-size: 2.3rem;
    }

    [data-testid="stMain"] p,
    [data-testid="stMain"] label,
    [data-testid="stMain"] [data-testid="stCaptionContainer"] {
        color: #657087;
    }

    /* Sidebar */
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {
        background-color: #FFFFFF !important;
        border-right-color: #E8E5F2;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #20243A;
    }

    [data-testid="stSidebar"] a {
        color: #5142A0 !important;
    }

    [data-testid="stSidebar"] a[aria-current="page"] {
        font-weight: 700;
    }

    /* Sidebar input containers */
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="input"] > div {
        background-color: #F7F6FC !important;
        border: 1px solid #E8E5F2 !important;
        border-radius: 9px !important;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #20243A !important;
        -webkit-text-fill-color: #20243A !important;
        background: transparent !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #20243A !important;
    }

    [data-testid="stSidebar"] svg {
        color: #657087 !important;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 18px 14px;
        border-radius: 16px;
        border: 1px solid #E8E5F2;
        box-shadow: 0 3px 12px rgba(40, 35, 90, 0.04);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #657087 !important;
        font-size: 0.85rem;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #20243A !important;
        font-size: clamp(1.3rem, 2vw, 2rem);
        font-weight: 700;
    }

    /* Tabs */
    [data-testid="stTabs"] [role="tablist"] {
        gap: 12px;
    }

    [data-testid="stTabs"] button[role="tab"] {
        color: #657087;
        font-weight: 600;
    }

    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #7664D8 !important;
        border-bottom-color: #7664D8 !important;
    }

    /* Tables and messages */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: #E8E5F2;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Shared chart styling
# --------------------------------------------------

def style_chart(fig, height=420):
    """Use consistent light styling for every Plotly chart."""

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=height,
        font=dict(
            family="Arial, sans-serif",
            color=NAVY,
            size=12,
        ),
        title=dict(
            font=dict(size=16, color=NAVY),
            x=0.03,
        ),
        margin=dict(l=35, r=30, t=65, b=45),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_color=NAVY,
        ),
        colorway=PALETTE,
    )

    fig.update_xaxes(
        gridcolor="#EEEAF5",
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
# Load real UCI transactions
# --------------------------------------------------

transactions = page_header(
    "🛍️ Online Retail Analytics",
    "Explore real shopping transactions, customer behavior, "
    "product performance, and retention using UCI Online Retail data.",
)

if transactions.empty:
    st.warning(
        "No transactions match your filters. "
        "Try changing the date, country, or product."
    )
    st.stop()


# --------------------------------------------------
# Dashboard navigation
# --------------------------------------------------

overview_tab, customer_tab, product_tab, retention_tab = st.tabs(
    [
        "📊 Sales Overview",
        "👥 Customer Insights",
        "📦 Products & Countries",
        "📈 Cohort Retention",
    ]
)


# ==================================================
# TAB 1: SALES OVERVIEW
# ==================================================

with overview_tab:

    st.subheader("Sales at a Glance")

    kpis = summarize_sales(transactions)

    first, second, third, fourth, fifth = st.columns(5)

    first.metric(
        "Total Revenue",
        f"£{kpis['revenue_gbp'] / 1_000_000:,.2f}M",
    )
    second.metric(
        "Unique Orders",
        f"{kpis['unique_invoices']:,}",
    )
    third.metric(
        "Average Order Value",
        f"£{kpis['average_order_value_gbp']:,.2f}",
    )
    fourth.metric(
        "Customers",
        f"{kpis['customers']:,}",
    )
    fifth.metric(
        "Repeat Purchase Rate",
        f"{kpis['repeat_purchase_rate_pct']:.1f}%",
    )

    st.caption(
        "Orders use distinct invoice numbers. Repeat purchase "
        "rate is the share of customers with two or more distinct "
        "invoices in the selected transaction window."
    )

    st.write("")

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
            xaxis_title="",
            yaxis_title="Revenue (£)",
            hovermode="x unified",
        )

        st.plotly_chart(
            style_chart(fig),
            width="stretch",
        )

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

        st.plotly_chart(
            style_chart(fig),
            width="stretch",
        )

    st.info(
        "**About this analysis:** Revenue is observed sales, "
        "not profit. Results use the documented cleaning rules "
        "applied to the real UCI Online Retail dataset."
    )


# ==================================================
# TAB 2: CUSTOMER INSIGHTS
# ==================================================

with customer_tab:

    st.subheader("Understanding Customer Behavior")

    customers = customer_rfm(transactions)
    summary = summarize_sales(transactions)

    st.metric(
        "Repeat Purchase Rate",
        f"{summary['repeat_purchase_rate_pct']:.1f}%",
    )

    st.caption(
        "Share of identifiable customers with at least two "
        "distinct invoices in the selected window."
    )

    if customers.empty:
        st.warning("No customer-level data is available.")
    else:
        left, right = st.columns([1, 1.5], gap="large")

        with left:
            st.subheader("Customer Segments")

            counts = (
                customers["Segment"]
                .value_counts()
                .rename_axis("Segment")
                .reset_index(name="Customers")
                .sort_values("Customers")
            )

            fig = px.bar(
                counts,
                x="Customers",
                y="Segment",
                orientation="h",
                color="Segment",
                color_discrete_sequence=PALETTE,
                title="Customers by RFM Segment",
            )

            fig.update_layout(
                showlegend=False,
                xaxis_title="Customers",
                yaxis_title="",
            )

            st.plotly_chart(
                style_chart(fig),
                width="stretch",
            )

        with right:
            st.subheader("Customer Recency and Value")

            fig = px.scatter(
                customers,
                x="RecencyDays",
                y="MonetaryGBP",
                color="Segment",
                size="Frequency",
                hover_data=["CustomerID", "Frequency"],
                color_discrete_sequence=PALETTE,
                title="Recency vs. Observed Spend",
            )

            fig.update_layout(
                xaxis_title="Days Since Last Invoice",
                yaxis_title="Observed Sales Value (£)",
            )

            st.plotly_chart(
                style_chart(fig),
                width="stretch",
            )

        st.subheader("Customer Details")

        st.dataframe(
            customers[
                [
                    "CustomerID",
                    "RecencyDays",
                    "Frequency",
                    "MonetaryGBP",
                    "Segment",
                ]
            ].rename(
                columns={
                    "CustomerID": "Customer ID",
                    "RecencyDays": "Recency (days)",
                    "Frequency": "Distinct Invoices",
                    "MonetaryGBP": "Observed Spend (£)",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    st.info(
        "**RFM is descriptive:** Recency, frequency, and monetary "
        "value describe observed transactions. Segment labels "
        "are rule-based, not churn predictions."
    )


# ==================================================
# TAB 3: PRODUCTS AND COUNTRIES
# ==================================================

with product_tab:

    st.subheader("Best-Selling Products")

    products = (
        product_performance(transactions)
        .head(15)
        .sort_values("RevenueGBP")
    )

    if products.empty:
        st.warning("No product results match the filters.")
    else:
        fig = px.bar(
            products,
            x="RevenueGBP",
            y="Description",
            orientation="h",
            title="Top Products by Revenue",
            hover_data=[
                "StockCode",
                "UnitsSold",
                "Invoices",
            ],
        )

        fig.update_traces(
            marker_color=PURPLE,
        )

        fig.update_layout(
            xaxis_title="Revenue (£)",
            yaxis_title="",
        )

        fig = style_chart(fig, height=600)
        fig.update_layout(
            margin=dict(l=180, r=30, t=65, b=40),
        )

        st.plotly_chart(fig, width="stretch")

    st.subheader("Country Performance")

    countries = country_performance(transactions)
    countries = countries.sort_values(
        "RevenueGBP",
        ascending=False,
    )

    left, right = st.columns([1, 1], gap="large")

    with left:
        fig = px.scatter(
            countries,
            x="Invoices",
            y="RevenueGBP",
            size="Customers",
            hover_name="Country",
            title="Revenue vs. Invoice Volume",
        )

        fig.update_traces(marker_color=TEAL)

        fig.update_layout(
            xaxis_title="Distinct Invoices",
            yaxis_title="Revenue (£)",
        )

        st.plotly_chart(
            style_chart(fig),
            width="stretch",
        )

    with right:
        st.subheader("Country Comparison")

        st.dataframe(
            countries.rename(
                columns={
                    "RevenueGBP": "Revenue (£)",
                    "Invoices": "Distinct Invoices",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    st.caption(
        "Only retained merchandise transactions are analyzed. "
        "Cleaning exclusions are documented in DATA_CLEANING.md."
    )


# ==================================================
# TAB 4: COHORT RETENTION
# ==================================================

with retention_tab:

    st.subheader("Monthly Customer Retention")

    retention = cohort_retention(transactions)

    if retention.empty:
        st.warning(
            "No cohort activity is available for these filters."
        )
    else:
        fig = px.imshow(
            retention,
            text_auto=".0f",
            color_continuous_scale=[
                [0, "#F1EEFC"],
                [0.5, "#B8A8ED"],
                [1, "#7664D8"],
            ],
            aspect="auto",
            labels={
                "x": "Months Since First Observed Order",
                "y": "First Observed Order Month",
                "color": "Retained (%)",
            },
            title="Monthly Customer Retention (%)",
        )

        fig.update_layout(
            coloraxis_colorbar=dict(
                title="Retained (%)"
            )
        )

        st.plotly_chart(
            style_chart(fig, height=520),
            width="stretch",
        )

        st.subheader("Retention Data")

        st.dataframe(
            retention.round(1),
            width="stretch",
        )

    st.info(
        "Cohorts are based on each customer's first invoice "
        "within the selected data. This is observed repeat "
        "activity, not a forecast or causal retention estimate."
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Data source: UCI Machine Learning Repository | "
    "Online Retail Dataset | December 2010 – December 2011"
)
