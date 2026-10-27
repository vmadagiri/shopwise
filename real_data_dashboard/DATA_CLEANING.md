# Data cleaning methodology

## Source and reproducibility

The project downloads UCI dataset 352 from `https://archive.ics.uci.edu/static/public/352/online+retail.zip`, extracts the original `Online Retail.xlsx`, and verifies the expected eight-column structure. It does not edit or resave the raw workbook. Every retained and excluded output carries `SourceRow`, the corresponding one-based Excel row number including the header.

Run `python real_data_dashboard/download_data.py` followed by `python real_data_dashboard/data_pipeline.py` from the repository root. The cleaning script prints checkpoints and writes its outputs to `real_data_dashboard/data/processed/`.

## Audit and exclusions

Missing values are counted in every source column before cleaning. Each exclusion flag is evaluated against all original rows, so the reason counts below can overlap and must not be added together. `exclusion_audit.csv` contains all excluded source records, Boolean flags for each rule, and a readable `exclusion_reasons` field. `cancellation_audit.csv` separately preserves every source line on an invoice whose number begins with `C`.

| Rule | Why it is used |
|---|---|
| Cancellation invoice (`InvoiceNo` begins with C) | A reversal is not a positive sale; preserve it in its own audit rather than include it in merchandise-sales KPIs |
| Exact duplicate line after its first copy | Avoid counting repeated copies of an otherwise identical source record twice |
| Missing or nonpositive quantity | Exclude returns/adjustments and non-usable unit quantities from positive-sales measures |
| Missing or nonpositive unit price | A nonpositive price cannot support the positive-sales metrics shown here |
| Missing `CustomerID` | Customer counts, repeat purchase, RFM, and customer cohorts require an identifiable customer |
| Invalid/missing invoice date or stock code | Required to place a sale in time and to identify the product |
| Missing product description | Exclude from product performance where a human-readable product is required |
| Known non-merchandise stock code | Keep merchandise sales separate from postage, discounts, fees, vouchers, and adjustment codes |

The non-merchandise list is deliberately visible in `data_pipeline.py`: `POST`, `D`, `DOT`, `M`, `BANK CHARGES`, `PADS`, `CRUK`, `AMAZONFEE`, `C2`, `S`, `B`, plus codes beginning with `DCGS` followed by digits. The exact unique stock codes flagged in the source workbook are recorded in `cleaning_summary.json`; the output audit records every affected row. This is an analysis choice, not a claim that UCI marks these as erroneous.

## Validation

The pipeline checks that retained quantities and unit prices are positive, customer IDs are present, source row numbers are unique, the retained table has no exact duplicate line, and the in-memory raw frame retains its original row count. Tests cover the same logic on a small fixture and check invoice-level calculations. Raw workbook hashes or source files are not rewritten by the pipeline.

## Important limits

The UCI metadata says there are no missing values, but the downloaded workbook contains blank `Description` and `CustomerID` values; the actual workbook is the basis for the audit. Exclusions overlap, so report the union for removed rows and the nonexclusive flags for explanation. The curated clean file is a positive, identifiable merchandise view; it is not a complete accounting ledger and does not support profit, cost, churn predictions, web personalization, or causal claims.
