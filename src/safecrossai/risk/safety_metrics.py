"""Basic safety metrics for predicted interactions."""

from __future__ import annotations

import numpy as np


def minimum_distance(agent_a: np.ndarray, agent_b: np.ndarray) -> float:
    """Return the minimum Euclidean distance between two predicted trajectories."""
    _validate_pair(agent_a, agent_b)
    return float(np.linalg.norm(agent_a - agent_b, axis=1).min())


def simple_conflict_score(
    agent_a: np.ndarray,
    agent_b: np.ndarray,
    safety_distance: float = 2.0,
) -> float:
    """Return a normalized conflict score based on minimum distance.

    The score is 0 when the trajectories remain outside the safety distance and
    approaches 1 when the minimum distance approaches zero.
    """
    if safety_distance <= 0:
        raise ValueError("safety_distance must be positive")

    distance = minimum_distance(agent_a, agent_b)
    return float(max(0.0, 1.0 - distance / safety_distance))


def _validate_pair(agent_a: np.ndarray, agent_b: np.ndarray) -> None:
    if agent_a.shape != agent_b.shape:
        raise ValueError("trajectories must have the same shape")
    if agent_a.ndim != 2 or agent_a.shape[1] != 2:
        raise ValueError("trajectories must have shape (T, 2)")
