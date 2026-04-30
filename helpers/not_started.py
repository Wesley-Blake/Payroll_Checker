from pathlib import Path
import logging
import pandas as pd
from pandas import DataFrame
from helpers.logger_config import setup_logger
from helpers.email_list import EmailList

def not_started_list(file: DataFrame) -> EmailList[str, list[str]]:
    logger = setup_logger("PayRollChecker.log")
    email_list = EmailList()

    final_df = file[
        (file["job_ecls"] != "SS") &
        (file["job_ecls"] != "SN") &
        (file["job_ecls"] != "WW")
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
