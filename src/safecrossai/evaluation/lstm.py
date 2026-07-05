"""Evaluation helpers for LSTM trajectory models."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch

from safecrossai.datasets.toy import TrajectorySample
from safecrossai.evaluation.metrics import average_displacement_error, final_displacement_error
from safecrossai.prediction.lstm import LSTMTrajectoryPredictor
from safecrossai.training.tensors import samples_to_tensors


@dataclass(frozen=True)
class LSTMEvaluationSummary:
    """Aggregate ADE/FDE metrics for an LSTM model."""

    samples: int
    mean_ade: float
    mean_fde: float


def evaluate_lstm_model(
    model: LSTMTrajectoryPredictor,
    samples: list[TrajectorySample],
) -> LSTMEvaluationSummary:
    """Evaluate an LSTM model on trajectory samples."""
    observed, future = samples_to_tensors(samples)

    model.eval()
    with torch.no_grad():
        prediction = model(observed).detach().cpu().numpy()

    future_np = future.detach().cpu().numpy()
    ade_values: list[float] = []
    fde_values: list[float] = []

    for predicted_sample, target_sample in zip(prediction, future_np, strict=True):
        ade_values.append(average_displacement_error(predicted_sample, target_sample))
        fde_values.append(final_displacement_error(predicted_sample, target_sample))

    return LSTMEvaluationSummary(
        samples=len(samples),
        mean_ade=float(np.mean(ade_values)),
        mean_fde=float(np.mean(fde_values)),
    )
