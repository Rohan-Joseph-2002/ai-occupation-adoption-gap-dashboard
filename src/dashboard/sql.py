"""
AUTHOR: Rohan Joseph
PURPOSE: DuckDB SQL execution and validation helpers for the AI occupation adoption-gap dashboard.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os
from dataclasses import dataclass

import duckdb
import pandas as pd


# --- Import project-specific utilities and pipeline code ---
from project.paths import DERIVED_DATA_DIR, SQL_DIR



"""
Classes
"""

@dataclass(frozen = True)
class SqlValidationResult:
    """
    Container for one SQL validation check.
    This makes validation script output predictable and testable.
    """

    query_name: str
    expected_rows: int
    actual_rows: int
    passed: bool
    detail: str



"""
Functions
"""

def read_sql_file(file_name: str) -> str:
    """
    Read one SQL file from the repo's SQL directory.
    This keeps query file access centralized.
    """

    with open(os.path.join(SQL_DIR, file_name), "r", encoding = "utf-8") as handle:
        return handle.read()


def sql_string_literal(value: str) -> str:
    """
    Return a SQL-safe single-quoted string literal.
    This lets Python resolve repository paths while keeping the SQL files readable.
    """

    return "'" + value.replace("'", "''") + "'"


def resolve_load_sql_paths(sql_text: str) -> str:
    """
    Replace repo-relative CSV paths in the load SQL with absolute paths.
    This lets SQL initialization work from notebooks, tests, scripts, and imported use.
    """

    replacements = {
        "'input/derived_data/occupation_analysis_dataset.csv'": sql_string_literal(
            os.path.join(DERIVED_DATA_DIR, "occupation_analysis_dataset.csv")
        ),
        "'input/derived_data/modeling_dataset.csv'": sql_string_literal(
            os.path.join(DERIVED_DATA_DIR, "modeling_dataset.csv")
        ),
    }

    for relative_path, absolute_path in replacements.items():
        sql_text = sql_text.replace(relative_path, absolute_path)

    return sql_text


def connect_database() -> duckdb.DuckDBPyConnection:
    """
    Create an in-memory DuckDB connection.
    Scripts and tests run from the project root so SQL file paths resolve consistently.
    """

    return duckdb.connect(database = ":memory:")


def initialize_database(connection: duckdb.DuckDBPyConnection) -> None:
    """
    Load the dashboard CSV inputs into DuckDB tables.
    This executes the repo's canonical load script.
    """

    connection.execute(resolve_load_sql_paths(read_sql_file("00_load.sql")))


def run_query_file(connection: duckdb.DuckDBPyConnection, file_name: str) -> pd.DataFrame:
    """
    Execute one SQL query file and return its result as a DataFrame.
    This is used by validation scripts, tests, and notebook checks.
    """

    return connection.execute(read_sql_file(file_name)).fetchdf()


def compare_frames(
    actual_df: pd.DataFrame,
    expected_df: pd.DataFrame,
    join_columns: list[str],
    value_columns: list[str],
    tolerance: float = 1e-9,
) -> tuple[bool, str]:
    """
    Compare two DataFrames on selected join and numeric value columns.
    This keeps SQL validation focused on the view-level outputs that matter.
    """

    actual_subset = actual_df[join_columns + value_columns].copy()
    expected_subset = expected_df[join_columns + value_columns].copy()

    merged_df = expected_subset.merge(
        actual_subset,
        on = join_columns,
        how = "outer",
        suffixes = ("_expected", "_actual"),
        indicator = True,
    )

    missing_rows = merged_df[merged_df["_merge"] != "both"]

    if len(missing_rows) > 0:
        return False, f"Row-key mismatch: {len(missing_rows)} unmatched rows"

    for column_name in value_columns:
        expected_values = merged_df[f"{column_name}_expected"]
        actual_values = merged_df[f"{column_name}_actual"]
        max_difference = (expected_values - actual_values).abs().max()

        if pd.notna(max_difference) and float(max_difference) > tolerance:
            return False, f"{column_name} max difference {max_difference}"

    return True, "matched"
