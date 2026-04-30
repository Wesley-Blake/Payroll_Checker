import pandas
from pandas import DataFrame
from helpers.support import *

def not_started_list(file: DataFrame) -> EmailList[str, list[str]]:
    logger = setup_logger("PayRollChecker.log")
    # NOTE: implement whitelist
    final_df = file[
        (file["job_ecls"] != "SS") &
        (file["job_ecls"] != "SN") &
        (file["job_ecls"] != "WW")
    ]
    if final_df.empty:
        logger.info("All employees started.")
        return email_list

    manager_emails = final_df["ApprEmail"].unique().tolist()
    # NOTE: implement return_dict
    email_list = EmailList()
    for manager_email in manager_emails:
        email_list.update({manager_email: []})
        employee_email_df = final_df[final_df["ApprEmail"] == manager_email]["EmplEmail"]
        employee_email_list = employee_email_df.unique().tolist()
        email_list[manager_email] += employee_email_list

    logger.info("Finished successfully.")
    return email_list

def pending(file: DataFrame) -> list[str]:
    # NOTE: implement return_dict
    import validators
    logger = setup_logger("PayRollChecker.log")
    final_df = file[file["ts_Status"] == "Pending"]
    if final_df.empty:
        logger.info("No employees in pending.")
        return []

    manager_emails = final_df["ApprEmail"].unique().tolist()
    for email in manager_emails:
        if not validators.email(email):
            logger.debug("Manager emails not emails.")
            return []
    logger.info("Finished Successfully.")
    return manager_emails
