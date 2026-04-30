import pandas
from pandas import DataFrame
from helpers.support import *


def over_eight_hours(file_hours: DataFrame, file_email: DataFrame) -> EmailList[str, list[str]]:
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
    new_order_df = file_hours[WHITE_LIST]
    filtered_df = new_order_df.groupby(
        WHITE_LIST[:-1],
        as_index=False
    )["earning_hours"].sum()
    earn_code = filtered_df[WHITE_LIST[3]] == "REG"
    union = (
        (filtered_df[WHITE_LIST[2]] == "UU") &
        (filtered_df[WHITE_LIST[-1]] > 7.5)
        ) | (
        (filtered_df[WHITE_LIST[2]] == "VV") &
        (filtered_df[WHITE_LIST[-1]] > 7.5)
    )
    non_union = (
        (filtered_df[WHITE_LIST[2]] != "UU") &
        (filtered_df[WHITE_LIST[-1]] > 8)
        ) | (
        (filtered_df[WHITE_LIST[2]] != "VV") &
        (filtered_df[WHITE_LIST[-1]] > 8)
    )
    final_df = filtered_df[earn_code & (union | non_union)]
    if final_df.empty:
        logger.info("No employees with excessive hours.")
        return {}

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
    logger.info(f"Found {len(merged_df)} employees with excessive hours.")
    return return_dict(merged_df)

def over_twleve_hours(file_hours: DataFrame, file_email: DataFrame) -> EmailList[str, list[str]]:
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
    new_order_df = file_hours[WHITE_LIST]
    new_order_df.loc[:,"earn_code"] = new_order_df["earn_code"].replace(
        {
            "REG":"REG&OT",
            "OT":"REG&OT"
        }
    )
    filtered_df = new_order_df.groupby(
        WHITE_LIST[:-1],
        as_index=False
    )["earning_hours"].sum()
    earn_code = filtered_df[WHITE_LIST[3]] == "REG&OT"
    over_twelve_df = ((filtered_df[WHITE_LIST[-1]] > 12))
    final_df = filtered_df[earn_code & over_twelve_df]
    if final_df.empty:
        logger.info("No employees with excessive hours.")
        return {}

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
    logger.info(f"Found {len(merged_df)} employees with excessive hours.")
    return return_dict(merged_df)
