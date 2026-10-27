"""Customer Analytics dashboard powered by UCI Online Retail transactions."""

import streamlit as st
import plotly.express as px

from analytics import country_performance, monthly_sales, summarize_sales
from shared import page_header


st.set_page_config(page_title="Online Retail | Customer Analytics", page_icon="🛍️", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background: #f7f8fc; }
    [data-testid="stMetric"] { background: white; padding: 16px; border-radius: 12px; border: 1px solid #e8eaf2; }
    h1, h2, h3 { color: #17243b; }
    </style>
    """,
    unsafe_allow_html=True,
)

transactions = page_header(
    "Online Retail | Customer Analytics",
    "A reproducible analysis of UCI's real retail transactions. Use the sidebar to explore dates, countries, and products.",
)

if transactions.empty:
    st.warning("No transactions match the current filters. Try a wider date range or different selections.")
    st.stop()

kpis = summarize_sales(transactions)
first, second, third, fourth, fifth = st.columns(5)
first.metric("Revenue", f"£{kpis['revenue_gbp']:,.0f}")
second.metric("Unique invoices", f"{kpis['unique_invoices']:,}")
third.metric("Average order value", f"£{kpis['average_order_value_gbp']:,.2f}")
fourth.metric("Customers", f"{kpis['customers']:,}")
fifth.metric("Repeat purchase rate", f"{kpis['repeat_purchase_rate_pct']:.1f}%")
st.caption("Order counts use distinct InvoiceNo. Repeat purchase rate means customers with 2+ distinct invoices in the current filtered window.")

left, right = st.columns([1.6, 1])
with left:
    st.subheader("Monthly sales trend")
    by_month = monthly_sales(transactions)
    fig = px.line(by_month, x="Month", y="Revenue", markers=True, title="Revenue by invoice month")
    fig.update_traces(line_color="#5b5bd6", hovertemplate="%{x|%b %Y}<br>Revenue £%{y:,.2f}<extra></extra>")
    fig.update_layout(yaxis_title="Revenue (£)", xaxis_title="", margin=dict(t=50, b=10))
    st.plotly_chart(fig, width="stretch")
with right:
    st.subheader("Top countries")
    countries = country_performance(transactions).head(10).sort_values("RevenueGBP")
    fig = px.bar(countries, x="RevenueGBP", y="Country", orientation="h", title="Revenue by country")
    fig.update_traces(marker_color="#29a88f", hovertemplate="%{y}<br>Revenue £%{x:,.2f}<extra></extra>")
    fig.update_layout(xaxis_title="Revenue (£)", yaxis_title="", margin=dict(t=50, b=10))
    st.plotly_chart(fig, width="stretch")

st.info("**How to read this:** these are observed transaction totals after the documented cleaning rules. Revenue is sales value, not profit, and the dataset contains no website behavior or marketing exposure.")
