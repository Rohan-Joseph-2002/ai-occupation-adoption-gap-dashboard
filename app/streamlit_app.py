"""
AUTHOR: Rohan Joseph
PURPOSE: Streamlit entrypoint for the AI occupation adoption-gap dashboard.
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

import streamlit as st



"""
Settings
"""

# --- Ensure that the src directory is on PATH ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


# --- Import project-specific utilities and pipeline code ---
from dashboard.charts import build_capability_use_scatter, build_ranked_bar  # type: ignore
from dashboard.data import load_derived_dataframe  # type: ignore
from dashboard.metrics import build_kpi_summary, filter_opportunity_roles, filter_top_observed_use  # type: ignore
from project.env import get_runtime_config  # type: ignore



"""
Script
"""

@st.cache_data
def load_app_data():
    """
    Load dashboard data with Streamlit caching.
    This keeps interactive filtering responsive while preserving simple CSV inputs.
    """

    return {
        "occupations": load_derived_dataframe("occupation_analysis_dataset.csv"),
        "modeling": load_derived_dataframe("modeling_dataset.csv"),
        "major_groups": load_derived_dataframe("major_group_summary.csv"),
        "coefficients": load_derived_dataframe("model_coefficients.csv"),
    }


def main() -> None:
    """
    Render the Streamlit dashboard.
    This first app version keeps the dashboard usable while deeper styling can follow.
    """

    st.set_page_config(
        page_title = "AI Adoption Gap",
        layout = "wide",
    )

    config = get_runtime_config()
    data = load_app_data()
    modeling_df = data["modeling"]

    st.title("The AI Adoption Gap: Where the Unrealized Potential Is")
    st.caption("High capability, low current use: Where AI enablement may have the most headroom.")

    group_options = ["All"] + sorted(modeling_df["major_group_title"].dropna().unique().tolist())
    selected_group = st.sidebar.selectbox("Major Group", group_options)
    threshold = st.sidebar.slider(
        "Capability Threshold",
        min_value = 0.0,
        max_value = 1.0,
        value = config.capability_threshold,
        step = 0.05,
    )
    search_text = st.sidebar.text_input("Occupation Search").strip().lower()

    filtered_df = modeling_df.copy()

    if selected_group != "All":
        filtered_df = filtered_df[filtered_df["major_group_title"] == selected_group]

    filtered_df = filtered_df[filtered_df["theoretical_exposure"] >= threshold]

    if search_text != "":
        filtered_df = filtered_df[
            filtered_df["occupation_title"].str.lower().str.contains(search_text, na = False)
        ]

    if len(filtered_df) == 0:
        st.warning("No occupations match the selected filters.")
        st.stop()

    kpis = build_kpi_summary(filtered_df)
    metric_columns = st.columns(4)
    metric_columns[0].metric("Occupations Analysed", f"{kpis['n_occupations']:,}")
    metric_columns[1].metric("Mean Observed Use", f"{kpis['mean_observed_exposure']:.3f}")
    metric_columns[2].metric("Mean Theoretical Capability", f"{kpis['mean_theoretical_exposure']:.3f}")
    metric_columns[3].metric("Mean Adoption Gap", f"{kpis['mean_adoption_gap']:.3f}")

    st.plotly_chart(build_capability_use_scatter(filtered_df), width = "stretch")

    left_column, right_column = st.columns(2)

    with left_column:
        opportunity_df = filter_opportunity_roles(
            filtered_df,
            min_theoretical_exposure = threshold,
            top_n = config.top_role_count,
        )
        st.plotly_chart(
            build_ranked_bar(
                opportunity_df,
                x_column = "adoption_gap_absolute",
                title = "Highest-Opportunity Roles",
            ),
            width = "stretch",
        )

    with right_column:
        observed_use_df = filter_top_observed_use(filtered_df, top_n = config.top_role_count)
        st.plotly_chart(
            build_ranked_bar(
                observed_use_df,
                x_column = "observed_exposure",
                title = "Where AI is Already Embedded",
            ),
            width = "stretch",
        )


if __name__ == "__main__":
    main()
