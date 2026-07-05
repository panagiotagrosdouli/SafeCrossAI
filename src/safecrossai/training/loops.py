"""Compact training loops for SafeCrossAI models."""

from __future__ import annotations

from dataclasses import dataclass

import torch

from safecrossai.datasets.toy import TrajectorySample
from safecrossai.prediction.lstm import LSTMTrajectoryPredictor
from safecrossai.training.steps import lstm_update_step
from safecrossai.training.tensors import samples_to_tensors


@dataclass(frozen=True)
class TrainingHistory:
    """Training summary for a small baseline run."""

    epochs: int
    losses: list[float]

    @property
    def final_loss(self) -> float:
        """Return the last recorded loss."""
        return self.losses[-1]


def fit_lstm_baseline(
    samples: list[TrajectorySample],
    epochs: int = 5,
    learning_rate: float = 0.001,
    hidden_dim: int = 32,
) -> tuple[LSTMTrajectoryPredictor, TrainingHistory]:
    """Fit an LSTM baseline on trajectory samples."""
    if epochs < 1:
        raise ValueError("epochs must be positive")

    observed, future = samples_to_tensors(samples)
    model = LSTMTrajectoryPredictor(hidden_dim=hidden_dim, prediction_steps=future.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    losses: list[float] = []

    for _ in range(epochs):
        losses.append(lstm_update_step(model, observed, future, optimizer))

    return model, TrainingHistory(epochs=epochs, losses=losses)
