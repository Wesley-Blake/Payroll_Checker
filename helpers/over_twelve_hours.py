"""Identifies employees working over 12 hours in a pay period.

Combines REG and OT earn codes, then filters by >12 hour threshold.
Returns dict mapping manager emails to lists of employee emails.
"""
from pathlib import Path
import pandas as pd
import validators
from helpers.logger_config import setup_logger


def over_twleve_hours(file_hours: Path, file_email: Path) -> dict[str, list[str]]:
    """Find employees exceeding 12 hours by manager.
    
    Args:
        file_hours: Path to hours breakdown CSV
        file_email: Path to employee email CSV
        
    Returns:
        Dict mapping manager email to list of employee emails, or empty dict.
    """
    logger = setup_logger("PayRollChecker.log")

    # Validate inputs are Path objects
    if not isinstance(file_hours, Path) or not isinstance(file_email, Path):
        logger.error("Invalid file path(s) provided.")
        return {}
    
    # Validate input files exist
    if file_hours.is_file() and file_email.is_file():
        df = pd.read_csv(file_hours)
    else:
        logger.error("Failed to create DataFrame.")
        return {}

    # Select columns and replace earn codes
    WHITE_LIST = [
        "Empl_ID",
        "LastName",
        "JobECLS",
        "earn_code",
        "ts_entry_date",
        "appr_id",
        "earning_hours"
    ]
    new_order_df = df[WHITE_LIST]
    # Combine REG and OT into single category
    new_order_df.loc[:,"earn_code"] = new_order_df["earn_code"].replace(
        {
            "REG":"REG&OT",
            "OT":"REG&OT"
        }
    )
    
    # Aggregate hours by employee and filter by threshold
    filtered_df = new_order_df.groupby(
        WHITE_LIST[:-1],
        as_index=False
    )["earning_hours"].sum()

    earn_code = filtered_df[WHITE_LIST[3]] == "REG&OT"
    over_twelve_df = ((filtered_df[WHITE_LIST[-1]] > 12))
    final_df = filtered_df[earn_code & over_twelve_df]
    if final_df.empty:
        logger.info("No employees with excessive hours.")
        return {}

    # Merge with email data and group by manager
    email_df = pd.read_csv(file_email)
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
    result: dict[str,list[str]] = {}
    manager_emails: list[str] = merged_df[headers[-1]].unique().tolist()
    for manager_email in manager_emails:
        result.update({manager_email: []})
        employee_email_df = merged_df[merged_df[headers[-1]] == manager_email][headers[-2]]
        employee_email_list = employee_email_df.unique().tolist()
        result[manager_email] += employee_email_list

    # Validate all emails
    for manager, employee in result.items():
        if not validators.email(manager):
            logger.debug("Manager email isn't email.")
            return {}
            for email in employee:
                if not validators.email(email):
                    logger.debug("Employee email isn't email.")
                    return {}
    logger.info("Finished Successfully.")
    return result
