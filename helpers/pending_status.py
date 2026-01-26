import pandas as pd
from pathlib import Path
import validators
from helpers.logger_config import setup_logger

def pending(file: Path) -> list[str]:
    logger = setup_logger("PayRollChecker.log")
    if file.is_file():
        df = pd.read_csv(file)
    else:
        logger.error("Failed to create DataFrame.")
        return []

    final_df = df[df["ts_Status"] == "Pending"]

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
