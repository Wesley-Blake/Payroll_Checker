from pathlib import Path
import logging
import pandas as pd
import validators
from helpers.logger_config import setup_logger

def overlapping_hours(file: Path) -> dict[str,list[str]]:
    logger = setup_logger("PayRollChecker.log")

    result = {}
    if isinstance(file, Path) and file.is_file():
        df = pd.read_csv(file)
    else:
        logger.error("Failed to create DataFream.")
        return {}

    final_df = df[
        (df["earn_code"] == "OT") |
        (df["earn_code"] == "OT2") |
        (df["earn_code"] == "VAC") |
        (df["earn_code"] == "SICK") |
        (df["earn_code"] == "MD") |
        (df["earn_code"] == "PER")
    ]

    if final_df.empty:
        logger.info("No overlapping hours.")
        return {}

    manager_emails = final_df["Appr_Email"].unique().tolist()

    for manager_email in manager_emails:
        result.update({manager_email: []})
        employee_email_df = final_df[final_df["Appr_Email"] == manager_email]["Empl_Email"]
        employee_email_list = employee_email_df.unique().tolist()
        result[manager_email] += employee_email_list

    for manager, employee in result.items():
        if not validators.email(manager):
            logger.error("Manager email isn't email.")
            return {}
        for email in employee:
            if not validators.email(email):
                logger.error("Employee email isn't email.")
                return {}

    logger.info("Finished successfully.")
    return result