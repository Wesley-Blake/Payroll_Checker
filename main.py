import argparse
import os
from pathlib import Path
from not_started import not_started_list
from pending_status import pending
from over_eight_hours import over_eight_hours
from win32com_email import email


def main(test: bool = False):
    DOWNLOADS = Path.home() / "Downloads"

    NOT_STARTED = ""
    PENDING = ""
    OVERTIME = ""
    EMAIL = ""
    PAY_PERIOD = input("Enter pay period: ")
    if not test:
        for file in os.scandir(DOWNLOADS):
            if "not_yet_started_WTE" in file.name and file.name > NOT_STARTED:
                NOT_STARTED = file.name
            if "Time_Sheet_Status" in file.name and file.name > PENDING:
                PENDING = file.name
            if "ts_break_down" in file.name and file.name > OVERTIME:
                OVERTIME = file.name
            if "Active" in file.name and file.name > EMAIL:
                EMAIL = file.name
        path_not_started =  DOWNLOADS / NOT_STARTED
        path_pending = DOWNLOADS / PENDING
        path_overtime = DOWNLOADS / OVERTIME
        path_email = DOWNLOADS / EMAIL
    else:
        DOCUMENTS = Path.home() / "Documents\\.mycode\\Payroll-Checker\\data_examples"
        path_not_started =  DOCUMENTS  / "NotStarted.csv"
        path_pending = DOCUMENTS / "comments-status.csv"
        path_overtime = DOCUMENTS / "hours-breakdown.csv"
        path_email = DOCUMENTS / "emails.csv"

    result_not_started = not_started_list(path_not_started)
    if len(result_not_started) > 0:
        for manager, employee in result_not_started.items():
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
""",
test
            )

    result_pending = pending(path_pending)
    if len(result_pending) > 0:
        email(
            "",
            result_pending,
            PAY_PERIOD,
f"""\
Hi,

For Manager:
You have employees in a pending status. Please approve them!
""",
test
        )

    result_overtime = over_eight_hours(path_overtime, path_email)
    if len(result_overtime) > 0:
        for manager, employee in result_overtime.items():
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
""",
test
            )


if __name__ == "__main__":
    main()
