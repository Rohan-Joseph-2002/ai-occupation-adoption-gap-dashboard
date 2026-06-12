-- AUTHOR: Rohan Joseph
-- PURPOSE: Assign adoption-gap quartiles and plain-language gap bands.
-- DATE CREATED: 2026-06-04
-- DATE MODIFIED: 2026-06-12
-- MODIFIED BY: Rohan Joseph



-- ==================================================
-- Gap Bands
-- ==================================================

-- Use NTILE for quartile practice and CASE for interpretable threshold labels.
SELECT occupation_title,
       major_group_title,
       adoption_gap_absolute,
       NTILE(4) OVER (ORDER BY adoption_gap_absolute, occupation_title, major_group_title) AS gap_quartile,
       CASE WHEN adoption_gap_absolute >= 0.6 THEN 'Severe'
            WHEN adoption_gap_absolute >= 0.4 THEN 'High'
            WHEN adoption_gap_absolute >= 0.2 THEN 'Moderate'
            ELSE 'Low' END AS gap_band
FROM modeling_occupations;
