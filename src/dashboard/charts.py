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

STANDARD_HOVER_COLUMNS = [
    "occupation_title",
    "major_group_title",
    "adoption_gap_absolute",
    "theoretical_exposure",
    "observed_exposure",
    "total_employment",
    "annual_mean_wage",
]

STANDARD_HOVER_TEMPLATE = (
    "Occupation&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = %{customdata[0]}<br>"
    "Group&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = %{customdata[1]}<br>"
    "Adoption Gap&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = %{customdata[2]:.3f}<br>"
    "Theoretical AI Capability = %{customdata[3]:.3f}<br>"
    "Observed AI Use&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = %{customdata[4]:.3f}<br>"
    "Total Employment&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = %{customdata[5]:,.0f}<br>"
    "Annual Mean Wage&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = $%{customdata[6]:,.0f}"
    "<extra></extra>"
)

STANDARD_HOVER_LABEL = {
    "align": "left",
    "font": {
        "family": "Menlo, Monaco, Consolas, 'Courier New', monospace",
    },
}


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
        custom_data = STANDARD_HOVER_COLUMNS,
        labels = {
            "major_group_title": "Group",
            "occupation_title": "Occupation",
            "theoretical_exposure": "Theoretical AI Capability",
            "observed_exposure": "Observed AI Use",
            "adoption_gap_absolute": "Adoption Gap",
        },
    )
    figure.update_traces(hovertemplate = STANDARD_HOVER_TEMPLATE, hoverlabel = STANDARD_HOVER_LABEL)
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
        custom_data = STANDARD_HOVER_COLUMNS,
        labels = {
            "occupation_title": "Occupation",
            display_column: "Occupation",
            "observed_exposure": "Observed AI Use",
            "theoretical_exposure": "Theoretical AI Capability",
            "adoption_gap_absolute": "Adoption Gap",
            "major_group_title": "Group",
        },
    )
    figure.update_traces(hovertemplate = STANDARD_HOVER_TEMPLATE, hoverlabel = STANDARD_HOVER_LABEL)
    figure.update_layout(
        height = max(420, 34 * len(plot_df) + 120),
        margin = {"l": 20, "r": 16, "t": 56, "b": 48},
        yaxis_title = "",
        xaxis_title = figure.layout.xaxis.title.text,
    )
    figure.update_yaxes(automargin = True, tickfont = {"size": 11})
    figure.update_xaxes(automargin = True)
    return figure
