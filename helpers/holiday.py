import pandas
from pandas import DataFrame
from datetime import datetime
from helpers.support import *


def holidays_input() -> list[str]:
    holiday_list = []
    while True:
        holiday = input("Enter 1 holiday: [%YYYY-%mm-%dd] ")
        try:
            date = datetime.strptime(holiday, "%Y-%m-%d").date().isoformat()
            holiday_list.append(date)
        finally:
            if len(holiday) == 0:
                return holiday_list

def holiday_detection_type(file: DataFrame, file_email: DataFrame, hol_list: list) -> list[str]:
    logger = setup_logger("PayRollChecker.log")
    WHITE_LIST = [
        "Empl_ID",
        "LastName",
        "JobECLS",
        "earn_code",
        "ts_entry_date",
        "appr_id",
        "earning_hours"
    ]
    new_order_df = file[WHITE_LIST]
    filtered_df = new_order_df[new_order_df["ts_entry_date"].isin(hol_list)]
    if filtered_df.empty:
        logger.info("No holiday entries found.")
        return []

    filter_holiday = (
        (filtered_df[WHITE_LIST[3]] == "HOL") |
        (filtered_df[WHITE_LIST[3]] == "HLW")
    )
    final_df = filtered_df[~filter_holiday]
    if final_df.empty:
        logger.info("No non-holiday entries found.")
        return []

    EMAIL_WHITE_LIST = [
        "EmplID",
        "PacificEmail",
        "SupervisorEmail"
    ]
    ordered_email_df = file_email[EMAIL_WHITE_LIST].drop_duplicates()
    merged_df = pandas.merge(
        final_df,
        ordered_email_df,
        left_on="Empl_ID",
        right_on="EmplID",
        how="inner"
    )
    logger.info(f"Holiday detection completed. Found {len(merged_df)} entries.")
    #return return_dict(merged_df)
    return make_list(merged_df["PacificEmail"].unique().tolist())

def holiday_detection_date(file: DataFrame, file_email: DataFrame, hol_list: list) -> list[str]:
    logger = setup_logger("PayRollChecker.log")
    WHITE_LIST = [
        "Empl_ID",
        "LastName",
        "JobECLS",
        "earn_code",
        "ts_entry_date",
        "appr_id",
        "earning_hours"
    ]
    new_order_df = file[WHITE_LIST]
    filter_holiday = (
        (new_order_df[WHITE_LIST[3]] == "HOL") |
        (new_order_df[WHITE_LIST[3]] == "HLW")
    )
    filtered_df = new_order_df[filter_holiday]
    if filtered_df.empty:
        logger.info("No holiday entries found.")
        return []

    final_df = filtered_df[~filtered_df["ts_entry_date"].isin(hol_list)]
    if final_df.empty:
        logger.info("No non-holiday entries found.")
        return []

    EMAIL_WHITE_LIST = [
        "EmplID",
        "PacificEmail",
        "SupervisorEmail"
    ]
    ordered_email_df = file_email[EMAIL_WHITE_LIST].drop_duplicates()
    merged_df = pandas.merge(
        final_df,
        ordered_email_df,
        left_on="Empl_ID",
        right_on="EmplID",
        how="inner"
    )
    logger.info(f"Holiday detection completed. Found {len(merged_df)} entries.")
    #return return_dict(merged_df)
    return make_list(merged_df["PacificEmail"].unique().tolist())

def no_holiday_detection(file: DataFrame, file_email: DataFrame) -> list[str]:
    logger = setup_logger("PayRollChecker.log")
    WHITE_LIST = [
        "Empl_ID",
        "LastName",
        "JobECLS",
        "earn_code",
        "ts_entry_date",
        "appr_id",
        "earning_hours"
    ]
    new_order_df = file[WHITE_LIST]
    filter_holiday = (
        (new_order_df[WHITE_LIST[3]] == "HOL") |
        (new_order_df[WHITE_LIST[3]] == "HLW")
    )
    final_df = new_order_df[filter_holiday]
    if final_df.empty:
        logger.info("No holiday entries found.")
        return []

    EMAIL_WHITE_LIST = [
        "EmplID",
        "PacificEmail",
        "SupervisorEmail"
    ]
    ordered_email_df = file_email[EMAIL_WHITE_LIST].drop_duplicates()
    merged_df = pandas.merge(
        final_df,
        ordered_email_df,
        left_on="Empl_ID",
        right_on="EmplID",
        how="inner"
    )
    logger.info(f"Holiday detection completed. Found {len(merged_df)} entries.")
    return make_list(merged_df["PacificEmail"].unique().tolist())
