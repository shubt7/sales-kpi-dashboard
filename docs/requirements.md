# Requirements: Sales KPI Dashboard

## Scope
One Power BI dashboard with three pages (executive summary, sales performance, pricing and discounts), built from one order-level dataset.

## User stories and acceptance criteria

**US-01: Headline KPIs**
As an executive, I want to see total revenue, total profit, profit margin %, orders and average order value so I can judge overall performance.
- Given the date filter is set to all years, the cards show totals that match `data/kpi_headline.csv`.
- Profit margin % = total profit ÷ total revenue, shown to one decimal place.

**US-02: Trend over time**
As a finance lead, I want a monthly revenue line with a 3-month average so I can see the trend without monthly noise.
- The line shows one point per month, Jan 2023 to Dec 2025.
- Monthly totals match `data/kpi_monthly_trend.csv`.

**US-03: Performance by region and channel**
As a regional manager, I want revenue, share and margin by region and channel so I can compare performance.
- Shares add up to 100%.
- Slicers for year, region and channel filter all visuals on the page.

**US-04: Product and rep performance**
As a sales director, I want revenue and margin by product and by sales rep so I can recognise strong performers and products with weak margins.
- Sales rep table sorts by revenue, highest first.

**US-05: Discount impact**
As a pricing analyst, I want profit margin by discount band so I can see whether deeper discounts reduce profit.
- Bands are 0–5%, 5–10%, 10–20% and 20–30%.
- Margin per band matches `data/kpi_discount_bands.csv`.

## Non-functional
- Data refreshes from the CSV file in the project.
- Each visual has a title that states the question it answers.
- The dashboard loads in under 5 seconds on a standard laptop.
