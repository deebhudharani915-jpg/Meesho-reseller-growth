# Part 1 SQL Outputs

The CSV files in this folder are generated from `data/meesho_reseller.db` by `part1_sql/run_queries.py`.

For the zero-order reseller demonstration, `COUNT(*)` is 1 because a `LEFT JOIN` preserves the reseller row even when no order matches. `COUNT(order_id)` is 0 because the joined `order_id` is NULL. Therefore `COUNT(order_id)`, not `COUNT(*)`, is the correct test for zero matching orders.
