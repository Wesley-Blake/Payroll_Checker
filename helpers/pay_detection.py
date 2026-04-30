from pathlib import Path
import pandas

def make_df(file: Path, pay_period: int) -> pandas.DataFrame | None:
    if not isinstance(file, Path):
        raise TypeError(f"Bad file input type {type(file)=}")
    df = pandas.read_csv(file)
    headers = df.columns
    for header in headers:
        if "pay" in header.lower() and "no" in header.lower():
            if df[header].iloc[0] == pay_period:
                return df
    else:
        return None
