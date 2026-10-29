# Building the Power BI dashboard

This guide walks through building the dashboard in Power BI Desktop (free from Microsoft) using the files in `data/`.

## 1. Load the data

1. Open Power BI Desktop, then **Get data → Text/CSV**, and choose `data/sales_orders.csv`.
2. In Power Query, check that `order_date` is a Date type and the money columns are Decimal numbers.
3. Click **Close & Apply**.

## 2. Create a date table

Power BI needs a date table for time-intelligence measures. In the **Modeling** tab, choose **New table** and paste:

```DAX
Date =
ADDCOLUMNS(
    CALENDAR(DATE(2023,1,1), DATE(2025,12,31)),
    "Year", YEAR([Date]),
    "Month", FORMAT([Date], "MMM yyyy"),
    "MonthStart", STARTOFMONTH([Date])
)
```

Then mark it as the date table (**Table tools → Mark as date table**) and relate `Date[Date]` to `sales_orders[order_date]`.

## 3. Add the measures

Create these in a dedicated **_Measures** table so they're easy to find.

```DAX
Total Revenue = SUM(sales_orders[revenue])

Total Profit = SUM(sales_orders[profit])

Profit Margin % = DIVIDE([Total Profit], [Total Revenue])

Orders = COUNTROWS(sales_orders)

Average Order Value = DIVIDE([Total Revenue], [Orders])

Revenue Prior Year = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Date[Date]))

Revenue YoY % = DIVIDE([Total Revenue] - [Revenue Prior Year], [Revenue Prior Year])

Revenue 3M Average =
AVERAGEX(
    DATESINPERIOD(Date[Date], MAX(Date[Date]), -3, MONTH),
    [Total Revenue]
)
```

## 4. Build the report pages

**Page 1: Executive summary**
- Cards: Total Revenue, Total Profit, Profit Margin %, Orders, Average Order Value.
- Line chart: `Date[MonthStart]` on the axis, with Total Revenue and Revenue 3M Average.
- Bar chart: Revenue by region.

**Page 2: Sales performance**
- Table or bar chart: Revenue and Profit Margin % by channel.
- Bar chart: Revenue by product.
- Matrix: Revenue by sales rep, with a conditional-format data bar.

**Page 3: Pricing and discounts**
- Column chart: Profit Margin % by `discount_pct` band. Create the band as a calculated column:

```DAX
Discount Band =
SWITCH(
    TRUE(),
    sales_orders[discount_pct] <= 5, "0-5%",
    sales_orders[discount_pct] <= 10, "5-10%",
    sales_orders[discount_pct] <= 20, "10-20%",
    "20-30%"
)
```

## 5. Add slicers and interactions

- Add slicers for Year, Region and Channel.
- Set the slicer on each page to filter all visuals on that page.
- Give every visual a title that states the business question it answers, not just the data it shows.

## 6. Check your numbers

Compare the cards with the values in `data/kpi_headline.csv` and `data/kpi_yearly_summary.csv`. If they don't match, check the relationship and the filter context first.

## 7. Publish

Save the file as `dashboard/sales_kpi_dashboard.pbix` and add a screenshot of each page to `images/` for the README.
