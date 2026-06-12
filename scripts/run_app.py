"""
AUTHOR: Rohan Joseph
PURPOSE: Launch the Streamlit dashboard app.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os
import subprocess
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
from project.logger import capture_script_console_to_markdown  # type: ignore
from project.utils import print_section_header, print_stage_banner, print_status  # type: ignore



"""
Script
"""

def run_app() -> None:
    """
    Launch Streamlit with the dashboard app entrypoint.
    This keeps the app command reproducible and logged.
    """

    config = get_runtime_config()
    app_path = os.path.join(PROJECT_ROOT, "app", "streamlit_app.py")

    print_stage_banner("Launching AI Occupation Adoption-Gap Dashboard")

    print_section_header("Streamlit")
    print_status(f"App path: {app_path}")
    print_status(f"Host: {config.streamlit_host}")
    print_status(f"Port: {config.streamlit_port}")

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                app_path,
                "--server.address",
                config.streamlit_host,
                "--server.port",
                str(config.streamlit_port),
                "--server.headless",
                "true",
                "--browser.gatherUsageStats",
                "false",
            ],
            cwd = PROJECT_ROOT,
            check = True,
        )
    except KeyboardInterrupt:
        print_status("Streamlit app stopped by user.")


def main() -> None:
    """
    Run the app launcher with Markdown logging.
    This gives the script one predictable command-line entrypoint.
    """

    capture_script_console_to_markdown(
        run_callable = run_app,
        output_dir = os.path.join(PROJECT_ROOT, "output", "logs"),
        script_name = "run_app",
    )


if __name__ == "__main__":
    main()
