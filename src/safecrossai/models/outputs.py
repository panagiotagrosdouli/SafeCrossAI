"""Prediction output containers for trajectory models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass(frozen=True)
class PredictionOutput:
    """Standard prediction output returned by trajectory predictors.

    Attributes:
        trajectories: Predicted trajectories. The expected shape is model-dependent,
            but single-modal predictors should use ``(prediction_steps, 2)``.
        confidence: Optional confidence score for the prediction.
        covariance: Optional uncertainty covariance array.
        runtime_seconds: Optional inference runtime in seconds.
        metadata: Additional model-specific metadata.
    """

    trajectories: np.ndarray
    confidence: float | None = None
    covariance: np.ndarray | None = None
    runtime_seconds: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
