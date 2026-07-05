"""Baseline experiment pipeline for SafeCrossAI."""

from __future__ import annotations

from dataclasses import dataclass

from safecrossai.datasets.toy import make_linear_crossing_sample
from safecrossai.evaluation.metrics import average_displacement_error, final_displacement_error
from safecrossai.prediction.baseline import constant_velocity_predict


@dataclass(frozen=True)
class BaselineResult:
    """Metrics from a trajectory prediction baseline."""

    ade: float
    fde: float


def run_constant_velocity_baseline() -> BaselineResult:
    """Run the constant-velocity baseline on a synthetic crossing sample."""
    sample = make_linear_crossing_sample()
    prediction = constant_velocity_predict(sample.observed, horizon=len(sample.future))

    return BaselineResult(
        ade=average_displacement_error(prediction, sample.future),
        fde=final_displacement_error(prediction, sample.future),
    )
