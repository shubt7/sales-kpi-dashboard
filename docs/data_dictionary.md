# Data dictionary: sales_orders.csv

| Column | Type | Description |
|---|---|---|
| order_id | Text | Unique order identifier, e.g. ORD00001 |
| order_date | Date | Date the order was placed (2023-01-01 to 2025-12-31) |
| region | Text | Northeast, Southeast, Midwest or West |
| channel | Text | Online, Retail or Partner |
| sales_rep | Text | Sales representative ID, REP001 to REP012 |
| customer_segment | Text | SMB, Mid-Market or Enterprise |
| product | Text | Software Licence, Hardware Device, Support Plan, Training Course or Consulting Hour |
| quantity | Integer | Units sold on the order |
| unit_price | Decimal | Price per unit before discount (USD) |
| discount_pct | Decimal | Discount applied to the order, 0 to 30 |
| revenue | Decimal | Quantity × unit price, after discount (USD) |
| cost | Decimal | Cost of goods and delivery (USD) |
| profit | Decimal | Revenue minus cost (USD) |

All data is synthetic.
