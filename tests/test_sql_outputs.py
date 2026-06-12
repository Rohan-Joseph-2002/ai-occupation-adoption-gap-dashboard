"""
AUTHOR: Rohan Joseph
PURPOSE: Test DuckDB SQL outputs against dashboard answer-key data.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os
import sys
from pathlib import Path


"""
Settings
"""

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# --- Import project-specific utilities and pipeline code ---
from dashboard.data import load_derived_dataframe
from dashboard.metrics import build_gap_band_dataframe, build_kpi_summary
from dashboard.sql import compare_frames, connect_database, initialize_database, run_query_file



"""
Tests
"""

def test_kpi_sql_matches_modeling_dataset() -> None:
    """
    Verify that the KPI SQL query matches pandas-computed modeling-sample metrics.
    This keeps the headline dashboard values aligned across SQL and Python paths.
    """

    os.chdir(REPO_ROOT)
    connection = connect_database()
    initialize_database(connection)
    actual_df = run_query_file(connection, "01_kpis.sql")
    expected_metrics = build_kpi_summary(load_derived_dataframe("modeling_dataset.csv"))

    assert int(actual_df.loc[0, "n_occupations"]) == expected_metrics["n_occupations"]
    assert float(actual_df.loc[0, "mean_observed_exposure"]) == expected_metrics["mean_observed_exposure"]
    assert float(actual_df.loc[0, "mean_theoretical_exposure"]) == expected_metrics["mean_theoretical_exposure"]
    assert float(actual_df.loc[0, "mean_adoption_gap"]) == expected_metrics["mean_adoption_gap"]
    assert float(actual_df.loc[0, "median_adoption_gap"]) == expected_metrics["median_adoption_gap"]


def test_group_means_sql_matches_answer_key() -> None:
    """
    Verify that the major-group SQL query matches the upstream answer-key CSV.
    This keeps the grouped dashboard view aligned with the analysis repo output.
    """

    os.chdir(REPO_ROOT)
    connection = connect_database()
    initialize_database(connection)
    actual_df = run_query_file(connection, "02_group_means.sql")
    expected_df = load_derived_dataframe("major_group_summary.csv")
    passed, detail = compare_frames(
        actual_df = actual_df,
        expected_df = expected_df,
        join_columns = ["major_group_code", "major_group_title"],
        value_columns = [
            "occupation_count",
            "mean_observed_exposure",
            "mean_theoretical_exposure",
            "mean_adoption_gap",
            "mean_underadoption_ratio",
        ],
    )

    assert passed, detail


def test_gap_bands_sql_matches_pandas_expected_output() -> None:
    """
    Verify that the gap-band SQL query matches independently computed pandas output.
    This protects the quartile and label logic, not just the returned row count.
    """

    os.chdir(REPO_ROOT)
    connection = connect_database()
    initialize_database(connection)
    actual_df = run_query_file(connection, "04_gap_bands.sql")
    expected_df = build_gap_band_dataframe(load_derived_dataframe("modeling_dataset.csv"))

    merged_df = expected_df.merge(
        actual_df,
        on = ["occupation_title", "major_group_title"],
        how = "outer",
        suffixes = ("_expected", "_actual"),
        indicator = True,
    )

    assert merged_df[merged_df["_merge"] != "both"].empty
    assert merged_df[
        (
            merged_df["adoption_gap_absolute_expected"]
            - merged_df["adoption_gap_absolute_actual"]
        ).abs()
        > 1e-9
    ].empty
    assert merged_df[
        merged_df["gap_quartile_expected"] != merged_df["gap_quartile_actual"]
    ].empty
    assert merged_df[
        merged_df["gap_band_expected"] != merged_df["gap_band_actual"]
    ].empty
