from pathlib import Path
import logging
import pandas
from pandas import DataFrame
import validators
import win32com.client as win32


class EmailList(dict):
    def __setitem__(self, key, value):
        if not validators.email(key):
            raise ValueError(f"Invalid email address: {key}")
        if not isinstance(value, list) or not all(validators.email(email) for email in value):
            raise ValueError(f"Value must be a list of valid email addresses: {value}")
        super().__setitem__(key, value)

def pay_period_check() -> int:
    pay_periods = [str(x) for x in range(1,27)]
    while True:
        result = input("What pay period is it? ")
        correction = input(f"{result} is this correct? [Y/n] ")
        if correction.lower() == 'n': continue
        if result in pay_periods: return int(result)

def loading_bar(length, index=1, pre_fix = '') -> callable:
    print()
    def make_bar(length=length, index=index, pre_fix=pre_fix) -> str:
        BAR_LENGTH = 30
        if len(pre_fix) > 0: print(pre_fix)
        while index <= length:
            block = int(BAR_LENGTH * index / length)
            bar = '=' * block + '-' * (BAR_LENGTH - block)
            yield f'\r|{bar}| {index} / {length} emails sent.'
            index += 1
    g = make_bar()
    return lambda: print(next(g), end='', flush=True)

def setup_logger(name: str) -> object:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"{name}")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

def make_df(file: Path, pay_period: int) -> DataFrame:
    if not isinstance(file, Path):
        raise TypeError(f"Bad file input type {type(file)=}")
    df = pandas.read_csv(file)
    headers = df.columns
    for header in headers:
        if "pay" in header.lower() and "no" in header.lower():
            if df[header].iloc[0] == pay_period:
                return df
    else:
        raise ValueError(f"Pay period {pay_period} not found in file {file.name}")

# NOTE: pass logger?
def return_dict(merged_df: DataFrame) -> EmailList[str:list[str]]:
    logger = setup_logger("PayRollChecker.log")
    headers = merged_df.columns
    if "appr" not in headers[-1].lower() and "super" not in headers[-1].lower():
        raise ValueError(f"Last column must be manager email, found {headers[-1]}")
    if "empl" not in headers[-2].lower() and "pacific" not in headers[-2].lower():
        raise ValueError(f"Last column must be employee email, found {headers[-2]}")
    result = EmailList()
    manager_emails: list[str] = merged_df[headers[-1]].unique().tolist()
    for manager_email in manager_emails:
        result.update({manager_email: []})
        employee_email_df = merged_df[merged_df[headers[-1]] == manager_email][headers[-2]]
        employee_email_list = employee_email_df.unique().tolist()
        result[manager_email] += employee_email_list
    logger.info("Finished Successfully.")
    return result

class winEmail:
    try:
        outlook = win32.Dispatch('outlook.application')
    except Exception as e:
        raise ValueError(f"Error initializing Outlook: {e}")
    def send_email(self, cc: str, bcc: list[str], pay_period: str, body: str) -> None:
        mail = self.outlook.CreateItem(0)
        mail.CC = cc
        mail.BCC = '; '.join(bcc)
        mail.Subject = f'Pay Period: BW{pay_period}'
        with open('secret.txt', 'r') as file:
            attachment = Path(file.readline().strip())
        if attachment.is_file():
            mail.Attachments.Add(str(attachment))
        mail.Body = body
        #mail.Display()
        mail.Send()
