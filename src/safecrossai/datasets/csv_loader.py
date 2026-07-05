"""CSV trajectory loading utilities."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from safecrossai.datasets.toy import TrajectorySample


REQUIRED_COLUMNS = {"scene_id", "agent_id", "frame", "x", "y"}


def load_trajectory_csv(path: str | Path) -> pd.DataFrame:
    """Load a trajectory CSV file and validate the required schema."""
    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"CSV file is missing required columns: {missing_text}")

    return data.sort_values(["scene_id", "agent_id", "frame"]).reset_index(drop=True)


def build_samples_from_csv(
    path: str | Path,
    observation_steps: int = 8,
    prediction_steps: int = 12,
) -> list[TrajectorySample]:
    """Convert CSV trajectories into observed/future samples.

    The expected CSV schema is:
    scene_id, agent_id, frame, x, y, agent_type

    The agent_type column is optional. If it is missing, pedestrian is used.
    """
    if observation_steps < 2:
        raise ValueError("observation_steps must be at least 2")
    if prediction_steps < 1:
        raise ValueError("prediction_steps must be positive")

    data = load_trajectory_csv(path)
    window = observation_steps + prediction_steps
    samples: list[TrajectorySample] = []

    for (_, _), group in data.groupby(["scene_id", "agent_id"]):
        group = group.sort_values("frame")
        if len(group) < window:
            continue

        positions = group[["x", "y"]].to_numpy(dtype=float)
        agent_type = str(group["agent_type"].iloc[0]) if "agent_type" in group else "pedestrian"

        for start in range(0, len(positions) - window + 1):
            segment = positions[start : start + window]
            samples.append(
                TrajectorySample(
                    observed=segment[:observation_steps],
                    future=segment[observation_steps:],
                    agent_type=agent_type,
                )
            )

    return samples
