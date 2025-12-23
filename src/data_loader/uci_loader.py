from __future__ import annotations

from pathlib import Path
import pandas as pd


UCI_MISSING_SENTINEL = -200


def load_uci_air_quality(csv_path: Path) -> pd.DataFrame:
    """
    Load UCI Air Quality dataset and create a Datetime column.
    """
    df = pd.read_csv(csv_path, sep=";", decimal=",")
    df = df.dropna(axis=1, how="all")

    # Drop possible empty last column
    if df.columns[-1].startswith("Unnamed"):
        df = df.iloc[:, :-1]

    df["Datetime"] = pd.to_datetime(
        df["Date"].astype(str) + " " + df["Time"].astype(str),
        format="%d/%m/%Y %H.%M.%S",
        errors="coerce",
    )

    df = df.dropna(subset=["Datetime"])
    df = df.sort_values("Datetime").reset_index(drop=True)

    return df


def preprocess_uci_for_co_regression(df: pd.DataFrame) -> pd.DataFrame:
    """
    Minimal preprocessing for CO(GT) regression task.
    """
    work = df.copy()

    for col in ["CO(GT)", "PT08.S1(CO)"]:
        work[col] = pd.to_numeric(work[col], errors="coerce")

    # Replace sentinel values (-200) with NaN
    work = work.replace(UCI_MISSING_SENTINEL, pd.NA)

    # Drop rows with missing target or feature
    work = work.dropna(subset=["CO(GT)", "PT08.S1(CO)"])

    return work
