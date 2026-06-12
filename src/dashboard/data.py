"""
AUTHOR: Rohan Joseph
PURPOSE: Data-loading helpers for the AI occupation adoption-gap dashboard.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os

import pandas as pd


# --- Import project-specific utilities and pipeline code ---
from project.paths import DERIVED_DATA_DIR
from project.settings import REQUIRED_DERIVED_FILES



"""
Functions
"""

def derived_file_path(file_name: str) -> str:
    """
    Return the path for one dashboard derived-data file.
    This keeps all app and script reads tied to one directory convention.
    """

    return os.path.join(DERIVED_DATA_DIR, file_name)


def load_derived_dataframe(file_name: str, **kwargs) -> pd.DataFrame:
    """
    Load one dashboard derived-data CSV.
    This keeps pandas reads concise and consistent.
    """

    return pd.read_csv(derived_file_path(file_name), **kwargs)


def load_dashboard_inputs() -> dict[str, pd.DataFrame]:
    """
    Load all derived CSV inputs used by the dashboard and SQL validation.
    This is the single high-level data loader for app/script use.
    """

    return {
        file_name.replace(".csv", ""): load_derived_dataframe(file_name)
        for file_name in REQUIRED_DERIVED_FILES
    }


def list_missing_derived_files() -> list[str]:
    """
    Return required dashboard input files that are not present.
    This helps checks and tests fail with a concrete missing-file list.
    """

    return [
        file_name
        for file_name in REQUIRED_DERIVED_FILES
        if not os.path.exists(derived_file_path(file_name))
    ]
