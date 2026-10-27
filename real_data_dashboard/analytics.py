"""Readable calculations used by the dashboard and the cleaning tests."""

from math import ceil

import pandas as pd


def summarize_sales(transactions: pd.DataFrame) -> dict[str, float | int]:
    """Calculate sales KPIs with invoices counted as distinct orders."""
    invoice_count = int(transactions["InvoiceNo"].nunique())
    revenue = float(transactions["Revenue"].sum())
    customer_count = int(transactions["CustomerID"].nunique())
    customer_orders = transactions.groupby("CustomerID")["InvoiceNo"].nunique()
    repeat_rate = float(customer_orders.ge(2).mean() * 100) if len(customer_orders) else 0.0
    return {
        "revenue_gbp": revenue,
        "unique_invoices": invoice_count,
        "average_order_value_gbp": revenue / invoice_count if invoice_count else 0.0,
        "customers": customer_count,
        "repeat_purchase_rate_pct": repeat_rate,
    }


def monthly_sales(transactions: pd.DataFrame) -> pd.DataFrame:
    """One row per calendar month; order counts use distinct InvoiceNo."""
    monthly = transactions.copy()
    monthly["Month"] = monthly["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
    return (
        monthly.groupby("Month", as_index=False)
        .agg(Revenue=("Revenue", "sum"), Invoices=("InvoiceNo", "nunique"))
        .sort_values("Month")
    )


def customer_rfm(transactions: pd.DataFrame) -> pd.DataFrame:
    """Build recency, frequency, and monetary values and a simple rule segment."""
    if transactions.empty:
        return pd.DataFrame(columns=["CustomerID", "RecencyDays", "Frequency", "MonetaryGBP", "Segment"])

    as_of = transactions["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)
    customers = transactions.groupby("CustomerID", as_index=False).agg(
        LastOrder=("InvoiceDate", "max"),
        Frequency=("InvoiceNo", "nunique"),
        MonetaryGBP=("Revenue", "sum"),
    )
    customers["RecencyDays"] = (as_of - customers["LastOrder"].dt.normalize()).dt.days

    # Rank then split into four roughly equal groups; this remains stable when
    # many customers share the same value.
    customer_count = len(customers)
    customers["R_Score"] = 5 - (customers["RecencyDays"].rank(method="first") / customer_count * 4).apply(ceil).astype(int)
    customers["F_Score"] = (customers["Frequency"].rank(method="first") / customer_count * 4).apply(ceil).astype(int)
    customers["M_Score"] = (customers["MonetaryGBP"].rank(method="first") / customer_count * 4).apply(ceil).astype(int)

    def label_segment(row: pd.Series) -> str:
        if row["R_Score"] >= 3 and row["F_Score"] >= 3 and row["M_Score"] >= 3:
            return "Champions"
        if row["R_Score"] <= 2 and row["F_Score"] >= 3:
            return "At risk (rule-based)"
        if row["R_Score"] >= 3 and row["F_Score"] <= 2:
            return "Recent customers"
        if row["F_Score"] >= 3:
            return "Loyal customers"
        return "Other customers"

    customers["Segment"] = customers.apply(label_segment, axis=1)
    return customers.sort_values("MonetaryGBP", ascending=False)


def cohort_retention(transactions: pd.DataFrame) -> pd.DataFrame:
    """Return a cohort-month retention table from the currently filtered rows."""
    if transactions.empty:
        return pd.DataFrame()
    data = transactions[["CustomerID", "InvoiceNo", "InvoiceDate"]].copy()
    data["OrderMonth"] = data["InvoiceDate"].dt.to_period("M")
    first_month = data.groupby("CustomerID")["OrderMonth"].min().rename("CohortMonth")
    data = data.join(first_month, on="CustomerID")
    data["CohortIndex"] = (
        (data["OrderMonth"].dt.year - data["CohortMonth"].dt.year) * 12
        + data["OrderMonth"].dt.month - data["CohortMonth"].dt.month
    )
    active = data.drop_duplicates(["CustomerID", "OrderMonth"]).groupby(
        ["CohortMonth", "CohortIndex"]
    )["CustomerID"].nunique().unstack(fill_value=0)
    if active.empty:
        return active
    retention = active.div(active[0], axis=0) * 100
    retention.index = retention.index.astype(str)
    retention.columns.name = "Months since first observed order"
    return retention


def product_performance(transactions: pd.DataFrame) -> pd.DataFrame:
    """Summarize products while keeping revenue and order counts distinct."""
    return transactions.groupby(["StockCode", "Description"], as_index=False).agg(
        RevenueGBP=("Revenue", "sum"),
        UnitsSold=("Quantity", "sum"),
        Invoices=("InvoiceNo", "nunique"),
    ).sort_values("RevenueGBP", ascending=False)


def country_performance(transactions: pd.DataFrame) -> pd.DataFrame:
    """Country comparisons; invoice counts are distinct within each country."""
    return transactions.groupby("Country", as_index=False).agg(
        RevenueGBP=("Revenue", "sum"),
        Invoices=("InvoiceNo", "nunique"),
        Customers=("CustomerID", "nunique"),
    ).sort_values("RevenueGBP", ascending=False)
