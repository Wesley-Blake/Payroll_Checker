"""
not_started.py

Utilities to detect employees who have not started their timesheets.

This module provides a function to build a mapping of manager emails to the
employee emails of direct reports who have not started their timesheets.

Dependencies:
    - pandas
"""

import sys
try:
    from pandas import DataFrame
except ImportError:
    sys.exit(
        f"Failed to import the packages. \
            {__file__}"
    )

# NOTE: Avoid relying on hard-coded column indices (e.g. headers[16],
# NOTE: "ApprEmail"). Prefer using explicit column names or a small schema
# NOTE: mapping at the top of the module so callers and maintainers know the
# NOTE: expected CSV layout. Consider returning an empty dict instead of
# NOTE: `None` for "no results" to keep return types consistent.

def not_started_list(df: DataFrame) -> dict[str, list[str]]:
    """
    Build a mapping of manager email -> list of employee emails who have not
    started their timesheets.

    Parameters:
        df (DataFrame): DataFrame containing the timesheet report rows.

    Returns:
        dict[str, list[str]] | None: Mapping of manager email to employee email
        list. Returns ``None`` if no matching employees are found.

    Raises:
        TypeError: If `df` is not a pandas DataFrame.
        ValueError: If the expected email fields are missing or not valid
        email strings.
    """
    result: dict[str, list[str]] = {}

    filtered_df = df[
        (df["ECLS"] != "SS") &
        (df["ECLS"] != "SN") &
        (df["ECLS"] != "WW")
    ]
    if filtered_df.empty:
        return result

    # unique() is the issue with pylance.
    manager_emails = filtered_df["ApprEmail"].unique().tolist() #type: ignore

    for email in manager_emails:
        if not isinstance(email, str) and '@' not in email:
            raise ValueError(
                f"manager_email in manager_emails is not email. \
                    {manager_emails[0]}\n{__file__}"
            )

    for manager_email in manager_emails:
        result.update({manager_email: []})
        employee_email_df = filtered_df[filtered_df["ApprEmail"] == manager_email]["EmplEmail"]
        employee_email_list = employee_email_df.unique().tolist() #type: ignore
        result[manager_email] += employee_email_list

    return result
