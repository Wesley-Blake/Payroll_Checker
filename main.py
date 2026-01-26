import os
from pathlib import Path
from helpers.not_started import not_started_list
from helpers.over_eight_hours import over_eight_hours
from helpers.overlapping_hours import overlapping_hours
from helpers.pending_status import pending
from helpers.win32com_email import email

def loading_bar(length, index=1, pre_fix = ''):
    BAR_LENGTH = 30
    print()
    if len(pre_fix) > 0: print(pre_fix)
    while index <= length:
        block = int(BAR_LENGTH * index / length)
        bar = '=' * block + '-' * (BAR_LENGTH - block)
        yield f'\r|{bar}| {index} / {length} emails sent.'
        index += 1

def main():
    WORKING_DIR = Path.cwd() / 'Payroll-Checker'
    if WORKING_DIR.is_dir():
        os.chdir(WORKING_DIR)
    else:
        print(WORKING_DIR)
        raise ValueError
    DOWNLOADS = Path.home() / "Downloads"

    PAY_PERIOD = input("Enter pay period: ")
    print("Starting file search:")
    NOT_STARTED = ""
    OVERTIME = ""
    EMAIL = ""
    OVERLAPPING = ""
    PENDING = ""
    for file in os.scandir(DOWNLOADS):
        if "not_yet_started_WTE" in file.name and file.name > NOT_STARTED:
            NOT_STARTED = file.name
        elif "ts_break_down" in file.name and file.name > OVERTIME:
            OVERTIME = file.name
        elif "Active" in file.name and file.name > EMAIL:
            EMAIL = file.name
        elif "Overlapping_Hours" in file.name and file.name > OVERLAPPING:
            OVERLAPPING = file.name
        elif "Time_Sheet_Status" in file.name and file.name > PENDING:
            PENDING = file.name
    path_not_started =  DOWNLOADS / NOT_STARTED
    path_overtime = DOWNLOADS / OVERTIME
    path_email = DOWNLOADS / EMAIL
    path_overlapping = DOWNLOADS / OVERLAPPING
    path_pending = DOWNLOADS / PENDING
    print("File search compelted!")


    # Not Started Check
    result_not_started = not_started_list(path_not_started)
    length = len(result_not_started)
    if length > 0:
        my_bar = loading_bar(length, pre_fix="Not Started Emails:")
        for manager, employee in result_not_started.items():
            print(next(my_bar), end='', flush=True)
            email(
                manager,
                employee,
                PAY_PERIOD,
                f"""\
                Hi,

                Employee Action: Timesheet Not Started!

                For Manager:
                If you are receiving this email, it means that {len(employee)} of your employees have some issue related to their timesheet: {PAY_PERIOD}.
                They are BCC'd on this email, so there is no action needed on your part.
                """
            )

    # Overtime Check
    result_overtime = over_eight_hours(path_overtime, path_email)
    length = len(result_overtime)
    if  length > 0:
        my_bar = loading_bar(length, pre_fix="Overitme Emails: ")
        for manager, employee in result_overtime.items():
            print(next(my_bar), end='', flush=True)
            email(
                manager,
                employee,
                PAY_PERIOD,
                f"""\
                Hi,

                Employee Action: Overtime Not Allocated!
                You have time that is greater than 8 (7.5 union) REG hours in a day.

                For Manager:
                If you are receiving this email, it means that {len(employee)} of your employees have some issue related to their timesheet: {PAY_PERIOD}.
                They are BCC'd on this email, so there is no action needed on your part.
                """
            )

    # Overlapping Check
    result_overlapping = overlapping_hours(path_overlapping)
    length = len(result_overlapping)
    if  length > 0:
        my_bar = loading_bar(length, pre_fix="Overlapping Hours Emails:")
        for manager, employee in result_overlapping.items():
            print(next(my_bar), end='', flush=True)
            email(
                manager,
                employee,
                PAY_PERIOD,
                f"""\
                Hi,

                Employee Action: Overlapping Hours!
                You have hours somewhere that are overlapping!

                For Manager:
                If you are receiving this email, it means that {len(employee)} of your employees have some issue related to their timesheet: {PAY_PERIOD}.
                They are BCC'd on this email, so there is no action needed on your part.
                """
            )

    # Pending Check
    result_pending = pending(path_pending)
    if len(result_pending) > 0:
        my_bar = loading_bar(1, pre_fix="Pending Email:")
        print(next(my_bar), end='', flush=True)
        email(
            "",
            result_pending,
            PAY_PERIOD,
            f"""\
            Hi,

            For Manager:
            You have employees in a pending status. Please approve them!
            """
        )


if __name__ == "__main__":
    main()
    print()
    print("I'm done!")
