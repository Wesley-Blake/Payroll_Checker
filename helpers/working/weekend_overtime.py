from pathlib import Path
import validators
import pandas as pd
#from helpers.logger_config import setup_logger
from logger_config import setup_logger

def weekend_overtime(file: Path, file_email: Path) -> dict:
    if file.is_file() and file_email.is_file():
        df = pd.read_csv(file)
    else:
        return {}

    WHITE_LIST = ["ts_payno", "Empl_ID", "JobECLS", "earn_code", "ts_entry_date", "appr_id", "earning_hours"]
    df = df[WHITE_LIST]

    # Remove people that didn't work the weekend.
    df['ts_entry_date'] = pd.to_datetime(df['ts_entry_date'])
    is_weekend = df['ts_entry_date'].dt.weekday.isin([5, 6])
    people_with_weekend = df.loc[is_weekend, 'Empl_ID'].unique()
    df = df[df['Empl_ID'].isin(people_with_weekend)].copy()

    # Narrow down to only REG
    df = df[df["earn_code"] == "REG"]
    filtered_df = df.groupby(
        WHITE_LIST[:-1],
        as_index=False
    )["earning_hours"].sum()
    # Union rule that it doesn't matter the number of hours worked.
    union = (
        (filtered_df[WHITE_LIST[2]] == "UU") |
        (filtered_df[WHITE_LIST[2]] == "VV")
    )
    # Law, requires > 40 hours REG.
    non_union = (
        (filtered_df[WHITE_LIST[2]] != "UU") &
        (filtered_df[WHITE_LIST[-1]] >= 8)
        ) | (
        (filtered_df[WHITE_LIST[2]] != "VV") &
        (filtered_df[WHITE_LIST[-1]] >= 8)
    )
    final_df = filtered_df[(union | non_union)]
    # Everything earlier than first Saturday.
    first_sat = (
        final_df.loc[final_df['ts_entry_date'].dt.weekday.isin([5,6]), 'ts_entry_date']
        .min()
    )
    final_df = final_df[final_df['ts_entry_date'] < first_sat]
    worked_weekend_df = final_df.groupby("Empl_ID")['ts_entry_date'].nunique().reset_index(name='days_worked')
    target_list = worked_weekend_df["Empl_ID"]
    final_df = final_df[final_df["Empl_ID"].isin(target_list)].copy()
    return final_df
