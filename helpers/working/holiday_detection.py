from pathlib import Path
import pandas as pd
import validators
from datetime import datetime
# from helpers.logger_config import setup_logger

def return_dict(merged_df) -> dict[str:list[str]]:
     # Build result dict: manager -> [employees]
    headers = merged_df.columns
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
            #logger.debug("Manager email isn't email.")
            return {}
            for email in employee:
                if not validators.email(email):
                    #logger.debug("Employee email isn't email.")
                    return {}
    #logger.info("Finished Successfully.")
    return result

def holidays_input() -> list[str]:
    holiday_list = []
    while True:
        holiday = input("Enter 1 holiday: [%YYYY-%mm-%dd] ")
        try:
            date = datetime.strptime(holiday, "%Y-%m-%d").date().isoformat()
            #date = datetime.strptime(holiday, "%Y-%m-%d").date()
            holiday_list.append(date)
        finally:
            if len(holiday) == 0:
                return holiday_list

def holiday_detection_type(file: Path, file_email: Path, hol_list: list) -> dict[str:list[str]]:
    #logger = setup_logger("PayRollChecker.log")
    if not isinstance(file, Path) and not isinstance(file_email, Path):
        #logger.error(f"Bad file input type {type(file)=} {type(file_email)=}")
        return {}

    if file.is_file() and file_email.is_file():
        df = pd.read_csv(file)
    else:
        #logger.error("File doesn't exist!")
        return {}
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
    # Isolate DF by date, then find all events != HOL and HLW.
    # What is the type of date (date or str) in DF?

def holiday_detection_date(file: Path, file_email: Path) -> dict[str:list[str]]:
    #logger = setup_logger("PayRollChecker.log")
    if not isinstance(file, Path) and not isinstance(file_email, Path):
        #logger.error(f"Bad file input type {type(file)=} {type(file_email)=}")
        return {}

    if file.is_file() and file_email.is_file():
        df = pd.read_csv(file)
    else:
        #logger.error("File doesn't exist!")
        return {}
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
    filter_holiday = (
        (new_order_df[WHITE_LIST[3]] == "HOL") |
        (new_order_df[WHITE_LIST[3]] == "HLW")
    )
    final_df = new_order_df[filter_holiday]
    if final_df.empty:
        return {}
    # Isolate everything != dates.

def no_holiday_detection(file: Path, file_email: Path) -> dict[str:list[str]]:
    #logger = setup_logger("PayRollChecker.log")
    if not isinstance(file, Path) and not isinstance(file_email, Path):
        #logger.error(f"Bad file input type {type(file)=} {type(file_email)=}")
        return {}

    if file.is_file() and file_email.is_file():
        df = pd.read_csv(file)
    else:
        #logger.error("File doesn't exist!")
        return {}

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
    filter_holiday = (
        (new_order_df[WHITE_LIST[3]] == "HOL") |
        (new_order_df[WHITE_LIST[3]] == "HLW")
    )
    final_df = new_order_df[filter_holiday]
    if final_df.empty:
        return {}

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
    return return_dict(merged_df)


if __name__ == '__main__':
    test_file = Path()
    test_file_email = Path()

    test_result = no_holiday_detection(test_file, test_file_email)

    print(test_result)
