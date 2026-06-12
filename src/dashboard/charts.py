"""
AUTHOR: Rohan Joseph
PURPOSE: Plotly chart helpers for the AI occupation adoption-gap dashboard.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import textwrap
from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



"""
Functions
"""

def wrap_axis_label(label: str, width: int = 28) -> str:
    """
    Wrap a long categorical axis label for compact Plotly chart columns.
    """

    return "<br>".join(textwrap.wrap(str(label), width = width, break_long_words = False))


def build_capability_use_scatter(dataframe: pd.DataFrame) -> go.Figure:
    """
    Build the dashboard centerpiece scatter plot.
    This shows theoretical capability against observed use for each occupation.
    """

    figure = px.scatter(
        dataframe,
        x = "theoretical_exposure",
        y = "observed_exposure",
        color = "major_group_title",
        hover_name = "occupation_title",
        hover_data = {
            "adoption_gap_absolute": ":.3f",
            "theoretical_exposure": ":.3f",
            "observed_exposure": ":.3f",
            "major_group_title": True,
        },
        labels = {
            "major_group_title": "Group",
            "occupation_title": "Occupation",
            "theoretical_exposure": "Theoretical AI Capability",
            "observed_exposure": "Observed AI Use",
            "adoption_gap_absolute": "Adoption Gap",
        },
    )
    figure.add_trace(
        go.Scatter(
            x = [0, 1],
            y = [0, 1],
            mode = "lines",
            line = {"color": "gray", "dash": "dash"},
            name = "Parity",
            hoverinfo = "skip",
        )
    )
    figure.update_layout(xaxis_title = "Theoretical AI capability", yaxis_title = "Observed AI use")
    return figure


def build_ranked_bar(
    dataframe: pd.DataFrame,
    x_column: str,
    y_column: str = "occupation_title",
    title: Optional[str] = None,
) -> go.Figure:
    """
    Build a horizontal ranked bar chart from a pre-sorted DataFrame.
    This supports the opportunity and observed-use views.
    """

    plot_df = dataframe.copy().iloc[::-1]
    display_column = f"{y_column}_display"
    plot_df[display_column] = plot_df[y_column].apply(wrap_axis_label)
    figure = px.bar(
        plot_df,
        x = x_column,
        y = display_column,
        orientation = "h",
        title = title,
        hover_name = y_column,
        labels = {
            "occupation_title": "Occupation",
            display_column: "Occupation",
            "observed_exposure": "Observed AI Use",
            "theoretical_exposure": "Theoretical AI Capability",
            "adoption_gap_absolute": "Adoption Gap",
            "major_group_title": "Group",
        },
    )
    figure.update_layout(
        height = max(420, 34 * len(plot_df) + 120),
        margin = {"l": 20, "r": 16, "t": 56, "b": 48},
        yaxis_title = "",
        xaxis_title = x_column.replace("_", " ").title(),
    )
    figure.update_yaxes(automargin = True, tickfont = {"size": 11})
    figure.update_xaxes(automargin = True)
    return figure
