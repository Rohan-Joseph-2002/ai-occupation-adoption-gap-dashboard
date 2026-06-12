"""
AUTHOR: Rohan Joseph
PURPOSE: Validate dashboard SQL outputs against R-produced answer-key CSVs.
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

"""
Settings
"""

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


# --- Import project-specific utilities and pipeline code ---
from dashboard.data import load_derived_dataframe  # type: ignore
from dashboard.metrics import build_gap_band_dataframe, build_kpi_summary  # type: ignore
from dashboard.sql import compare_frames, connect_database, initialize_database, run_query_file  # type: ignore
from project.logger import capture_script_console_to_markdown  # type: ignore
from project.paths import ensure_project_directories  # type: ignore
from project.utils import print_section_header, print_stage_banner, print_status  # type: ignore



"""
Script
"""

def validate_kpis(connection) -> bool:
    """
    Validate the KPI SQL output against pandas-computed modeling-sample metrics.
    This checks the dashboard headline query.
    """

    actual_df = run_query_file(connection, "01_kpis.sql")
    modeling_df = load_derived_dataframe("modeling_dataset.csv")
    expected_metrics = build_kpi_summary(modeling_df)
    actual_metrics = actual_df.iloc[0].to_dict()

    checks = {
        "n_occupations": int(actual_metrics["n_occupations"]) == expected_metrics["n_occupations"],
        "mean_observed_exposure": float(actual_metrics["mean_observed_exposure"]) == expected_metrics["mean_observed_exposure"],
        "mean_theoretical_exposure": float(actual_metrics["mean_theoretical_exposure"]) == expected_metrics["mean_theoretical_exposure"],
        "mean_adoption_gap": float(actual_metrics["mean_adoption_gap"]) == expected_metrics["mean_adoption_gap"],
        "median_adoption_gap": float(actual_metrics["median_adoption_gap"]) == expected_metrics["median_adoption_gap"],
    }

    for check_name, passed in checks.items():
        print_status(f"{check_name}: {'passed' if passed else 'failed'}")

    return all(checks.values())


def validate_group_means(connection) -> bool:
    """
    Validate the major-group SQL output against major_group_summary.csv.
    This checks the dumbbell view's grouped statistics.
    """

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
    print_status(f"group means: {'passed' if passed else 'failed'} ({detail})")
    print_status(f"rows expected: {len(expected_df)}; rows returned: {len(actual_df)}")
    return passed


def validate_top_gap(connection) -> bool:
    """
    Validate the opportunity-rank SQL output against top_gap_occupations.csv.
    This checks the highest-opportunity roles view.
    """

    actual_df = run_query_file(connection, "03_opportunity_rank.sql")
    expected_df = load_derived_dataframe("top_gap_occupations.csv")
    passed, detail = compare_frames(
        actual_df = actual_df,
        expected_df = expected_df,
        join_columns = ["occupation_title", "major_group_title"],
        value_columns = [
            "observed_exposure",
            "theoretical_exposure",
            "adoption_gap_absolute",
            "underadoption_ratio",
            "annual_mean_wage",
            "total_employment",
        ],
    )
    print_status(f"top gap occupations: {'passed' if passed else 'failed'} ({detail})")
    print_status(f"rows expected: {len(expected_df)}; rows returned: {len(actual_df)}")
    return passed


def validate_top_observed_use(connection) -> bool:
    """
    Validate the observed-use SQL output against top_observed_use_occupations.csv.
    This checks the already-embedded AI use view.
    """

    actual_df = run_query_file(connection, "05_top_observed_use.sql")
    expected_df = load_derived_dataframe("top_observed_use_occupations.csv")
    passed, detail = compare_frames(
        actual_df = actual_df,
        expected_df = expected_df,
        join_columns = ["occupation_title", "major_group_title"],
        value_columns = [
            "observed_exposure",
            "theoretical_exposure",
            "adoption_gap_absolute",
            "underadoption_ratio",
            "annual_mean_wage",
            "total_employment",
        ],
    )
    print_status(f"top observed-use occupations: {'passed' if passed else 'failed'} ({detail})")
    print_status(f"rows expected: {len(expected_df)}; rows returned: {len(actual_df)}")
    return passed


def validate_gap_bands(connection) -> bool:
    """
    Validate that the gap-band query matches pandas-computed quartiles and labels.
    This checks the NTILE/CASE practice query.
    """

    actual_df = run_query_file(connection, "04_gap_bands.sql")
    modeling_df = load_derived_dataframe("modeling_dataset.csv")
    expected_df = build_gap_band_dataframe(modeling_df)

    merged_df = expected_df.merge(
        actual_df,
        on = ["occupation_title", "major_group_title"],
        how = "outer",
        suffixes = ("_expected", "_actual"),
        indicator = True,
    )

    missing_rows = merged_df[merged_df["_merge"] != "both"]
    gap_value_mismatches = merged_df[
        (merged_df["_merge"] == "both")
        & (
            (
                merged_df["adoption_gap_absolute_expected"]
                - merged_df["adoption_gap_absolute_actual"]
            ).abs()
            > 1e-9
        )
    ]
    quartile_mismatches = merged_df[
        (merged_df["_merge"] == "both")
        & (merged_df["gap_quartile_expected"] != merged_df["gap_quartile_actual"])
    ]
    band_mismatches = merged_df[
        (merged_df["_merge"] == "both")
        & (merged_df["gap_band_expected"] != merged_df["gap_band_actual"])
    ]

    passed = (
        len(missing_rows) == 0
        and len(gap_value_mismatches) == 0
        and len(quartile_mismatches) == 0
        and len(band_mismatches) == 0
    )

    print_status(f"gap bands: {'passed' if passed else 'failed'}")
    print_status(f"rows expected: {len(expected_df)}; rows returned: {len(actual_df)}")
    print_status(f"unmatched rows: {len(missing_rows)}")
    print_status(f"gap-value mismatches: {len(gap_value_mismatches)}")
    print_status(f"quartile mismatches: {len(quartile_mismatches)}")
    print_status(f"band mismatches: {len(band_mismatches)}")
    return passed


def run_validation() -> None:
    """
    Run the full SQL validation workflow.
    This logs each query check and fails if any dashboard SQL output drifts from the answer keys.
    """

    os.chdir(PROJECT_ROOT)
    ensure_project_directories()

    print_stage_banner("Validating AI Occupation Adoption-Gap Dashboard SQL")

    connection = connect_database()
    initialize_database(connection)

    print_section_header("Validation Checks")
    checks = [
        validate_kpis(connection),
        validate_group_means(connection),
        validate_top_gap(connection),
        validate_gap_bands(connection),
        validate_top_observed_use(connection),
    ]

    print_section_header("Status")
    if not all(checks):
        raise RuntimeError("One or more SQL validation checks failed.")

    print_status("All SQL validation checks passed.")


def main() -> None:
    """
    Run SQL validation with Markdown logging.
    This gives the script one predictable command-line entrypoint.
    """

    capture_script_console_to_markdown(
        run_callable = run_validation,
        output_dir = os.path.join(PROJECT_ROOT, "output", "logs"),
        script_name = "002_validate_sql",
    )


if __name__ == "__main__":
    main()
