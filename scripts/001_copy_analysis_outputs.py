"""
AUTHOR: Rohan Joseph
PURPOSE: Copy approved derived outputs from the analysis repo into the dashboard repo.
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
from project.env import get_runtime_config  # type: ignore
from project.io import copy_file, require_existing_file  # type: ignore
from project.logger import capture_script_console_to_markdown  # type: ignore
from project.paths import DERIVED_DATA_DIR, ensure_project_directories  # type: ignore
from project.settings import REQUIRED_DERIVED_FILES  # type: ignore
from project.utils import print_section_header, print_stage_banner, print_status  # type: ignore



"""
Script
"""

def run_copy() -> None:
    """
    Copy the approved dashboard input files from the upstream analysis repo.
    This keeps the dashboard repo as a presentation layer over reproducible analysis outputs.
    """

    config = get_runtime_config()
    ensure_project_directories()

    upstream_derived_dir = os.path.join(config.analysis_repo_path, "output", "derived_data")

    print_stage_banner("Copying Analysis Outputs for Dashboard")

    print_section_header("Source and Destination")
    print_status(f"Analysis derived-data directory: {upstream_derived_dir}")
    print_status(f"Dashboard derived-data directory: {DERIVED_DATA_DIR}")

    print_section_header("Files")
    for file_name in REQUIRED_DERIVED_FILES:
        source_path = os.path.join(upstream_derived_dir, file_name)
        output_path = os.path.join(DERIVED_DATA_DIR, file_name)
        require_existing_file(source_path, file_name)
        copy_file(source_path = source_path, output_path = output_path)
        print_status(f"Copied {file_name}")

    print_section_header("Status")
    print_status("Dashboard input copy complete.")


def main() -> None:
    """
    Run the copy step with Markdown logging.
    This gives the script one predictable command-line entrypoint.
    """

    capture_script_console_to_markdown(
        run_callable = run_copy,
        output_dir = os.path.join(PROJECT_ROOT, "output", "logs"),
        script_name = "001_copy_analysis_outputs",
    )


if __name__ == "__main__":
    main()
