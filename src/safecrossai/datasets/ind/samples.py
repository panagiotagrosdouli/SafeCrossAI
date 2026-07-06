"""Convert inD-style tracks into SafeCrossAI trajectory samples."""

from __future__ import annotations

from pathlib import Path

from safecrossai.datasets.ind.loader import load_ind_tracks_csv
from safecrossai.datasets.toy import TrajectorySample


def build_ind_samples(
    path: str | Path,
    observation_steps: int = 8,
    prediction_steps: int = 12,
) -> list[TrajectorySample]:
    """Build trajectory samples from an inD-style tracks CSV file."""
    if observation_steps < 2:
        raise ValueError("observation_steps must be at least 2")
    if prediction_steps < 1:
        raise ValueError("prediction_steps must be positive")

    data = load_ind_tracks_csv(path)
    window = observation_steps + prediction_steps
    samples: list[TrajectorySample] = []

    for _, group in data.groupby("trackId"):
        group = group.sort_values("frame")
        if len(group) < window:
            continue

        positions = group[["xCenter", "yCenter"]].to_numpy(dtype=float)
        agent_type = str(group["class"].iloc[0]) if "class" in group else "unknown"

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
