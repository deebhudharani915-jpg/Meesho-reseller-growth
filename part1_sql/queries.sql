-- Part 1: Meesho Reseller Growth & Alert Intelligence Pipeline
-- Run against data/meesho_reseller.db.

-- Q1: Monthly revenue by category.
SELECT month, category,
       ROUND(SUM(quantity * unit_price), 2) AS revenue,
       COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END,
         CASE category WHEN 'Ethnic Wear' THEN 1 WHEN 'Western Wear' THEN 2
                       WHEN 'Kids Wear' THEN 3 WHEN 'Home & Kitchen' THEN 4
                       WHEN 'Beauty & Personal Care' THEN 5 END;

-- Q2: Region-wise total revenue and order count.
SELECT r.region,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
       COUNT(*) AS n_orders
FROM orders o
JOIN resellers r ON r.reseller_id = o.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;

-- Q3: Top resellers by total spend, restricted by HAVING > 50000.
SELECT r.reseller_id, r.reseller_name, r.region,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name, r.region
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- Q4a: Resellers who have never placed an order.
SELECT r.reseller_id, r.reseller_name, r.region
FROM resellers r
LEFT JOIN orders o ON o.reseller_id = r.reseller_id
WHERE o.order_id IS NULL;

-- Q4b: Demonstrate COUNT(*) versus COUNT(order_id) for the zero-match LEFT JOIN row.
-- COUNT(*) counts the preserved reseller row as 1; COUNT(order_id) counts only
-- non-NULL order IDs, so it correctly reports 0 matching orders.
SELECT r.reseller_id, r.reseller_name,
       COUNT(*) AS count_star,
       COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o ON o.reseller_id = r.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id, r.reseller_name;

-- Q5: June AOV for Delivered orders only.
SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov
FROM orders
WHERE month = 'June' AND status = 'Delivered';
