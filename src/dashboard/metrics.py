"""
AUTHOR: Rohan Joseph
PURPOSE: KPI and ranking helpers for the AI occupation adoption-gap dashboard.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

import pandas as pd



"""
Functions
"""

def build_kpi_summary(dataframe: pd.DataFrame) -> dict[str, float]:
    """
    Build the headline KPI summary from a modeling/display sample.
    This keeps displayed values and SQL validation aligned.
    """

    return {
        "n_occupations": int(len(dataframe)),
        "mean_observed_exposure": round(float(dataframe["observed_exposure"].mean()), 3),
        "mean_theoretical_exposure": round(float(dataframe["theoretical_exposure"].mean()), 3),
        "mean_adoption_gap": round(float(dataframe["adoption_gap_absolute"].mean()), 3),
        "median_adoption_gap": round(float(dataframe["adoption_gap_absolute"].median()), 3),
    }


def filter_opportunity_roles(
    dataframe: pd.DataFrame,
    min_theoretical_exposure: float,
    top_n: int,
) -> pd.DataFrame:
    """
    Return high-capability occupations with the largest adoption gaps.
    This mirrors the SQL opportunity-rank query.
    """

    return (
        dataframe[dataframe["theoretical_exposure"] >= min_theoretical_exposure]
        .sort_values("adoption_gap_absolute", ascending = False)
        .head(top_n)
        .reset_index(drop = True)
    )


def filter_top_observed_use(dataframe: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """
    Return occupations with the highest observed AI use.
    This mirrors the SQL observed-use query.
    """

    return (
        dataframe.sort_values(
            ["observed_exposure", "theoretical_exposure"],
            ascending = [False, False],
        )
        .head(top_n)
        .reset_index(drop = True)
    )


def build_gap_band_dataframe(dataframe: pd.DataFrame, quartile_count: int = 4) -> pd.DataFrame:
    """
    Build expected adoption-gap quartiles and plain-language labels.
    This mirrors the SQL gap-band query with deterministic tie-breaking.
    """

    sorted_df = (
        dataframe[
            [
                "occupation_title",
                "major_group_title",
                "adoption_gap_absolute",
            ]
        ]
        .sort_values(
            ["adoption_gap_absolute", "occupation_title", "major_group_title"],
            ascending = [True, True, True],
        )
        .reset_index(drop = True)
    )

    row_count = len(sorted_df)
    base_bucket_size = row_count // quartile_count
    extra_rows = row_count % quartile_count
    bucket_sizes = [
        base_bucket_size + (1 if bucket_index < extra_rows else 0)
        for bucket_index in range(quartile_count)
    ]

    gap_quartiles = []
    for bucket_index, bucket_size in enumerate(bucket_sizes, start = 1):
        gap_quartiles.extend([bucket_index] * bucket_size)

    sorted_df["gap_quartile"] = gap_quartiles
    sorted_df["gap_band"] = pd.cut(
        sorted_df["adoption_gap_absolute"],
        bins = [-float("inf"), 0.2, 0.4, 0.6, float("inf")],
        labels = ["Low", "Moderate", "High", "Severe"],
        right = False,
    ).astype(str)

    return sorted_df
