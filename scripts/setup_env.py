"""
AUTHOR: Rohan Joseph
PURPOSE: Create dashboard directories and install Python dependencies.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import argparse
import os
import shutil
import subprocess
import sys
import venv



"""
Settings
"""

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


# --- Import project-specific utilities and pipeline code ---
from project.logger import capture_script_console_to_markdown  # type: ignore
from project.paths import PROJECT_ROOT as PACKAGE_PROJECT_ROOT  # type: ignore
from project.paths import ensure_project_directories  # type: ignore
from project.utils import print_section_header, print_stage_banner, print_status  # type: ignore



"""
Script
"""

def resolve_python_path(project_root: str) -> str:
    """
    Resolve the Python interpreter used for package installation.
    This targets the local virtual environment when it exists.
    """

    venv_python_path = os.path.join(project_root, ".venv", "bin", "python")

    if os.path.exists(venv_python_path):
        return venv_python_path

    return sys.executable


def install_requirements(python_path: str, project_root: str) -> None:
    """
    Install repository Python dependencies from requirements.txt.
    This keeps the dashboard environment reproducible on a clean machine.
    """

    requirements_path = os.path.join(project_root, "requirements.txt")

    if not os.path.exists(requirements_path):
        print_status("No requirements.txt file found. Skipping Python dependency installation.")
        return

    print_status(f"Installing requirements from: {requirements_path}")
    subprocess.run(
        [python_path, "-m", "pip", "install", "-r", requirements_path],
        cwd = project_root,
        check = True,
    )


def create_env_file_from_example(project_root: str) -> bool:
    """
    Create a repo-local .env file from .env.example when one does not already exist.
    This keeps local path overrides easy to bootstrap without tracking them.
    """

    env_example_path = os.path.join(project_root, ".env.example")
    env_path = os.path.join(project_root, ".env")

    if os.path.exists(env_path):
        return False

    if not os.path.exists(env_example_path):
        raise FileNotFoundError(
            f"Cannot create {env_path} because {env_example_path} does not exist."
        )

    shutil.copyfile(env_example_path, env_path)
    return True


def run_setup(args: argparse.Namespace) -> None:
    """
    Execute the environment setup workflow.
    This keeps logging and CLI wiring thin.
    """

    print_stage_banner("Setting Up AI Occupation Adoption-Gap Dashboard")

    paths = ensure_project_directories()

    print_section_header("Project Root")
    print_status(f"Script root: {PROJECT_ROOT}")
    print_status(f"Package root: {PACKAGE_PROJECT_ROOT}")

    print_section_header("Created or Verified Directories")
    print_status(f"Input directory: {paths.input_dir}")
    print_status(f"Derived-data directory: {paths.derived_data_dir}")
    print_status(f"Output directory: {paths.output_dir}")
    print_status(f"Screenshots directory: {paths.screenshots_dir}")
    print_status(f"Exports directory: {paths.exports_dir}")
    print_status(f"Log directory: {paths.log_dir}")

    print_section_header("Preparing Local Environment File")
    env_created = create_env_file_from_example(PROJECT_ROOT)

    if env_created:
        print_status("Created .env from .env.example.")
    else:
        print_status("Found existing .env file. Leaving it unchanged.")

    venv_path = os.path.join(PROJECT_ROOT, ".venv")

    if args.create_venv:
        print_section_header("Creating Virtual Environment")
        print_status(f"Creating virtual environment at: {venv_path}")
        venv.EnvBuilder(with_pip = True).create(venv_path)

    if args.install_requirements:
        print_section_header("Installing Requirements")
        python_path = resolve_python_path(PROJECT_ROOT)
        install_requirements(python_path = python_path, project_root = PROJECT_ROOT)
    else:
        print_section_header("Installing Requirements")
        print_status("Skipped. Pass --install-requirements to install Python dependencies.")

    print_section_header("Status")
    print_status("Environment setup complete.")


def main() -> None:
    """
    Parse CLI arguments and run setup with Markdown logging.
    This gives the script one predictable command-line entrypoint.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--create-venv", action = "store_true")
    parser.add_argument("--install-requirements", action = "store_true")
    args = parser.parse_args()

    capture_script_console_to_markdown(
        run_callable = lambda: run_setup(args),
        output_dir = os.path.join(PROJECT_ROOT, "output", "logs"),
        script_name = "setup_env",
    )


if __name__ == "__main__":
    main()
