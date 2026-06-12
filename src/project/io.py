"""
AUTHOR: Rohan Joseph
PURPOSE: Input and output helpers for the AI occupation adoption-gap dashboard.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os
import shutil

import pandas as pd



"""
Functions
"""

def load_dotenv_file(dotenv_path: str) -> dict[str, str]:
    """
    Load simple KEY=VALUE pairs from a repo-local .env file.
    This helps keep local path overrides out of committed Python code.
    """

    env_values: dict[str, str] = {}

    if not os.path.exists(dotenv_path):
        return env_values

    with open(dotenv_path, "r", encoding = "utf-8") as handle:
        for raw_line in handle:
            cleaned_line = raw_line.strip()

            if cleaned_line == "" or cleaned_line.startswith("#") or "=" not in cleaned_line:
                continue

            key, value = cleaned_line.split("=", 1)
            env_values[key.strip()] = value.strip()

    return env_values


def read_csv_dataframe(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Read a CSV file into a DataFrame.
    This centralizes pandas loading behavior for scripts and the app.
    """

    return pd.read_csv(file_path, **kwargs)


def write_csv_dataframe(dataframe: pd.DataFrame, output_path: str) -> None:
    """
    Write a DataFrame to CSV after ensuring the parent directory exists.
    This keeps export logic concise.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok = True)
    dataframe.to_csv(output_path, index = False)


def copy_file(source_path: str, output_path: str) -> None:
    """
    Copy one file after ensuring the output directory exists.
    This keeps copy scripts explicit without shell-specific behavior.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok = True)
    shutil.copy2(source_path, output_path)


def require_existing_file(file_path: str, label: str) -> None:
    """
    Require that a configured file exists.
    This helps fail early before validation or app startup.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing {label}: {file_path}")
