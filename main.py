import os
from pathlib import Path
import textwrap
from datetime import datetime
from helpers.not_started import not_started_list
from helpers.over_eight_hours import over_eight_hours
from helpers.over_twelve_hours import over_twleve_hours
from helpers.overlapping_hours import overlapping_hours
#from helpers.weekend_overtime import weekend_overtime
from helpers.pending_status import pending
from helpers.win32com_email import email

def pay_period_check() -> str:
    pay_periods = [str(x) for x in range(1,27)]
    while True:
        result = input("What pay period is it? ")
        correction = input(f"{result} is this correct? [Y/n] ")
        if correction.lower() == 'n': continue
        if result in pay_periods: return result

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

    PAY_PERIOD = pay_period_check()
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
                textwrap.dedent(f"""\
                Hi,

                Friendly Reminder: Timesheet Not Started
                Timesheets are due this friday!

                Manager:
                Hello! We wanted to let you know that {len(employee)} of your employees have not started their timesheet for the pay period {PAY_PERIOD}.
                They've been BCC'd on this email as a helpful reminder, so no action is needed from you at this time.

                Thanks so much, and have a great day!
                """)
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
                textwrap.dedent(f"""\
                Hi,

                Friendly Reminder: Overtime Not Allocated

                We wanted to let you know that you recorded more than 8 hours of regular (7.5 for union) time in a single day, and overtime has not yet been allocated.
                For helpful guidance, you can review the overtime rules here: https://www.dir.ca.gov/dlse/FAQ_Overtime.htm
                Essentially, you should put 8 (7.5 union) in Regular Earnings, the rest goes in Overtime.

                Manager Notification:
                You're receiving this email because {len(employee)} of your employees haven't allocated Overtime for the pay period {PAY_PERIOD}.
                They've been BCC'd on this message as a friendly reminder, so no action is needed from you at this time.

                Thanks so much, and appreciate your support!
                """)
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
                textwrap.dedent(f"""\
                Hi,

                Friendly Reminder: Overtime for Hours Over 12 Not Allocated

                We wanted to share a quick reminder that any hours worked over 12 in a single day (regular + overtime) are automatically considered OT2 and may need to be allocated accordingly.
                For more information, you can review the guidelines here: https://www.dir.ca.gov/dlse/FAQ_Overtime.htm
                Example:
                    8 REG (7.5 unoin) + 4 OT (4.5 union) = 12 hours and everything else is in OT2.

                Manager Notification:
                You're receiving this email because {len(employee)} of your employees have a timesheet item to review for the pay period {PAY_PERIOD}.
                They've been BCC'd on this message as a helpful reminder, so no action is needed from you at this time.

                Thanks so much, and we appreciate your support!
                """)
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
                textwrap.dedent(f"""\
                Hi,

                Friendly Reminder: Overlapping Hours

                We noticed that there are some hours on your timesheet that overlap. This happens from time to time and can usually be resolved with a quick review.
                Additionally, if you are using the Employee Services (new), the yellow (!) will tell you specifics.

                Manager Notification:
                You're receiving this email because {len(employee)} of your employees have a timesheet item to review for the pay period {PAY_PERIOD}.
                They've been BCC'd on this message as a helpful reminder, so no action is needed from you at this time.

                Thanks so much, and have a great day!
                """)
            )

    # Weekend Overtime Not Allocated
    #result_weekend_overtime = weekend_overtime(path_overtime,path_email)
    #length = len(result_weekend_overtime)
    #if length > 0:
    #    my_bar = loading_bar(length, pre_fix="Weekend Overtime Emails:")
    #    for manager, employee in result_weekend_overtime.items():
    #        print(next(my_bar), end='', flush=True)
    #        email(
    #            manager,
    #            employee,
    #            PAY_PERIOD,
    #            textwrap.dedent(f"""\
    #            Hi,

    #            Employee Action: Weekend Overtime Not Allocated!
    #            Union: if you had REG from Monday to Friday, Saturday and Sunday are Overtime by default.
    #            Everyone else: if you worked 40 hours REG from Monday, everyting is Overtime by default.
    #            https://www.dir.ca.gov/dlse/FAQ_Overtime.htm

    #            For Manager:
    #            If you are receiving this email, it means that {len(employee)} of your employees have some issue related to their timesheet: {PAY_PERIOD}.
    #            They are BCC'd on this email, so there is no action needed on your part.
    #            """)
    #        )

    # Pending Check
    result_pending = pending(path_pending)
    if len(result_pending) > 0:
        my_bar = loading_bar(1, pre_fix="Pending Email:")
        print(next(my_bar), end='', flush=True)
        email(
            "",
            result_pending,
            PAY_PERIOD,
            textwrap.dedent(f"""\
            Hi,

            Manager Reminder: Pending Approvals

            Just a quick heads-up that you have employees whose timesheets are currently in a pending status and ready for your approval when you have a moment.

            Thanks so much for your time and support!
            """)
        )


if __name__ == "__main__":
    main()
    print()
    print("I'm done!")
