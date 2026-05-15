from pathlib import Path
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt

# Historgam of timesheet statuses
def plot_timesheet_statuses(df, title='Timesheet Status Distribution', save_path='timesheet_status_distribution.png'):
    plt.style.use('dark_background')
    year = date.today().year
    white_list = ['EmplID', 'job_ecls', 'ts_Status']
    df = df[white_list].drop_duplicates()
    status_counts = df['ts_Status'].value_counts()
    plt.figure(figsize=(10, 6))
    ax = status_counts.plot(kind='bar', color='#E7763E')

    # Add centered data labels
    for p in ax.patches:
        ax.annotate(
            str(int(p.get_height())),
            (p.get_x() + p.get_width() / 2, p.get_height() / 2),
            ha='center',
            va='center',
            fontsize=10
        )

    plt.title(f"{year} BW{title}")
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path)


if __name__ == "__main__":
    # Example usage
    downloads = Path.home() / "Downloads"
    csv_list = []
    for i in downloads.iterdir():
        if "Comments Report" in i.name:
            csv_list.append(i)
    df = pd.read_csv(max(csv_list))
    plot_timesheet_statuses(df)
