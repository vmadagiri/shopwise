"""Shared data loading and sidebar filters for the Streamlit pages."""

from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parent
CLEAN_FILE = PROJECT_DIR / "data" / "processed" / "cleaned_transactions.csv"


@st.cache_data(show_spinner="Loading cleaned transactions...")
def load_transactions() -> pd.DataFrame:
    """Read the generated clean file once and cache it between reruns."""
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(
            "Cleaned data is missing. From the repository root, run "
            "`python real_data_dashboard/download_data.py` and then "
            "`python real_data_dashboard/data_pipeline.py`."
        )
    data = pd.read_csv(CLEAN_FILE, parse_dates=["InvoiceDate"])
    data["CustomerID"] = data["CustomerID"].astype("string")
    return data


def page_header(title: str, subtitle: str) -> pd.DataFrame:
    """Show consistent title and reusable date, country, and product filters."""
    st.title(title)
    st.caption(subtitle)
    try:
        data = load_transactions()
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    st.sidebar.header("Explore the data")
    min_day = data["InvoiceDate"].min().date()
    max_day = data["InvoiceDate"].max().date()
    date_values = st.sidebar.date_input(
        "Invoice date range", value=(min_day, max_day), min_value=min_day, max_value=max_day
    )
    countries = sorted(data["Country"].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect("Countries (empty means all)", countries)
    products = ["All products"] + sorted(data["Description"].dropna().unique().tolist())
    selected_product = st.sidebar.selectbox("Product", products)
    st.sidebar.caption("Sales are recorded in the dataset's source currency: GBP (£).")

    if isinstance(date_values, tuple) and len(date_values) == 2:
        start_day, end_day = date_values
    else:
        start_day, end_day = min_day, max_day
    filtered = data.loc[
        data["InvoiceDate"].dt.date.between(start_day, end_day)
    ].copy()
    if selected_countries:
        filtered = filtered.loc[filtered["Country"].isin(selected_countries)]
    if selected_product != "All products":
        filtered = filtered.loc[filtered["Description"].eq(selected_product)]
    return filtered
