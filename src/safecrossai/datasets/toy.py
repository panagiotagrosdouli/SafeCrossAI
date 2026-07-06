"""Toy intersection trajectories for early experiments."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TrajectorySample:
    """Observed and future trajectory pair for one road user."""

    observed: np.ndarray
    future: np.ndarray
    agent_type: str = "pedestrian"
    group_id: str | None = None


def make_linear_crossing_sample(
    observation_steps: int = 8,
    prediction_steps: int = 12,
    velocity: tuple[float, float] = (0.5, 0.2),
    group_id: str | None = "toy_trajectory",
) -> TrajectorySample:
    """Create a simple synthetic crossing trajectory."""
    if observation_steps < 2:
        raise ValueError("observation_steps must be at least 2")
    if prediction_steps < 1:
        raise ValueError("prediction_steps must be positive")

    total_steps = observation_steps + prediction_steps
    positions = np.zeros((total_steps, 2), dtype=float)
    step_velocity = np.array(velocity, dtype=float)

    for step in range(1, total_steps):
        positions[step] = positions[step - 1] + step_velocity

    return TrajectorySample(
        observed=positions[:observation_steps],
        future=positions[observation_steps:],
        agent_type="pedestrian",
        group_id=group_id,
    )
