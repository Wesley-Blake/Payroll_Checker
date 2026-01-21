from pathlib import Path
import overlapping_hours

def main():
    csv = Path.cwd()
    csv.parent
    csv = csv / "data_examples" / "overlapping_hours.csv"
    result = overlapping_hours.overlapping_hours(csv)


if __name__ == "__main__":
    main()