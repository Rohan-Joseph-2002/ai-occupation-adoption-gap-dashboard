-- AUTHOR: Rohan Joseph
-- PURPOSE: Build headline KPI metrics for the AI occupation adoption-gap dashboard.
-- DATE CREATED: 2026-06-04
-- DATE MODIFIED: 2026-06-12
-- MODIFIED BY: Rohan Joseph



-- ==================================================
-- Dashboard KPI Band
-- ==================================================

-- Use the complete-case modeling sample so the KPI count matches the regression/display sample.
SELECT COUNT(*)                                AS n_occupations,
       ROUND(AVG(observed_exposure), 3)        AS mean_observed_exposure,
       ROUND(AVG(theoretical_exposure), 3)     AS mean_theoretical_exposure,
       ROUND(AVG(adoption_gap_absolute), 3)    AS mean_adoption_gap,
       ROUND(MEDIAN(adoption_gap_absolute), 3) AS median_adoption_gap
FROM modeling_occupations;
