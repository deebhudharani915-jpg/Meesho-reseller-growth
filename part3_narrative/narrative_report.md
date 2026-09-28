# Part 3.2 — Worked Narrative Report

## May — Ethnic Wear

**Context:** This measures Ethnic Wear monthly revenue for **May versus April** using the verified Part 1 monthly-category revenue feed.

**Insight (fact):** Ethnic Wear recorded **77.1%** MoM growth in May versus April, so the Part 2 rule classified it as **flagged**.

**Implication (hypothesis):** Confirm whether the May movement was associated with assortment availability, pricing, or order-volume changes by reviewing the category's May operating details before deciding on the next commercial action.

### Self-score
- **Specificity:** Pass — the narrative names Ethnic Wear, May, April, and the exact 77.1% result.
- **Audience fit:** Pass — it gives a regional manager a concise business signal and next action without implementation detail.
- **Completeness:** Pass — Context, Insight, and Implication are all present and clearly labeled.
- **Actionability:** Pass — the next step is to review assortment, pricing, and order-volume drivers before taking action.

## June — Ethnic Wear

**Context:** This measures Ethnic Wear monthly revenue for **June versus May** using the verified Part 1 monthly-category revenue feed.

**Insight (fact):** Ethnic Wear recorded **-58.74%** MoM change in June versus May, so the Part 2 rule classified it as **flagged** in the opposite direction from May.

**Implication (hypothesis):** Check June assortment availability, pricing changes, and order-volume movement against May first; if a material operational or commercial change is confirmed, address that driver before planning the next category action.

### Self-score
- **Specificity:** Pass — the narrative names Ethnic Wear, June, May, and the exact -58.74% result.
- **Audience fit:** Pass — the message is framed for a regional manager and focuses on business follow-up rather than code or implementation.
- **Completeness:** Pass — Context, Insight, and Implication are all present and clearly labeled.
- **Actionability:** Pass — the next step identifies concrete June-versus-May checks and a follow-up action if a driver is confirmed.

# Part 3.3 — Chart-choice Justification

## 1. Which month had the highest total revenue?
Use a **vertical bar/column chart**. This is primarily a univariate comparison of one measure (total revenue) across one dimension (month), so bars make the three monthly values easy to compare within 10 seconds. The y-axis should start at zero, there is no need for a legend because there is one series, and 3D should be avoided. The verified values are April INR 419417.43, May INR 444594.25, and June INR 398055.24.

## 2. What percentage share does Ethnic Wear represent of April's total revenue?
Use a **100% stacked bar or a simple share/donut chart**, with the preferred choice being a **100% stacked bar** for a precise business comparison. This is a univariate composition question about one month's total, not a time trend; the single bar can show Ethnic Wear's share against the remainder. The verified Ethnic Wear revenue is INR 104520.77 out of April's INR 419417.43, equal to **24.92%**. Keep the message readable within 10 seconds, avoid 3D, and do not add a legend unless multiple series/categories require it.

## 3. How do the four regions compare on total revenue?
Use a **horizontal bar chart**. This is a univariate comparison of total revenue across the region dimension; four bars provide a direct ranking without introducing unnecessary multivariate encoding. Start the revenue axis at zero, use direct labels where possible, avoid 3D, and omit a legend because each bar represents one region in the same measure. The verified figures are North INR 337125.46, West INR 333106.33, South INR 316736.68, and East INR 275098.45.

# Part 3.4 — Masking Policy and Top-Reseller Narrative

External-facing narrative must never contain a raw reseller name. The approved aliases are derived only from reseller IDs.

**Top-reseller narrative:** The monitored top-spend resellers include **West — ALIAS-19**, **West — ALIAS-22**, **South — ALIAS-12**, **North — ALIAS-06**, and **North — ALIAS-05**. This narrative deliberately reports only region and alias, not raw reseller names.

The five source records are the Part 1 `HAVING total_spend > 50000` results for RS019, RS022, RS012, RS006, and RS005. No raw reseller name is used in the external-facing narrative.

**Masking checks:**
- `alias_for("RS019") == "ALIAS-19"` → `True`
- `assert_no_raw_names_leak(final_narrative, reseller_names)` → `True`
- `assert_no_raw_names_leak("West — Mumbai Reseller 1.", reseller_names)` → `False`
