"""Convert inD-style tracks into SafeCrossAI trajectory samples."""

from __future__ import annotations

from pathlib import Path

from safecrossai.datasets.ind.loader import load_ind_tracks_csv
from safecrossai.datasets.toy import TrajectorySample


def build_ind_samples(
    path: str | Path,
    observation_steps: int = 8,
    prediction_steps: int = 12,
    classes: set[str] | None = None,
) -> list[TrajectorySample]:
    """Build trajectory samples from an inD-style tracks CSV file.

    Parameters
    ----------
    path:
        Path to an inD-style tracks CSV file.
    observation_steps:
        Number of observed positions.
    prediction_steps:
        Number of future positions.
    classes:
        Optional set of allowed agent classes. When provided, tracks whose
        class is not in the set are skipped.
    """
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

        agent_type = str(group["class"].iloc[0]) if "class" in group else "unknown"
        if classes is not None and agent_type not in classes:
            continue

        positions = group[["xCenter", "yCenter"]].to_numpy(dtype=float)

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
