from pathlib import Path
import logging
import pandas as pd
from helpers.logger_config import setup_logger
from helpers.email_list import EmailList

def not_started_list(file: Path) -> EmailList[str, list[str]]:
    logger = setup_logger("PayRollChecker.log")
    email_list = EmailList()

    if isinstance(file, Path) and file.is_file():
        df = pd.read_csv(file)
    else:
        logger.error("Failed to create DataFrame.")
        return email_list

    final_df = df[
        (df["job_ecls"] != "SS") &
        (df["job_ecls"] != "SN") &
        (df["job_ecls"] != "WW")
    ]
    if final_df.empty:
        logger.info("All employees started.")
        return email_list

    manager_emails = final_df["ApprEmail"].unique().tolist()

    for manager_email in manager_emails:
        email_list.update({manager_email: []})
        employee_email_df = final_df[final_df["ApprEmail"] == manager_email]["EmplEmail"]
        employee_email_list = employee_email_df.unique().tolist()
        email_list[manager_email] += employee_email_list

    logger.info("Finished successfully.")
    return email_list
