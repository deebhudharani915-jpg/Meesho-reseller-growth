import csv, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "meesho_reseller.db"
OUT = ROOT / "part1_sql" / "output"
OUT.mkdir(exist_ok=True)

queries = {
    "monthly_category_revenue.csv": """SELECT month, category, ROUND(SUM(quantity * unit_price), 2) AS revenue, COUNT(*) AS n_orders
        FROM orders GROUP BY month, category
        ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END,
        CASE category WHEN 'Ethnic Wear' THEN 1 WHEN 'Western Wear' THEN 2 WHEN 'Kids Wear' THEN 3 WHEN 'Home & Kitchen' THEN 4 WHEN 'Beauty & Personal Care' THEN 5 END""",
    "region_revenue.csv": """SELECT r.region, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue, COUNT(*) AS n_orders
        FROM orders o JOIN resellers r ON r.reseller_id=o.reseller_id GROUP BY r.region ORDER BY total_revenue DESC""",
    "top_resellers.csv": """SELECT r.reseller_id, r.reseller_name, r.region, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
        FROM orders o JOIN resellers r ON r.reseller_id=o.reseller_id GROUP BY r.reseller_id, r.reseller_name, r.region
        HAVING total_spend > 50000 ORDER BY total_spend DESC LIMIT 5""",
    "inactive_resellers.csv": """SELECT r.reseller_id, r.reseller_name, r.region FROM resellers r LEFT JOIN orders o ON o.reseller_id=r.reseller_id WHERE o.order_id IS NULL""",
    "left_join_count_demo.csv": """SELECT r.reseller_id, r.reseller_name, COUNT(*) AS count_star, COUNT(o.order_id) AS count_order_id
        FROM resellers r LEFT JOIN orders o ON o.reseller_id=r.reseller_id WHERE r.reseller_id='RS024'
        GROUP BY r.reseller_id, r.reseller_name""",
    "june_delivered_aov.csv": """SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov FROM orders WHERE month='June' AND status='Delivered'""",
}

with sqlite3.connect(DB) as conn:
    for filename, sql in queries.items():
        rows = conn.execute(sql).fetchall()
        headers = [d[0] for d in conn.execute(sql).description]
        with open(OUT / filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f); writer.writerow(headers); writer.writerows(rows)
print(f"Wrote {len(queries)} query outputs to {OUT}")
