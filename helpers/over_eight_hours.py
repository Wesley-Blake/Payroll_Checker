"""Identifies employees working over 8 hours in a pay period.

Handles union/non-union thresholds: union >7.5 hrs, non-union >8 hrs.
Returns dict mapping manager emails to lists of employee emails.
"""
from pathlib import Path
import pandas as pd
from pandas import DataFrame
import validators
from helpers.logger_config import setup_logger
from helpers.email_list import EmailList


def over_eight_hours(file_hours: DataFrame, file_email: DataFrame) -> dict[str, list[str]]:
    """Find employees exceeding 8 hours by manager.

    Args:
        file_hours: Path to hours breakdown CSV
        file_email: Path to employee email CSV

    Returns:
        Dict mapping manager email to list of employee emails, or empty dict.
    """
    logger = setup_logger("PayRollChecker.log")

    # Select and aggregate hours by employee
    WHITE_LIST = [
        "Empl_ID",
        "LastName",
        "JobECLS",
        "earn_code",
        "ts_entry_date",
        "appr_id",
        "earning_hours"
    ]
    new_order_df = file_hours[WHITE_LIST]
    filtered_df = new_order_df.groupby(
        WHITE_LIST[:-1],
        as_index=False
    )["earning_hours"].sum()

    # Filter by earn code and hours threshold
    earn_code = filtered_df[WHITE_LIST[3]] == "REG"
    # Union employees: >7.5 hours; Non-union: >8 hours
    union = (
        (filtered_df[WHITE_LIST[2]] == "UU") &
        (filtered_df[WHITE_LIST[-1]] > 7.5)
        ) | (
        (filtered_df[WHITE_LIST[2]] == "VV") &
        (filtered_df[WHITE_LIST[-1]] > 7.5)
    )
    non_union = (
        (filtered_df[WHITE_LIST[2]] != "UU") &
        (filtered_df[WHITE_LIST[-1]] > 8)
        ) | (
        (filtered_df[WHITE_LIST[2]] != "VV") &
        (filtered_df[WHITE_LIST[-1]] > 8)
    )
    final_df = filtered_df[earn_code & (union | non_union)]
    if final_df.empty:
        logger.info("No employees with excessive hours.")
        return {}

    # Merge with email data and group by manager
    email_df = file_email
    EMAIL_WHITE_LIST = [
        "EmplID",
        "PacificEmail",
        "SupervisorEmail"
    ]
    ordered_email_df = email_df[EMAIL_WHITE_LIST].drop_duplicates()
    merged_df = pd.merge(
        final_df,
        ordered_email_df,
        left_on="Empl_ID",
        right_on="EmplID",
        how="inner"
    )
    headers = merged_df.columns

    # Build result dict: manager -> [employees]
    result = EmailList()
    manager_emails: list[str] = merged_df[headers[-1]].unique().tolist()
    for manager_email in manager_emails:
        result.update({manager_email: []})
        employee_email_df = merged_df[merged_df[headers[-1]] == manager_email][headers[-2]]
        employee_email_list = employee_email_df.unique().tolist()
        result[manager_email] += employee_email_list

    logger.info("Finished Successfully.")
    return result
