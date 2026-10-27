import plotly.express as px
import streamlit as st

from analytics import customer_rfm, summarize_sales
from shared import page_header

st.set_page_config(page_title="Customer Insights", page_icon="👥", layout="wide")
transactions = page_header("Customer Insights", "Rule-based RFM segments and repeat purchase behavior in the selected transaction window.")
if transactions.empty:
    st.warning("No transactions match the current filters.")
    st.stop()

summary = summarize_sales(transactions)
customers = customer_rfm(transactions)
left, right = st.columns([1, 1.5])
with left:
    st.metric("Repeat purchase rate", f"{summary['repeat_purchase_rate_pct']:.1f}%")
    st.caption("Share of identifiable customers with at least two distinct invoices in this filtered window.")
    segment_counts = customers["Segment"].value_counts().rename_axis("Segment").reset_index(name="Customers")
    fig = px.bar(segment_counts.sort_values("Customers"), x="Customers", y="Segment", orientation="h", color="Segment", title="Customers by RFM rule segment")
    fig.update_layout(showlegend=False, xaxis_title="Customers", yaxis_title="")
    st.plotly_chart(fig, width="stretch")
with right:
    st.subheader("Customer recency and value")
    fig = px.scatter(customers, x="RecencyDays", y="MonetaryGBP", color="Segment", size="Frequency", hover_data=["CustomerID", "Frequency"], title="Recency vs. observed spend")
    fig.update_layout(xaxis_title="Days since last observed invoice", yaxis_title="Observed sales value (£)")
    st.plotly_chart(fig, width="stretch")

st.subheader("Customer-level detail")
st.dataframe(customers[["CustomerID", "RecencyDays", "Frequency", "MonetaryGBP", "Segment"]].rename(columns={"CustomerID": "Customer ID", "RecencyDays": "Recency (days)", "Frequency": "Distinct invoices", "MonetaryGBP": "Observed spend (£)"}), width="stretch", hide_index=True)
st.info("**RFM is descriptive:** recency is measured from one day after the latest selected invoice date, frequency counts distinct invoices, and monetary value sums line-item revenue. ‘At risk’ is a simple rule label, not a churn probability or prediction.")
