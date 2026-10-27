"""Small checks for the documented cleaning rules and dashboard metrics."""

import pandas as pd

from real_data_dashboard.analytics import cohort_retention, customer_rfm, summarize_sales
from real_data_dashboard.data_pipeline import EXPECTED_COLUMNS, clean_transactions


def sample_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["100001", "85123A", "HEART T-LIGHT", 2, "2011-01-01", 3.0, 10001, "United Kingdom"],
            ["100001", "85123A", "HEART T-LIGHT", 2, "2011-01-01", 3.0, 10001, "United Kingdom"],
            ["C100002", "85123A", "HEART T-LIGHT", -2, "2011-01-02", 3.0, 10001, "United Kingdom"],
            ["100003", "POST", "POSTAGE", 1, "2011-01-03", 2.0, 10002, "France"],
            ["100004", "71053", "LANTERN", 1, "2011-01-04", 0.0, 10002, "France"],
            ["100005", "84406B", "HANGER", 1, "2011-01-05", 2.0, None, "France"],
            ["100006", "84406B", None, 1, "2011-01-06", 2.0, 10003, "France"],
            ["100007", "84406B", "HANGER", 1, "2011-01-07", 2.0, 10002, "France"],
        ],
        columns=EXPECTED_COLUMNS,
    )


def test_cleaning_retains_only_valid_customer_merchandise_rows_and_keeps_source():
    raw = sample_rows()
    before = raw.copy(deep=True)
    clean, cancellations, excluded, summary = clean_transactions(raw)

    assert len(clean) == 2
    assert len(cancellations) == 1
    assert len(excluded) == 6
    assert clean["Revenue"].tolist() == [6.0, 2.0]
    assert summary["rows_excluded_union"] == 6
    assert summary["exclusion_flag_counts_nonexclusive"]["exact_duplicate_after_first_copy"] == 1
    assert raw.equals(before)


def test_order_metrics_count_distinct_invoice_numbers():
    rows = pd.DataFrame(
        {
            "InvoiceNo": ["A", "A", "B"],
            "CustomerID": ["1", "1", "1"],
            "Revenue": [5.0, 5.0, 10.0],
            "InvoiceDate": pd.to_datetime(["2011-01-01", "2011-01-01", "2011-02-01"]),
            "Quantity": [1, 1, 1],
        }
    )
    metrics = summarize_sales(rows)
    assert metrics["unique_invoices"] == 2
    assert metrics["revenue_gbp"] == 20.0
    assert metrics["average_order_value_gbp"] == 10.0
    assert metrics["repeat_purchase_rate_pct"] == 100.0


def test_rfm_and_cohort_work_with_small_customer_groups():
    rows = pd.DataFrame(
        {
            "InvoiceNo": ["A", "B"],
            "CustomerID": ["1", "2"],
            "Revenue": [5.0, 8.0],
            "InvoiceDate": pd.to_datetime(["2011-01-01", "2011-02-01"]),
        }
    )
    assert len(customer_rfm(rows)) == 2
    retention = cohort_retention(rows)
    assert retention.loc["2011-01", 0] == 100.0
