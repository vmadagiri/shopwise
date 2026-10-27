# UCI Online Retail Customer Analytics

A beginner-friendly, reproducible customer analytics project using the real **Online Retail** workbook from the UCI Machine Learning Repository. The existing synthetic project remains at the repository root; this is a separate subproject.

## Data and attribution

- Dataset: [UCI Online Retail, dataset ID 352](https://archive.ics.uci.edu/dataset/352/online%2Bretail)
- DOI: [10.24432/C5BW33](https://doi.org/10.24432/C5BW33)
- Creator: Daqing Chen (2015)
- License: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- Required attribution: Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33.

The original 22.6 MB Excel file is downloaded from UCI when needed and is ignored by Git. The source workbook is never edited. See [DATA_CLEANING.md](DATA_CLEANING.md) for field-level decisions and [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for field definitions.

## Run it

Run these commands from the repository root after checking out the `real-data-dashboard` branch:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -r real_data_dashboard/requirements.txt
python real_data_dashboard/download_data.py
python real_data_dashboard/data_pipeline.py
python -m streamlit run real_data_dashboard/app.py
```

The dashboard opens in your browser. Use the sidebar to filter invoice dates, countries, and products. The pipeline saves these local (Git-ignored) outputs under `real_data_dashboard/data/processed/`:

- `cleaned_transactions.csv` — rows retained for merchandise and customer analysis
- `cancellation_audit.csv` — every source line whose invoice number begins with `C`
- `exclusion_audit.csv` — every excluded source row with one Boolean column per reason
- `cleaning_summary.json` — source row count, missing values, overlapping reason counts, and validations

Re-running the download script reuses an existing workbook. To force a fresh UCI download, delete `real_data_dashboard/data/raw/Online Retail.xlsx` first and run the download command again.

## Pages

1. **Overview** — GBP revenue, distinct invoices, average order value, customers, repeat purchase rate, monthly sales, and top countries.
2. **Customer Insights** — rule-based RFM segments and customer-level details.
3. **Products & Countries** — merchandise performance and country comparisons.
4. **Cohort Retention** — a monthly retention heatmap.

All charts are interactive Plotly charts. KPIs are recalculated for the current date, country, and product filters. Invoice counts always use distinct `InvoiceNo` values.

## Validate and test

```bash
python real_data_dashboard/data_pipeline.py
python -m pytest -q real_data_dashboard/tests
```

The tests use a tiny hand-built fixture to check overlap-aware cleaning, immutable input, distinct-invoice KPIs, small RFM groups, and cohort calculations. The full-data run writes checks into `cleaning_summary.json`; it does not generate synthetic rows or fabricate values.

## Screenshots

See [`screenshots/`](screenshots/) for static dashboard-view previews rendered from the cleaned workbook and the same calculation functions. Findings are documented separately in [FINDINGS.md](FINDINGS.md); those numbers are computed from the project code and downloaded UCI workbook, not copied from an example.

## Project boundaries

Revenue is quantity multiplied by unit price in GBP. The dataset does not contain cost, profit, web activity, campaign exposure, or future outcomes, so this project does not calculate profit, personalization impact, causal effects, or churn probabilities. The “at risk” RFM label is a transparent descriptive rule, not a predictive model.
