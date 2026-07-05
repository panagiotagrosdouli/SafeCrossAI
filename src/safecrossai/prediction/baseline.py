"""Baseline trajectory prediction models."""

from __future__ import annotations

import numpy as np


def constant_velocity_predict(history: np.ndarray, horizon: int) -> np.ndarray:
    """Predict future 2D positions with a constant-velocity baseline.

    Parameters
    ----------
    history:
        Array with shape ``(T, 2)`` containing observed x/y positions.
    horizon:
        Number of future steps to predict.

    Returns
    -------
    np.ndarray
        Array with shape ``(horizon, 2)`` containing predicted positions.
    """
    if history.ndim != 2 or history.shape[1] != 2:
        raise ValueError("history must have shape (T, 2)")
    if len(history) < 2:
        raise ValueError("at least two observed positions are required")
    if horizon <= 0:
        raise ValueError("horizon must be positive")

    velocity = history[-1] - history[-2]
    steps = np.arange(1, horizon + 1, dtype=float).reshape(-1, 1)
    return history[-1] + steps * velocity
