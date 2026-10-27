# Data dictionary

## Source fields

UCI describes the workbook as 541,909 transaction-line records with eight fields. `CustomerID` is missing on some rows even though the public metadata table says “no” missing values; this project audits the actual workbook directly.

| Field | Type used | Meaning | Cleaning notes |
|---|---|---|---|
| `InvoiceNo` | text | Invoice identifier; a value beginning with `C` marks a cancellation | Kept as text so cancellation prefixes are preserved; counted distinctly for orders |
| `StockCode` | text | Product or service code | Kept as text; special adjustment/service codes are excluded from merchandise metrics |
| `Description` | text | Product description | Missing descriptions are excluded from the clean product/customer table |
| `Quantity` | integer | Units on a transaction line | Retained only when greater than zero |
| `InvoiceDate` | datetime | Invoice transaction timestamp | Parsed for dates and cohorts |
| `UnitPrice` | decimal | Unit price in pounds sterling | Retained only when greater than zero |
| `CustomerID` | text in clean output | Customer identifier | Missing IDs are excluded from customer-level analysis; stored as text to preserve identifier meaning |
| `Country` | text | Customer country | Used for filtering and comparison; no missing countries were found |

## Added fields

| Field | Meaning |
|---|---|
| `SourceRow` | Original Excel row number, counting the header as row 1; supports audit trace-back |
| `Revenue` | `Quantity * UnitPrice`, in GBP; transaction line sales value, not profit |
| `InvoiceMonth` | Calendar month derived from `InvoiceDate`, formatted `YYYY-MM` |
| Exclusion reason columns | Boolean flags in `exclusion_audit.csv`; a row can have several flags |
| `exclusion_reasons` | Semicolon-separated reasons explaining why that source row was excluded |

## Dashboard terms

- **Distinct invoice:** unique `InvoiceNo`; a multi-line basket still counts as one order.
- **Average order value (AOV):** retained line revenue divided by distinct invoices in the current filters.
- **Repeat purchase rate:** customers with two or more distinct invoices divided by all customers represented in the current filters.
- **RFM:** recency (days since last observed invoice), frequency (distinct invoices), and monetary (sum of retained line revenue), calculated within the current filter window.
- **Cohort:** month of a customer's first invoice inside the currently filtered transaction rows. Retention is the percentage of that cohort with an invoice in each later month.
