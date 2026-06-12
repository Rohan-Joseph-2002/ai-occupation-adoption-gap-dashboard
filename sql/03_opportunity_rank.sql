-- AUTHOR: Rohan Joseph
-- PURPOSE: Rank high-capability occupations by adoption gap for the opportunity-role view.
-- DATE CREATED: 2026-06-04
-- DATE MODIFIED: 2026-06-12
-- MODIFIED BY: Rohan Joseph



-- ==================================================
-- High-Capability Eligible Occupations
-- ==================================================

-- Restrict to occupations where theoretical capability is at least 0.5.
-- This mirrors the paper's high-capability lens before ranking adoption gaps.
WITH eligible AS (
    SELECT occupation_title,
           major_group_title,
           theoretical_exposure,
           observed_exposure,
           adoption_gap_absolute,
           underadoption_ratio,
           annual_mean_wage,
           total_employment
    FROM modeling_occupations
    WHERE theoretical_exposure >= 0.5
)



-- ==================================================
-- Opportunity Ranking
-- ==================================================

-- Rank overall opportunity and within-family opportunity using window functions.
SELECT occupation_title,
       major_group_title,
       observed_exposure,
       theoretical_exposure,
       adoption_gap_absolute,
       underadoption_ratio,
       annual_mean_wage,
       total_employment,
       RANK() OVER (ORDER BY adoption_gap_absolute DESC)                                AS opportunity_rank,
       RANK() OVER (PARTITION BY major_group_title ORDER BY adoption_gap_absolute DESC) AS rank_in_family
FROM eligible
ORDER BY adoption_gap_absolute DESC
LIMIT 15;
