import os
from pathlib import Path
import textwrap
import pandas
from helpers.holiday import *
from helpers.overlapping_hours import *
from helpers.overtime import *
from helpers.status import *
from helpers.support import *
from helpers.templates import *


# implement asyncio
# dict[dfName: df]
WORKING_DIR = Path.cwd() / 'Payroll-Checker'
if WORKING_DIR.is_dir():
    os.chdir(WORKING_DIR)
else:
    print(WORKING_DIR)
    raise FileNotFoundError
DOWNLOADS = Path.home() / "Downloads"

PAY_PERIOD = pay_period_check()
print("Starting file search:")
NOT_STARTED = ""
OVERTIME = ""
EMAIL = ""
OVERLAPPING = ""
PENDING = ""
for file in os.scandir(DOWNLOADS):
    # implement date detection for files instead of relying on name.
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
path_not_started =  make_df(DOWNLOADS / NOT_STARTED, PAY_PERIOD)
path_overtime = make_df(DOWNLOADS / OVERTIME, PAY_PERIOD)
path_email = pandas.read_csv(DOWNLOADS / EMAIL)
path_overlapping = make_df(DOWNLOADS / OVERLAPPING, PAY_PERIOD)
path_pending = make_df(DOWNLOADS / PENDING, PAY_PERIOD)
print("File search compelted!")

# Holiday Detections
if input("Is there a holiday? [Y/n]") == "n":
    result_no_holiday = no_holiday_detection(path_overtime, path_email)
    length = len(result_no_holiday)
    if length > 0:
        my_bar = loading_bar(length, pre_fix="No Holiday Email:")
        for manager, employee in result_no_holiday.items():
            print(next(my_bar), end='', flush=True)
            email(
                manager,
                employee,
                PAY_PERIOD,
                NO_HOLIDAY_TEMPLATE + \
                MANGER_TEMPLATE.substitute(
                    length=length,
                    PAY_PERIOD=PAY_PERIOD
                )
            )
else:
    list_o_holidays = holidays_input()
    if len(list_o_holidays) == 0:
        SystemExit(f"{list_o_holidays=}\n is empty.")

    result_holiday_type = holiday_detection_type(
        path_overtime,
        path_email,
        list_o_holidays
    )
    length = len(result_holiday_type)
    if length > 0:
        my_bar = loading_bar(length, pre_fix="Holiday Type Email:")
        for manager, employee in result_holiday_type.items():
            print(next(my_bar), end='', flush=True)
            email(
                manager,
                employee,
                PAY_PERIOD,
                HOLIDAY_TYPE_TEMPLATE.substitute(
                    list_o_holidays=list_o_holidays
                ) + \
                MANGER_TEMPLATE.substitute(
                    length=length,
                    PAY_PERIOD=PAY_PERIOD
                )
            )
    result_holiday_date = holiday_detection_date(path_overtime, path_email, list_o_holidays)
    length = len(result_holiday_date)
    if length > 0:
        my_bar = loading_bar(length, pre_fix="Holiday Date Email:")
        for manager, employee in result_holiday_date.items():
            print(next(my_bar), end='', flush=True)
            email(
                manager,
                employee,
                PAY_PERIOD,
                HOLIDAY_DATE_TEMPLATE.substitute(
                    list_o_holidays=list_o_holidays
                ) + \
                MANGER_TEMPLATE.substitute(
                    length=length,
                    PAY_PERIOD=PAY_PERIOD
                )
            )

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
            NOT_STARTED_TEMPLATE + \
            MANGER_TEMPLATE.substitute(
                length=length,
                PAY_PERIOD=PAY_PERIOD
            )
        )

# Overtime Check
result_overtime = over_eight_hours(path_overtime, path_email)
length = len(result_overtime)
if  length > 0:
    my_bar = loading_bar(length, pre_fix="Overitme Emails over 8 hours: ")
    for manager, employee in result_overtime.items():
        print(next(my_bar), end='', flush=True)
        email(
            manager,
            employee,
            PAY_PERIOD,
            OVERTIME_TEMPLATE + \
            MANGER_TEMPLATE.substitute(
                length=length,
                PAY_PERIOD=PAY_PERIOD
            )
        )

# Over twelve hours in a day Overtime
result_over_twelve = over_twleve_hours(path_overtime, path_email)
length = len(result_over_twelve)
if length > 0:
    my_bar = loading_bar(length, pre_fix="Overitme Emails over 12 hours: ")
    for manager, employee in result_over_twelve.items():
        print(next(my_bar), end='', flush=True)
        email(
            manager,
            employee,
            PAY_PERIOD,
            OVER_TWELVE_TEMPLATE + \
            MANGER_TEMPLATE.substitute(
                length=length,
                PAY_PERIOD=PAY_PERIOD
            )
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
            OVERLAPPING_TEMPLATE + \
            MANGER_TEMPLATE.substitute(
                length=length,
                PAY_PERIOD=PAY_PERIOD
            )
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
        PENDING_TEMPLATE
    )
