"""Loader for inD-style track CSV files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"trackId", "frame", "xCenter", "yCenter"}


def load_ind_tracks_csv(path: str | Path) -> pd.DataFrame:
    """Load and validate an inD-style tracks CSV file.

    Expected core columns are:
    - trackId
    - frame
    - xCenter
    - yCenter

    Optional columns such as class, xVelocity, and yVelocity are preserved.
    """
    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"inD tracks CSV is missing required columns: {missing_text}")

    return data.sort_values(["trackId", "frame"]).reset_index(drop=True)
