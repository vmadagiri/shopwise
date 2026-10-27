import plotly.express as px
import streamlit as st

from analytics import country_performance, product_performance
from shared import page_header

st.set_page_config(page_title="Products and Countries", page_icon="📦", layout="wide")
transactions = page_header("Products & Countries", "Compare merchandise sales by product and customer country.")
if transactions.empty:
    st.warning("No transactions match the current filters.")
    st.stop()

products = product_performance(transactions).head(15).sort_values("RevenueGBP")
fig = px.bar(products, x="RevenueGBP", y="Description", orientation="h", color="RevenueGBP", title="Top products by observed revenue", hover_data=["StockCode", "UnitsSold", "Invoices"])
fig.update_layout(xaxis_title="Revenue (£)", yaxis_title="")
st.plotly_chart(fig, width="stretch")

countries = country_performance(transactions).sort_values("RevenueGBP", ascending=False)
left, right = st.columns([1, 1])
with left:
    fig = px.scatter(countries, x="Invoices", y="RevenueGBP", size="Customers", color="Country", hover_name="Country", title="Country revenue and invoice volume")
    fig.update_layout(xaxis_title="Distinct invoices", yaxis_title="Revenue (£)", showlegend=False)
    st.plotly_chart(fig, width="stretch")
with right:
    st.subheader("Country comparison")
    st.dataframe(countries.rename(columns={"Country": "Country", "RevenueGBP": "Revenue (£)", "Invoices": "Distinct invoices", "Customers": "Customers"}), width="stretch", hide_index=True)

st.caption("The filters apply to this page too. Product rows are merchandise items only; adjustment, delivery, voucher, and fee codes are documented in DATA_CLEANING.md.")
