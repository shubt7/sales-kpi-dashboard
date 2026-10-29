"""Generate a synthetic sales dataset for the KPI dashboard project.

All data is fictional. It mimics a mid-sized company selling products
through three channels across four regions, from Jan 2023 to Dec 2025.
"""
import numpy as np
import pandas as pd

SEED = 42
N_ORDERS = 6000
rng = np.random.default_rng(SEED)

regions = ["Northeast", "Southeast", "Midwest", "West"]
region_w = [0.30, 0.25, 0.20, 0.25]

channels = ["Online", "Retail", "Partner"]
channel_w = [0.45, 0.35, 0.20]

products = {
    "Software Licence": (450, 1200, 0.78),
    "Hardware Device":  (120, 480, 0.52),
    "Support Plan":     (60, 240, 0.85),
    "Training Course":  (200, 900, 0.70),
    "Consulting Hour":  (150, 300, 0.60),
}
product_names = list(products.keys())
product_w = [0.30, 0.25, 0.20, 0.10, 0.15]

reps = [f"REP{n:03d}" for n in range(1, 13)]
segments = ["SMB", "Mid-Market", "Enterprise"]
segment_w = [0.50, 0.32, 0.18]

start = pd.Timestamp("2023-01-01")
end = pd.Timestamp("2025-12-31")
days = (end - start).days

order_days = rng.integers(0, days + 1, N_ORDERS)
order_dates = start + pd.to_timedelta(order_days, unit="D")

prod = rng.choice(product_names, N_ORDERS, p=product_w)
reg = rng.choice(regions, N_ORDERS, p=region_w)
chan = rng.choice(channels, N_ORDERS, p=channel_w)
seg = rng.choice(segments, N_ORDERS, p=segment_w)
rep = rng.choice(reps, N_ORDERS)

qty = np.array([rng.integers(1, 6) if s != "Enterprise" else rng.integers(5, 40)
                for s in seg])

price_lo = np.array([products[p][0] for p in prod])
price_hi = np.array([products[p][1] for p in prod])
unit_price = rng.uniform(price_lo, price_hi).round(2)
margin = np.array([products[p][2] for p in prod])

# Discounts are larger for Partner and Enterprise deals
disc_base = np.where(chan == "Partner", 12, 4) + np.where(seg == "Enterprise", 8, 0)
discount_pct = np.clip(rng.normal(disc_base, 4), 0, 30).round(1)

gross = qty * unit_price
revenue = (gross * (1 - discount_pct / 100)).round(2)
cost = np.clip(revenue * (1 - margin + rng.normal(0, 0.03, N_ORDERS)), 0, None).round(2)
profit = (revenue - cost).round(2)

# Give the business a visible growth trend across years
years = order_dates.year.to_numpy()
year_factor = np.select([years == 2023, years == 2024],
                        [1.00, 1.12], default=1.27)
revenue = (revenue * year_factor).round(2)
cost = (cost * year_factor).round(2)
profit = (revenue - cost).round(2)

df = pd.DataFrame({
    "order_id": [f"ORD{i:05d}" for i in range(1, N_ORDERS + 1)],
    "order_date": order_dates,
    "region": reg,
    "channel": chan,
    "sales_rep": rep,
    "customer_segment": seg,
    "product": prod,
    "quantity": qty,
    "unit_price": unit_price,
    "discount_pct": discount_pct,
    "revenue": revenue,
    "cost": cost,
    "profit": profit,
}).sort_values("order_date").reset_index(drop=True)

df.to_csv("data/sales_orders.csv", index=False)
print(f"Wrote {len(df):,} rows to data/sales_orders.csv")
