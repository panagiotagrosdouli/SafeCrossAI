"""Linear trajectory prediction baselines.

This module intentionally implements a deterministic, interpretable baseline rather
than a learned model. It is suitable for sanity checks, ablation studies, and
reproducible comparisons before introducing neural forecasting methods.
"""

from __future__ import annotations

import numpy as np


def linear_regression_predict(history: np.ndarray, horizon: int) -> np.ndarray:
    """Predict future 2D positions with independent least-squares linear fits.

    The predictor fits ``x(t) = a_x t + b_x`` and ``y(t) = a_y t + b_y`` over
    the observed history and extrapolates for ``horizon`` future steps. Unlike a
    constant-velocity baseline that uses only the final displacement, this model
    uses all observed positions and is therefore less sensitive to a noisy last
    observation.

    Args:
        history: Observed positions with shape ``(T, 2)``.
        horizon: Number of future steps to predict.

    Returns:
        Predicted future positions with shape ``(horizon, 2)``.

    Raises:
        ValueError: If the input trajectory has invalid shape or horizon.
    """
    history = np.asarray(history, dtype=float)
    if history.ndim != 2 or history.shape[1] != 2:
        raise ValueError("history must have shape (T, 2)")
    if len(history) < 2:
        raise ValueError("at least two observed positions are required")
    if horizon <= 0:
        raise ValueError("horizon must be positive")

    observed_steps = np.arange(len(history), dtype=float)
    future_steps = np.arange(len(history), len(history) + horizon, dtype=float)

    x_coefficients = np.polyfit(observed_steps, history[:, 0], deg=1)
    y_coefficients = np.polyfit(observed_steps, history[:, 1], deg=1)

    predicted_x = np.polyval(x_coefficients, future_steps)
    predicted_y = np.polyval(y_coefficients, future_steps)
    return np.column_stack((predicted_x, predicted_y))
