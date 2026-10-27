import plotly.express as px
import streamlit as st

from analytics import cohort_retention
from shared import page_header

st.set_page_config(page_title="Cohort Retention", page_icon="📈", layout="wide")
transactions = page_header("Cohort Retention", "Explore the share of customers who return in later calendar months.")
retention = cohort_retention(transactions)
if retention.empty:
    st.warning("No cohort activity is available for these filters.")
    st.stop()

fig = px.imshow(
    retention,
    text_auto=".0f",
    color_continuous_scale="Purples",
    aspect="auto",
    labels={"x": "Months since first observed order", "y": "First observed order month", "color": "Retained (%)"},
    title="Monthly customer retention (%)",
)
fig.update_layout(coloraxis_colorbar=dict(title="Retained (%)"))
st.plotly_chart(fig, width="stretch")
st.dataframe(retention.round(1), width="stretch")
st.info("Cohorts are based on each customer's first invoice inside the currently filtered rows. Because the source covers about one year and filters can hide transactions, this is an observed repeat-activity view, not a forecast or causal retention estimate.")
