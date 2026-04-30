import pandas
from pandas import DataFrame
from helpers.support import *

def overlapping_hours(file: DataFrame) -> EmailList[str, list[str]]:
    logger = setup_logger('PayRollChecker.log')
    white_list = ['REG', 'SHF', 'HOL', 'HLW']
    final_df = file[~file['earn_code'].isin(white_list)]
    if final_df.empty:
        logger.info('No overlapping hours.')
        return {}

    # NOTE: implement return dict
    result = EmailList()
    manager_emails = final_df['Appr_Email'].unique().tolist()
    for manager_email in manager_emails:
        result.update({manager_email: []})
        employee_email_df = final_df[final_df['Appr_Email'] == manager_email]['Empl_Email']
        employee_email_list = employee_email_df.unique().tolist()
        result[manager_email] += employee_email_list
    logger.info('Finished successfully.')
    return result
