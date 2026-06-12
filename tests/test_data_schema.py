"""
AUTHOR: Rohan Joseph
PURPOSE: Test required dashboard input files and core CSV schemas.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import sys
from pathlib import Path

import pandas as pd


"""
Settings
"""

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# --- Import project-specific utilities and pipeline code ---
from project.settings import ANALYSIS_DATA_COLUMNS, MODELING_DATA_EXTRA_COLUMNS, REQUIRED_DERIVED_FILES



"""
Tests
"""

def test_required_derived_files_exist() -> None:
    """
    Verify that every dashboard-ready derived input file is present.
    This catches incomplete repository copies before schema-level tests run.
    """

    missing_files = [
        file_name
        for file_name in REQUIRED_DERIVED_FILES
        if not (REPO_ROOT / "input" / "derived_data" / file_name).exists()
    ]

    assert missing_files == []


def test_analysis_dataset_schema_and_rows() -> None:
    """
    Verify the master occupation dataset row count and column order.
    This protects the dashboard's descriptive views from upstream schema drift.
    """

    dataset_path = REPO_ROOT / "input" / "derived_data" / "occupation_analysis_dataset.csv"
    dataframe = pd.read_csv(dataset_path)

    assert len(dataframe) == 709
    assert list(dataframe.columns) == ANALYSIS_DATA_COLUMNS


def test_modeling_dataset_schema_and_rows() -> None:
    """
    Verify the modeling/display dataset row count and column order.
    This protects the dashboard's KPI, ranking, and SQL validation views.
    """

    dataset_path = REPO_ROOT / "input" / "derived_data" / "modeling_dataset.csv"
    dataframe = pd.read_csv(dataset_path)

    assert len(dataframe) == 693
    assert list(dataframe.columns) == ANALYSIS_DATA_COLUMNS + MODELING_DATA_EXTRA_COLUMNS
