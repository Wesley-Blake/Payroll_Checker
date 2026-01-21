from pathlib import Path
import validators
from over_eight_hours import over_eight_hours

def main():
    hours = Path.cwd()
    hours = hours / "data_examples" / "hours-breakdown.csv"

    emails = Path.cwd()
    emails = emails / "data_examples" / "emails.csv"

    test = over_eight_hours(hours, emails)

if __name__ == "__main__":
    main()