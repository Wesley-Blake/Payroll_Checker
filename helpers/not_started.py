from pathlib import Path
import logging
import pandas as pd
import validators
from logger_config import setup_logger

def not_started_list(file: Path) -> dict[str, list[str]]:
    logger = setup_logger("PayRollChecker.log")

    result = {}
    if isinstance(file, Path) and file.is_file():
        df = pd.read_csv(file)
    else:
        logger.error("Failed to create DataFream.")
        return {}

    final_df = df[
        (df["job_ecls"] != "SS") &
        (df["job_ecls"] != "SN") &
        (df["job_ecls"] != "WW")
    ]
    if final_df.empty:
        logger.info("All employees started.")
        return {}

    manager_emails = final_df["ApprEmail"].unique().tolist()

    for manager_email in manager_emails:
        result.update({manager_email: []})
        employee_email_df = final_df[final_df["ApprEmail"] == manager_email]["EmplEmail"]
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
