# Report Build Steps

Use these steps when creating the Day 4 report from the default semantic model.

## Recommended report layout

Build one report page with these visuals:

1. card visual for `Total Sales`
2. card visual for `Order Count`
3. card visual for `Average Order Value`
4. matrix visual with `DimCustomer[Region]` on rows and the two measures `Total Sales` and `Order Count` in values

## QA checks while building the report

- confirm the unrestricted KPI cards show `4680.00`, `8`, and `585.00`
- confirm the matrix shows `East`, `North`, `South`, and `West`
- confirm the region totals match `EXPECTED_RESULTS.md`
- after RLS is enabled, use **View as** to confirm the cards and matrix change to the restricted totals
