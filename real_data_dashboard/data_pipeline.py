"""A small, auditable cleaning pipeline for UCI Online Retail."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
RAW_FILE = PROJECT_DIR / "data" / "raw" / "Online Retail.xlsx"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
EXPECTED_COLUMNS = [
    "InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate",
    "UnitPrice", "CustomerID", "Country",
]

# These are adjustment, postage, fee, or voucher codes seen in this workbook.
# The retained transaction table is for merchandise sales only.
NON_MERCHANDISE_CODES = {
    "POST", "D", "DOT", "M", "BANK CHARGES", "PADS", "CRUK",
    "AMAZONFEE", "C2", "S", "B",
}


def load_raw_data(file_path: Path = RAW_FILE) -> pd.DataFrame:
    """Read the source workbook and standardize only in-memory types."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw workbook not found at {file_path}. Run `python real_data_dashboard/download_data.py` first."
        )
    print("Checkpoint 1/5: Reading the unchanged Excel workbook...")
    raw = pd.read_excel(file_path, dtype={"InvoiceNo": "string", "StockCode": "string"})
    if list(raw.columns) != EXPECTED_COLUMNS:
        raise ValueError(f"Unexpected columns: {list(raw.columns)}")
    raw["InvoiceNo"] = raw["InvoiceNo"].str.strip()
    raw["StockCode"] = raw["StockCode"].str.strip()
    return raw


def audit_missing_values(raw: pd.DataFrame) -> dict[str, int]:
    """Return the count of missing values in each source column."""
    return {str(column): int(count) for column, count in raw.isna().sum().items()}


def is_non_merchandise(stock_code: object) -> bool:
    """Identify known adjustment and service codes, including code families."""
    if pd.isna(stock_code):
        return False
    code = str(stock_code).strip().upper()
    return code in NON_MERCHANDISE_CODES or bool(re.fullmatch(r"DCGS\d+", code))


