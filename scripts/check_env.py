"""
AUTHOR: Rohan Joseph
PURPOSE: Validate local runtime configuration and required dashboard inputs.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import importlib.util
import os
import sys



"""
Settings
"""

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
REQUIRED_PACKAGES = ["pandas", "plotly", "duckdb", "streamlit"]

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


# --- Import project-specific utilities and pipeline code ---
from dashboard.data import list_missing_derived_files  # type: ignore
from project.env import get_runtime_config  # type: ignore
from project.logger import capture_script_console_to_markdown  # type: ignore
from project.paths import ensure_project_directories  # type: ignore
from project.utils import print_section_header, print_stage_banner, print_status  # type: ignore



"""
Script
"""

def check_python_packages() -> None:
    """
    Verify that required Python packages are importable.
    This catches incomplete dashboard environments before running the app.
    """

    missing_packages = [
        package_name
        for package_name in REQUIRED_PACKAGES
        if importlib.util.find_spec(package_name) is None
    ]

    if len(missing_packages) > 0:
        raise RuntimeError(f"Missing Python packages: {', '.join(missing_packages)}")


def run_check() -> None:
    """
    Execute the environment validation workflow.
    This keeps CLI wiring thin and outputs concrete diagnostics.
    """

    config = get_runtime_config()
    paths = ensure_project_directories()

    print_stage_banner("Checking AI Occupation Adoption-Gap Dashboard Environment")

    print_section_header("Resolved Configuration")
    print_status(f"Runtime mode: {config.runtime_mode}")
    print_status(f"Analysis repo path: {config.analysis_repo_path}")
    print_status(f"Streamlit host: {config.streamlit_host}")
    print_status(f"Streamlit port: {config.streamlit_port}")
    print_status(f"Capability threshold: {config.capability_threshold}")
    print_status(f"Top role count: {config.top_role_count}")

    print_section_header("Required Inputs")
    missing_files = list_missing_derived_files()

    if len(missing_files) > 0:
        raise FileNotFoundError(f"Missing derived input files: {', '.join(missing_files)}")

    print_status("All required derived input files are present.")

    print_section_header("Python Dependencies")
    check_python_packages()
    print_status("Required Python packages are importable.")

    print_section_header("Output Directories")
    print_status(f"Screenshots directory: {paths.screenshots_dir}")
    print_status(f"Exports directory: {paths.exports_dir}")
    print_status(f"Log directory: {paths.log_dir}")

    print_section_header("Status")
    print_status("Environment check passed.")


def main() -> None:
    """
    Run the environment check with Markdown logging.
    This gives the script one predictable command-line entrypoint.
    """

    capture_script_console_to_markdown(
        run_callable = run_check,
        output_dir = os.path.join(PROJECT_ROOT, "output", "logs"),
        script_name = "check_env",
    )


if __name__ == "__main__":
    main()
