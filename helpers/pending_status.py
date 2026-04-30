import pandas as pd
from pandas import DataFrame
from pathlib import Path
import validators
from helpers.logger_config import setup_logger

def pending(file: DataFrame) -> list[str]:
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
