"""Evaluation metrics for trajectory prediction."""

from __future__ import annotations

import numpy as np


def average_displacement_error(prediction: np.ndarray, target: np.ndarray) -> float:
    """Compute Average Displacement Error (ADE)."""
    _validate_trajectory_pair(prediction, target)
    return float(np.linalg.norm(prediction - target, axis=1).mean())


def final_displacement_error(prediction: np.ndarray, target: np.ndarray) -> float:
    """Compute Final Displacement Error (FDE)."""
    _validate_trajectory_pair(prediction, target)
    return float(np.linalg.norm(prediction[-1] - target[-1]))


def _validate_trajectory_pair(prediction: np.ndarray, target: np.ndarray) -> None:
    if prediction.shape != target.shape:
        raise ValueError("prediction and target must have the same shape")
    if prediction.ndim != 2 or prediction.shape[1] != 2:
        raise ValueError("trajectories must have shape (T, 2)")
