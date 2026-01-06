import pandas as pd

def pending(file):
    df = pd.read_csv(file)
    result = {}

    final_df = df[df["status"] == "pending"]

    if final_df.empty:
        return result

    manager_emails = final_df[final_df["manager_email"]].unique().tolist()

    for manger_email in manager_emails:
        result.update({manger_email: []})
        result[manger_email] += final_df[final_df["manager_email"]].unique().tolist()
    
    return result
