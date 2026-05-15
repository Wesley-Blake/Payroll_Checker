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
    plt.figure()
    ax = status_counts.plot(kind='bar', color='#E7763E')
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

def plot_timesheet_statuses_by_job_ecls(df, title='Timesheet Status Distribution', save_path='timesheet_status_distribution.png'):
    plt.style.use('dark_background')
    year = date.today().year
    white_list = ['EmplID', 'job_ecls', 'ts_Status']
    df = df[white_list].drop_duplicates()
    counts = (
        df
        .groupby(["ts_Status", "job_ecls"])
        .size()
        .unstack(fill_value=0)
    )
    statuses = counts.index
    job_ecls = counts.columns
    fig, ax = plt.subplots()
    counts.plot(
        kind='bar',
        stacked=True,
        ax=ax,
    )
    ax.set_title(f"{year} BW{title}")
    ax.set_xlabel("Status")
    ax.set_ylabel("Total")
    ax.set_xticklabels(statuses, rotation=0)
    ax.legend(title="job_ecls")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    # Optional: add value labels on bars
    for container in ax.containers:
        labels = [
            f"{int(v)}" if v > 0 else ""
            for v in container.datavalues
        ]
        ax.bar_label(container, labels=labels, label_type='center')
    plt.tight_layout()
    plt.savefig(save_path)


if __name__ == "__main__":
    from pathlib import Path

    DOWNLOADS = Path.home() / "Downloads"
    path_list = []
    for i in DOWNLOADS.iterdir():
        if "Time_Sheet_Status" in i.name:
            path_list.append(i)
    if len(path_list) == 0:
        FileNotFoundError("No file with 'Time_Sheet_Status' in the name found in Downloads folder.")
    path_csv = max(path_list)
    df = pd.read_csv(path_csv)
    PAY_PERIOD = df['PayNo'].iloc[0]
    plot_timesheet_statuses(
        df,
        title=f"{PAY_PERIOD} Timesheet Status Distribution",
        save_path=DOWNLOADS / "Timesheet_Status_Distribution.png"
    )
    plot_timesheet_statuses_by_job_ecls(
        df,
        title=f"{PAY_PERIOD} Timesheet Status Distribution",
        save_path=DOWNLOADS / "Timesheet_Status_Distribution_by_Job_Ecls.png"
    )