-- AUTHOR: Rohan Joseph
-- PURPOSE: Reproduce major-group mean exposure and adoption-gap statistics.
-- DATE CREATED: 2026-06-04
-- DATE MODIFIED: 2026-06-12
-- MODIFIED BY: Rohan Joseph



-- ==================================================
-- Major-Group Means
-- ==================================================

-- Aggregate the full occupation master dataset to one row per SOC major group.
-- These columns are validated against major_group_summary.csv from the analysis repo.
SELECT major_group_code,
       major_group_title,
       COUNT(*)                             AS occupation_count,
       AVG(observed_exposure)               AS mean_observed_exposure,
       AVG(theoretical_exposure)            AS mean_theoretical_exposure,
       AVG(adoption_gap_absolute)           AS mean_adoption_gap,
       AVG(underadoption_ratio)             AS mean_underadoption_ratio
FROM occupations
GROUP BY major_group_code, major_group_title
ORDER BY mean_adoption_gap DESC;
