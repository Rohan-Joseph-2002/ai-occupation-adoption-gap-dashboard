"""
AUTHOR: Rohan Joseph
PURPOSE: Shared schema and validation settings for the AI occupation adoption-gap dashboard.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Settings
"""

REQUIRED_DERIVED_FILES = [
    "occupation_analysis_dataset.csv",
    "modeling_dataset.csv",
    "major_group_summary.csv",
    "top_gap_occupations.csv",
    "low_gap_high_capability_occupations.csv",
    "top_observed_use_occupations.csv",
    "model_coefficients.csv",
    "variable_codebook.csv",
    "source_manifest.csv",
]

ANALYSIS_DATA_COLUMNS = [
    "occ_code",
    "occupation_title",
    "major_group_code",
    "major_group_title",
    "observed_exposure",
    "theoretical_exposure",
    "human_theoretical_exposure",
    "adoption_gap_absolute",
    "observed_to_theoretical_ratio",
    "underadoption_ratio",
    "total_employment",
    "annual_mean_wage",
    "job_zone",
    "digital_information_index",
    "interpersonal_index",
    "physical_index",
    "decision_index",
    "compliance_index",
]

MODELING_DATA_EXTRA_COLUMNS = [
    "log_total_employment",
    "log_annual_mean_wage",
    "digital_information_index_z",
    "interpersonal_index_z",
    "physical_index_z",
    "decision_index_z",
    "compliance_index_z",
    "job_zone_factor",
    "regression_weight",
]

MODEL_COEFFICIENT_COLUMNS = [
    "term",
    "estimate",
    "std.error",
    "statistic",
    "p.value",
    "conf.low",
    "conf.high",
    "model_name",
    "model_label",
]

PREFERRED_MODEL_NAME = "model_3_major_group_fe"
CAPABILITY_THRESHOLD_DEFAULT = 0.50
TOP_ROLE_COUNT_DEFAULT = 15

SQL_QUERY_FILES = [
    "00_load.sql",
    "01_kpis.sql",
    "02_group_means.sql",
    "03_opportunity_rank.sql",
    "04_gap_bands.sql",
    "05_top_observed_use.sql",
]
