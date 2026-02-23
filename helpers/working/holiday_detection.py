from pathlib import Path
import pandas as pd
import validators


def holidays_input() -> list[str]:
    holiday_list = []
    while True:
        holiday = input("Enter 1 holiday: [%Y-%m-%d] ")
        try:
            date = datetime.strptime(holiday, "%Y-%m-%d").date().isoformat()
            holiday_list.append(date)
        finally:
            if len(holiday) == 0:
                return holiday_list

def holiday_detection(file: Path, file_email: Path) -> dict[str:list[str]]:
    hol_list = holidays_input()
