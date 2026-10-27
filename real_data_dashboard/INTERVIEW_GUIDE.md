# Interview notes and resume bullets

## 30-second project explanation

“I built a reproducible customer analytics dashboard using the UCI Online Retail transaction dataset. I started from the original Excel workbook, audited missing values, duplicate rows, cancellations, invalid quantities and prices, customer IDs, and service-style stock codes, and kept both cancellation and row-level exclusion audits. The cleaned transaction table feeds a multi-page Streamlit dashboard with interactive Plotly charts. I count orders by distinct invoice number and calculate repeat purchase, RFM, and cohort views with explicit definitions, so the dashboard is useful without presenting a descriptive label as a prediction.”

## Questions to be ready for

**Why did you exclude rows with missing CustomerID?** Customer-level metrics need a stable identifier. I keep a row-level exclusion record and do not pretend those lines belong to a known customer. That choice means the revenue shown is for the identifiable, valid merchandise subset, not the entire transaction ledger.

**How do you count orders?** I use `nunique()` on `InvoiceNo`, because each invoice can have many product lines. AOV is the sum of retained line revenue divided by this distinct invoice count.

**What does “at risk” mean?** It is a descriptive rule based on a lower recency score and a higher frequency score within the current analysis window. It is not a churn model, probability, or forecast.

**What would you improve next?** I would validate the code list with a domain owner, add cost or margin data for profit analysis, compare repeat behavior across longer periods, and add automated data quality monitoring. I would also keep raw data access and customer identifiers controlled in a production deployment.

## ATS-ready resume bullets

- Built an auditable pandas pipeline for UCI's 541,909-row Online Retail dataset, documenting overlapping quality flags and retaining 391,150 positive, identifiable merchandise lines with separate cancellation and exclusion audits.
- Developed a multi-page Streamlit and Plotly dashboard with interactive date, country, and product filters to explore GBP revenue, distinct-invoice KPIs, repeat purchase behavior, RFM segments, cohort retention, and product and country performance.
- Applied customer analytics definitions using distinct invoice counts and documented data limitations, avoiding unsupported claims about profit, churn prediction, personalization impact, or causality.
