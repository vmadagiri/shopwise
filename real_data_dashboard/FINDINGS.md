# Observed findings and recommendations

These figures were calculated from the cleaned UCI workbook using the code in this folder. Full-period views use all retained rows from December 1, 2010 through December 9, 2011. Revenue is retained line sales value in GBP, not profit.

## Observed findings

- The source has **541,909 rows**. The pipeline retained **391,150 merchandise lines** and excluded the union of **150,759 rows**. Exclusion reasons overlap.
- The workbook has **135,080 missing `CustomerID` values** and **1,454 missing descriptions**; other source columns have no blanks. The pipeline flagged **9,288 cancellation lines**, **5,268 exact duplicate copies**, **10,624 nonpositive or missing quantities**, **2,517 nonpositive or missing prices**, **2,936 special-code lines**, and **1,454 missing descriptions**. These flag counts overlap.
- The clean table contains **18,402 distinct invoices**, **4,334 identified customers**, and **3,659 distinct stock codes** across **37 countries**.
- Total retained merchandise revenue is **£8,737,227.64**. Average order value is **£474.80** across distinct invoices.
- **65.3%** of customers in the full-period clean table placed two or more distinct invoices.
- The United Kingdom contributed **£7,242,855.32** across **16,579 distinct invoices**. It is the largest country by retained revenue in this dataset.
- November 2011 is the largest observed calendar month by retained sales at **£1,136,534.00**. The last month, December 2011, is partial: the last observed invoice date is December 9.
- `PAPER CRAFT , LITTLE BIRDIE` has **£168,469.60** retained line revenue across **one invoice**. This is a concentrated observation, not evidence of typical demand.
- The full-period, transparent rule-based RFM labels classify **1,312 Champions**, **205 Loyal**, **650 Recent**, **650 At risk (rule-based)**, and **1,517 Other** customers. These are descriptive groups, not predictive classifications.

The full count-by-reason table and retained-row validation booleans are in the generated `data/processed/cleaning_summary.json` after running the pipeline. The overlapping counts are included to show why the **150,759-row exclusion union** is the correct total removed.

## What the data suggests checking next

These are analysis ideas, not findings about cause or future behavior:

- Review whether the UK revenue concentration should guide a separate country-level assortment or service analysis.
- Inspect high-revenue products with very few invoices before using them for stocking decisions; one large order can dominate a total.
- Compare repeat purchase rates across longer or multiple observation windows before designing retention actions.
- Add cost, margin, inventory, campaign, and web-event data before evaluating profitability or personalization.

## Definitions and limitations

Invoice counts use distinct `InvoiceNo`. AOV divides retained revenue by distinct invoices. Repeat purchase rate counts identifiable customers with at least two invoices in this observed period. Cohorts use first observed month within currently filtered rows, so they are an exploratory description of this roughly one-year dataset. No causal effect, profit, web behavior, or churn probability is measured.
