-- AUTHOR: Rohan Joseph
-- PURPOSE: Identify occupations where observed AI use is already highest.
-- DATE CREATED: 2026-06-04
-- DATE MODIFIED: 2026-06-12
-- MODIFIED BY: Rohan Joseph



-- ==================================================
-- Top Observed-Use Occupations
-- ==================================================

-- Sort by observed use, then theoretical exposure for stable tie-breaking.
-- This provides a contrast view to the high-adoption-gap ranking.
SELECT occupation_title,
       major_group_title,
       observed_exposure,
       theoretical_exposure,
       adoption_gap_absolute,
       underadoption_ratio,
       annual_mean_wage,
       total_employment
FROM modeling_occupations
ORDER BY observed_exposure DESC, theoretical_exposure DESC
LIMIT 15;
