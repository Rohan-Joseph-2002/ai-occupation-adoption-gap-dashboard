"""
AUTHOR: Rohan Joseph
PURPOSE: Runtime configuration loading for the AI occupation adoption-gap dashboard.
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


# --- Import project-specific utilities and pipeline code ---
from project.io import load_dotenv_file
from project.paths import PROJECT_ROOT
from project.settings import CAPABILITY_THRESHOLD_DEFAULT, TOP_ROLE_COUNT_DEFAULT



"""
Classes
"""

@dataclass(frozen = True)
class RuntimeConfig:
    """
    Container for repo-local runtime settings.
    This gives scripts and the app one typed source of local configuration.
    """

    runtime_mode: str
    analysis_repo_path: str
    streamlit_host: str
    streamlit_port: int
    capability_threshold: float
    top_role_count: int



"""
Functions
"""

def resolve_project_path(path_text: str) -> str:
    """
    Resolve a possibly relative path against the project root.
    This keeps local .env overrides portable across machines.
    """

    expanded_path = os.path.expanduser(path_text)

    if os.path.isabs(expanded_path):
        return os.path.abspath(expanded_path)

    return os.path.abspath(os.path.join(PROJECT_ROOT, expanded_path))


def get_runtime_config() -> RuntimeConfig:
    """
    Load runtime configuration from the repo-local .env file.
    This centralizes local file locations and app thresholds.
    """

    env_values = load_dotenv_file(os.path.join(PROJECT_ROOT, ".env"))

    return RuntimeConfig(
        runtime_mode = env_values.get("RUNTIME_MODE", "local"),
        analysis_repo_path = resolve_project_path(
            env_values.get("ANALYSIS_REPO_PATH", os.path.join("..", "ai-occupation-adoption-gap-analysis"))
        ),
        streamlit_host = env_values.get("STREAMLIT_HOST", "localhost"),
        streamlit_port = int(env_values.get("STREAMLIT_PORT", "8501")),
        capability_threshold = float(env_values.get("CAPABILITY_THRESHOLD", str(CAPABILITY_THRESHOLD_DEFAULT))),
        top_role_count = int(env_values.get("TOP_ROLE_COUNT", str(TOP_ROLE_COUNT_DEFAULT))),
    )
