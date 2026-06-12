-- AUTHOR: Rohan Joseph
-- PURPOSE: Load the derived dashboard CSVs into DuckDB tables for SQL validation and portfolio queries.
-- DATE CREATED: 2026-06-04
-- DATE MODIFIED: 2026-06-12
-- MODIFIED BY: Rohan Joseph



-- ==================================================
-- Master Occupation Dataset
-- ==================================================

-- Load the full occupation-level master sample used for descriptive app views.
CREATE OR REPLACE TABLE occupations AS
SELECT * FROM read_csv_auto('input/derived_data/occupation_analysis_dataset.csv', header = true);



-- ==================================================
-- Modeling Dataset
-- ==================================================

-- Load the complete-case modeling/display sample used for KPI, ranking, and regression-linked views.
CREATE OR REPLACE TABLE modeling_occupations AS
SELECT * FROM read_csv_auto('input/derived_data/modeling_dataset.csv', header = true);
