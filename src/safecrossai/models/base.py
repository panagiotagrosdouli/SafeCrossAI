"""Base model interfaces for trajectory prediction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable

from safecrossai.models.outputs import PredictionOutput


class TrajectoryPredictor(ABC):
    """Abstract interface for all trajectory prediction models."""

    @abstractmethod
    def fit(self, samples: Iterable[Any]) -> None:
        """Fit the predictor on training samples."""

    @abstractmethod
    def predict(self, sample: Any) -> PredictionOutput:
        """Predict future trajectory for a single sample."""

    def predict_batch(self, samples: Iterable[Any]) -> list[PredictionOutput]:
        """Predict future trajectories for multiple samples."""
        return [self.predict(sample) for sample in samples]

    @abstractmethod
    def save(self, path: str | Path) -> None:
        """Save predictor state to disk."""

    @classmethod
    @abstractmethod
    def load(cls, path: str | Path) -> "TrajectoryPredictor":
        """Load predictor state from disk."""
