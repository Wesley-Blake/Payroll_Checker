from pathlib import Path
from logger_config import setup_logger
from pending_status import pending

def main():
    file = Path.cwd()
    file = file / "data_examples" / "comments-status.csv"

    pending(file)


if __name__ == "__main__":
    main()