def clean_transactions(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Return retained merchandise rows, cancellation audit, and count summary.

    Each flag is evaluated against the original workbook, so reason counts can
    overlap. The final exclusion count is the union of flagged rows.
    """
    print("Checkpoint 2/5: Auditing blanks, duplicates, cancellations, and item rows...")
    working = raw.copy()
    working["SourceRow"] = range(2, len(working) + 2)  # Excel header is row 1.
    working["InvoiceDate"] = pd.to_datetime(working["InvoiceDate"], errors="coerce")
    working["Quantity"] = pd.to_numeric(working["Quantity"], errors="coerce")
    working["UnitPrice"] = pd.to_numeric(working["UnitPrice"], errors="coerce")

    cancellation_mask = working["InvoiceNo"].str.upper().str.startswith("C", na=False)
    cancellation_audit = working.loc[cancellation_mask].copy()
    duplicate_mask = working[EXPECTED_COLUMNS].duplicated(keep="first")
    masks = {
        "cancellation_invoice": cancellation_mask,
        "exact_duplicate_after_first_copy": duplicate_mask,
        "quantity_missing_or_nonpositive": working["Quantity"].isna() | working["Quantity"].le(0),
        "unit_price_missing_or_nonpositive": working["UnitPrice"].isna() | working["UnitPrice"].le(0),
        "missing_customer_id": working["CustomerID"].isna(),
        "missing_or_invalid_invoice_date": working["InvoiceDate"].isna(),
        "missing_stock_code": working["StockCode"].isna() | working["StockCode"].eq(""),
        "missing_product_description": working["Description"].isna() | working["Description"].astype("string").str.strip().eq(""),
        "non_merchandise_code": working["StockCode"].map(is_non_merchandise),
    }

    print("Checkpoint 3/5: Applying documented exclusions...")
    excluded_any = pd.Series(False, index=working.index)
    counts = {}
    for reason, mask in masks.items():
        mask = mask.fillna(False)
        counts[reason] = int(mask.sum())
        excluded_any |= mask
    excluded = working.loc[excluded_any].copy()
    for reason, mask in masks.items():
        excluded[reason] = mask.loc[excluded.index].fillna(False).astype(bool)
    excluded["exclusion_reasons"] = excluded.apply(
        lambda row: "; ".join(reason for reason in masks if row[reason]), axis=1
    )
    cleaned = working.loc[~excluded_any].copy()
    cleaned["Revenue"] = cleaned["Quantity"] * cleaned["UnitPrice"]
    cleaned["CustomerID"] = cleaned["CustomerID"].astype("Int64").astype("string")
    cleaned["InvoiceMonth"] = cleaned["InvoiceDate"].dt.to_period("M").astype(str)

    # Preserve every original source field plus its original Excel row number.
    cancellation_audit = cancellation_audit[[*EXPECTED_COLUMNS, "SourceRow"]]
    cleaned = cleaned[[*EXPECTED_COLUMNS, "SourceRow", "Revenue", "InvoiceMonth"]]
    excluded = excluded[[*EXPECTED_COLUMNS, "SourceRow", *masks.keys(), "exclusion_reasons"]]
    summary = {
        "source": "UCI Online Retail, dataset ID 352, DOI 10.24432/C5BW33",
        "source_rows": int(len(raw)),
        "missing_values_by_column": audit_missing_values(raw),
        "non_merchandise_stock_codes_flagged": sorted(
            str(code) for code in raw.loc[raw["StockCode"].map(is_non_merchandise), "StockCode"].dropna().unique()
        ),
        "exclusion_flag_counts_nonexclusive": counts,
        "rows_excluded_union": int(excluded_any.sum()),
        "cleaned_rows": int(len(cleaned)),
        "cancellation_audit_rows": int(len(cancellation_audit)),
        "exclusion_audit_rows": int(len(excluded)),
        "retained_rows_have_positive_quantity": bool(cleaned["Quantity"].gt(0).all()),
        "retained_rows_have_positive_unit_price": bool(cleaned["UnitPrice"].gt(0).all()),
        "retained_rows_have_customer_id": bool(cleaned["CustomerID"].notna().all()),
        "retained_rows_have_unique_source_rows": bool(cleaned["SourceRow"].is_unique),
        "retained_rows_have_no_exact_duplicates": bool(not cleaned[EXPECTED_COLUMNS].duplicated().any()),
        "raw_frame_rows_after_cleaning": int(len(raw)),
    }
    print(f"Source rows: {len(raw):,}")
    for reason, count in counts.items():
        print(f"  {reason}: {count:,} flagged rows (overlap is possible)")
    print(f"Excluded union: {summary['rows_excluded_union']:,}")
    print(f"Clean merchandise rows: {len(cleaned):,}")
    print("Checkpoint 4/5: Checking output rules...")
    if not all(summary[key] for key in (
        "retained_rows_have_positive_quantity", "retained_rows_have_positive_unit_price",
        "retained_rows_have_customer_id", "retained_rows_have_unique_source_rows",
        "retained_rows_have_no_exact_duplicates",
    )):
        raise AssertionError("A retained-row validation failed")
    if len(raw) != summary["raw_frame_rows_after_cleaning"]:
        raise AssertionError("The in-memory source frame changed size")
    print("All retained-row checks passed; the source workbook was not rewritten.")
    return cleaned, cancellation_audit, excluded, summary


def run_pipeline(file_path: Path = RAW_FILE, output_dir: Path = OUTPUT_DIR) -> dict:
    """Run cleaning and write processed outputs, leaving raw input untouched."""
    raw = load_raw_data(file_path)
    cleaned, cancellations, excluded, summary = clean_transactions(raw)
    output_dir.mkdir(parents=True, exist_ok=True)
    print("Checkpoint 5/5: Saving reproducible outputs...")
    cleaned.to_csv(output_dir / "cleaned_transactions.csv", index=False)
    cancellations.to_csv(output_dir / "cancellation_audit.csv", index=False)
    excluded.to_csv(output_dir / "exclusion_audit.csv", index=False)
    (output_dir / "cleaning_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Saved outputs in {output_dir}")
    return summary


if __name__ == "__main__":
    run_pipeline()
