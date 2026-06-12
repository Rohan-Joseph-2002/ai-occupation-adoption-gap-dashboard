"""
AUTHOR: Rohan Joseph
PURPOSE: Project path definitions and directory bootstrapping helpers for the AI occupation adoption-gap dashboard.
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



"""
Settings
"""

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INPUT_DIR = os.path.join(PROJECT_ROOT, "input")
DERIVED_DATA_DIR = os.path.join(INPUT_DIR, "derived_data")
REFERENCE_DIR = os.path.join(INPUT_DIR, "reference")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
SCREENSHOTS_DIR = os.path.join(OUTPUT_DIR, "screenshots")
EXPORTS_DIR = os.path.join(OUTPUT_DIR, "exports")
LOG_DIR = os.path.join(OUTPUT_DIR, "logs")
SQL_DIR = os.path.join(PROJECT_ROOT, "sql")
APP_DIR = os.path.join(PROJECT_ROOT, "app")
NOTEBOOKS_DIR = os.path.join(PROJECT_ROOT, "notebooks")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")



"""
Classes
"""

@dataclass(frozen = True)
class ProjectPaths:
    """
    Container for filesystem locations used across the repository.
    This keeps path resolution in one place so scripts and the app use the same locations.
    """

    input_dir: str
    derived_data_dir: str
    reference_dir: str
    output_dir: str
    screenshots_dir: str
    exports_dir: str
    log_dir: str
    sql_dir: str
    app_dir: str
    notebooks_dir: str
    tests_dir: str



"""
Functions
"""

def ensure_project_directories() -> ProjectPaths:
    """
    Create the standard project directories if they do not already exist.
    This helps guarantee that scripts and app runs can write outputs without repeated boilerplate.
    """

    for directory in [
        INPUT_DIR,
        DERIVED_DATA_DIR,
        REFERENCE_DIR,
        OUTPUT_DIR,
        SCREENSHOTS_DIR,
        EXPORTS_DIR,
        LOG_DIR,
        SQL_DIR,
        APP_DIR,
        NOTEBOOKS_DIR,
        TESTS_DIR,
    ]:
        os.makedirs(directory, exist_ok = True)

    return ProjectPaths(
        input_dir = INPUT_DIR,
        derived_data_dir = DERIVED_DATA_DIR,
        reference_dir = REFERENCE_DIR,
        output_dir = OUTPUT_DIR,
        screenshots_dir = SCREENSHOTS_DIR,
        exports_dir = EXPORTS_DIR,
        log_dir = LOG_DIR,
        sql_dir = SQL_DIR,
        app_dir = APP_DIR,
        notebooks_dir = NOTEBOOKS_DIR,
        tests_dir = TESTS_DIR,
    )
