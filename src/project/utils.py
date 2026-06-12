"""
AUTHOR: Rohan Joseph
PURPOSE: Shared utility functions for formatting and diagnostics.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Functions
"""

def print_stage_banner(label: str) -> None:
    """
    Print a standardized stage banner.
    This helps make run logs easier to scan.
    """

    print("\n" + "-" * 76)
    print(label)
    print("-" * 76 + "\n")


def print_section_header(label: str) -> None:
    """
    Print a lightweight section header.
    This helps separate phases of setup, checks, and validation runs.
    """

    print(f"\n{label}")


def print_status(message: str) -> None:
    """
    Print a consistently indented status line.
    This helps make console output easier to scan.
    """

    print(f"  > {message}")
