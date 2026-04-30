from pathlib import Path
import pandas as pd
from pandas import DataFrame
import validators
from datetime import datetime
from helpers.logger_config import setup_logger
from helpers.email_list import EmailList

def return_dict(merged_df: DataFrame) -> EmailList[str:list[str]]:
    logger = setup_logger("PayRollChecker.log")
    headers = merged_df.columns
    result = EmailList()
    manager_emails: list[str] = merged_df[headers[-1]].unique().tolist()
    for manager_email in manager_emails:
        result.update({manager_email: []})
        employee_email_df = merged_df[merged_df[headers[-1]] == manager_email][headers[-2]]
        employee_email_list = employee_email_df.unique().tolist()
        result[manager_email] += employee_email_list

    logger.info("Finished Successfully.")
    return result

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

def holiday_detection_type(file: DataFrame, file_email: DataFrame, hol_list: list) -> dict[str:list[str]]:
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
        return {}
    filter_holiday = (
        (filtered_df[WHITE_LIST[3]] == "HOL") |
        (filtered_df[WHITE_LIST[3]] == "HLW")
    )
    final_df = filtered_df[~filter_holiday]
    if final_df.empty:
        return {}

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
    return return_dict(merged_df)

def holiday_detection_date(file: DataFrame, file_email: DataFrame, hol_list: list) -> dict[str:list[str]]:
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
        return {}
    final_df = filtered_df[~filtered_df["ts_entry_date"].isin(hol_list)]
    if final_df.empty:
        return {}

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
    return return_dict(merged_df)

def no_holiday_detection(file: DataFrame, file_email: DataFrame) -> dict[str:list[str]]:
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
        return {}

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
    return return_dict(merged_df)
