import pandas
from pandas import DataFrame
from helpers.support import *


def overlapping_hours(file: DataFrame) -> list[str]:
    logger = setup_logger('PayRollChecker.log')
    white_list = ["empl_id", "earn_code", "Empl_Email", "Appr_Email"]
    file = file[white_list]
    white_list = ['REG', 'SHF', 'HOL', 'HLW']
    final_df = file[~file['earn_code'].isin(white_list)]
    if final_df.empty:
        logger.info('No overlapping hours.')
        return []

    return make_list(final_df["Empl_Email"].unique().tolist())
