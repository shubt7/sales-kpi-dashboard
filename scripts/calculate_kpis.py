"""Calculate the sales KPIs shown in the dashboard and save summary tables.

Run from the project root:  python3 scripts/calculate_kpis.py
Reads  data/sales_orders.csv
Writes data/kpi_*.csv and images/*.png
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("data/sales_orders.csv", parse_dates=["order_date"])
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()

# ---- Headline KPIs -------------------------------------------------------
total_rev = df["revenue"].sum()
total_profit = df["profit"].sum()
margin_pct = total_profit / total_rev * 100
orders = len(df)
aov = total_rev / orders

yearly = df.groupby("year").agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    orders=("order_id", "count"),
)
yearly["profit_margin_pct"] = yearly["profit"] / yearly["revenue"] * 100
yearly["revenue_growth_pct"] = yearly["revenue"].pct_change() * 100
yearly.round(2).to_csv("data/kpi_yearly_summary.csv")

kpis = pd.DataFrame({
    "KPI": ["Total revenue", "Total profit", "Profit margin %", "Orders", "Average order value"],
    "Value": [round(total_rev, 2), round(total_profit, 2), round(margin_pct, 2), orders, round(aov, 2)],
})
kpis.to_csv("data/kpi_headline.csv", index=False)

# ---- Monthly trend -------------------------------------------------------
monthly = df.groupby("month").agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
monthly["revenue_3m_avg"] = monthly["revenue"].rolling(3).mean()
monthly.round(2).to_csv("data/kpi_monthly_trend.csv")

# ---- Region, channel and product breakdowns ------------------------------
def breakdown(col):
    t = df.groupby(col).agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "count"))
    t["share_of_revenue_pct"] = t["revenue"] / t["revenue"].sum() * 100
    t["profit_margin_pct"] = t["profit"] / t["revenue"] * 100
    return t.sort_values("revenue", ascending=False).round(2)

breakdown("region").to_csv("data/kpi_by_region.csv")
breakdown("channel").to_csv("data/kpi_by_channel.csv")
breakdown("product").to_csv("data/kpi_by_product.csv")

# ---- Sales rep leaderboard -----------------------------------------------
reps = breakdown("sales_rep")
reps.to_csv("data/kpi_by_sales_rep.csv")

# ---- Discount impact: do deeper discounts still earn profit? -------------
df["discount_band"] = pd.cut(df["discount_pct"], [-0.1, 5, 10, 20, 30],
                             labels=["0-5%", "5-10%", "10-20%", "20-30%"])
disc = df.groupby("discount_band", observed=True).agg(
    orders=("order_id", "count"),
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
)
disc["profit_margin_pct"] = disc["profit"] / disc["revenue"] * 100
disc.round(2).to_csv("data/kpi_discount_bands.csv")

# ---- Charts for the README ----------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")
navy, teal = "#1d4e89", "#14b8a6"

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(monthly.index, monthly["revenue"] / 1000, color=navy, lw=1.6, label="Monthly revenue")
ax.plot(monthly.index, monthly["revenue_3m_avg"] / 1000, color=teal, lw=2.6, label="3-month average")
ax.set_title("Monthly revenue trend (USD thousands)", loc="left", fontweight="bold")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig("images/01_monthly_revenue_trend.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 4.5))
r = breakdown("region")
ax.barh(r.index[::-1], r["revenue"][::-1] / 1000, color=navy)
ax.set_title("Revenue by region (USD thousands)", loc="left", fontweight="bold")
fig.tight_layout()
fig.savefig("images/02_revenue_by_region.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 4.5))
p = breakdown("product")
ax.bar(p.index, p["profit_margin_pct"], color=teal)
ax.set_title("Profit margin by product (%)", loc="left", fontweight="bold")
ax.tick_params(axis="x", rotation=20)
fig.tight_layout()
fig.savefig("images/03_margin_by_product.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(disc.index.astype(str), disc["profit_margin_pct"], color=[navy, navy, teal, "#e07a5f"])
ax.set_title("Profit margin by discount band (%)", loc="left", fontweight="bold")
fig.tight_layout()
fig.savefig("images/04_margin_by_discount.png", dpi=150)
plt.close(fig)

print(kpis.to_string(index=False))
print()
print(yearly[["revenue", "profit_margin_pct", "revenue_growth_pct"]].round(1).to_string())
print()
print(disc[["orders", "profit_margin_pct"]].round(1).to_string())
