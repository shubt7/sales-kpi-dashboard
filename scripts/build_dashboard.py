"""Build a self-contained interactive dashboard from data/sales_orders.csv.

Run from the project root:  python3 scripts/build_dashboard.py
Writes docs/index.html (open it in any browser, or host it on GitHub Pages).
"""
import json
import pandas as pd

df = pd.read_csv("data/sales_orders.csv", parse_dates=["order_date"])
rows = [
    [r.order_date.strftime("%Y-%m-%d"), r.region, r.channel, r.sales_rep,
     r.customer_segment, r.product, float(r.discount_pct), float(r.revenue), float(r.profit)]
    for r in df.itertuples()
]
payload = json.dumps({
    "cols": ["date", "region", "channel", "rep", "segment", "product", "discount", "revenue", "profit"],
    "rows": rows,
}, separators=(",", ":"))

with open("scripts/dashboard_template.html", encoding="utf-8") as f:
    html = f.read().replace("__DATA__", payload)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"Wrote docs/index.html with {len(rows):,} orders")
