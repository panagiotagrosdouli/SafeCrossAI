"""Trajectory visualization utilities."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


def plot_trajectory_prediction(
    observed: np.ndarray,
    future: np.ndarray,
    prediction: np.ndarray,
    title: str = "SafeCrossAI trajectory prediction",
    save_path: str | Path | None = None,
) -> Figure:
    """Plot observed, ground-truth future, and predicted trajectories.

    Parameters
    ----------
    observed:
        Observed trajectory with shape ``(T_obs, 2)``.
    future:
        Ground-truth future trajectory with shape ``(T_fut, 2)``.
    prediction:
        Predicted future trajectory with shape ``(T_fut, 2)``.
    title:
        Figure title.
    save_path:
        Optional path for saving the figure.
    """
    _validate_xy(observed, "observed")
    _validate_xy(future, "future")
    _validate_xy(prediction, "prediction")

    if future.shape != prediction.shape:
        raise ValueError("future and prediction must have the same shape")

    figure, axis = plt.subplots(figsize=(7, 5))
    axis.plot(observed[:, 0], observed[:, 1], marker="o", label="observed")
    axis.plot(future[:, 0], future[:, 1], marker="o", label="future")
    axis.plot(prediction[:, 0], prediction[:, 1], marker="x", linestyle="--", label="prediction")
    axis.scatter(observed[-1, 0], observed[-1, 1], marker="s", label="last observed")
    axis.set_title(title)
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.axis("equal")
    axis.grid(True, alpha=0.3)
    axis.legend()
    figure.tight_layout()

    if save_path is not None:
        figure.savefig(save_path, dpi=150)

    return figure


def _validate_xy(values: np.ndarray, name: str) -> None:
    if values.ndim != 2 or values.shape[1] != 2:
        raise ValueError(f"{name} must have shape (T, 2)")
