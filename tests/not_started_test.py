from pathlib import Path
import not_started

def main():
    csv = Path.cwd()
    csv.parent
    csv = csv / "data_examples" / "NotStarted.csv"
    result = not_started.not_started_list(csv)


if __name__ == "__main__":
    main()