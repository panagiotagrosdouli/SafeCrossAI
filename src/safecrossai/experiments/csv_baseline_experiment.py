"""Run baseline trajectory prediction on CSV trajectory data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from safecrossai.datasets.csv_loader import build_samples_from_csv
from safecrossai.evaluation.metrics import average_displacement_error, final_displacement_error
from safecrossai.prediction.baseline import constant_velocity_predict


@dataclass(frozen=True)
class CsvBaselineSummary:
    """Aggregate metrics for a CSV baseline experiment."""

    samples: int
    mean_ade: float
    mean_fde: float


def run_csv_constant_velocity_baseline(
    path: str | Path,
    observation_steps: int = 8,
    prediction_steps: int = 12,
) -> CsvBaselineSummary:
    """Run the constant-velocity baseline on all valid CSV trajectory windows."""
    samples = build_samples_from_csv(
        path,
        observation_steps=observation_steps,
        prediction_steps=prediction_steps,
    )
    if not samples:
        raise ValueError("no valid trajectory samples found")

    ade_values: list[float] = []
    fde_values: list[float] = []

    for sample in samples:
        prediction = constant_velocity_predict(sample.observed, horizon=len(sample.future))
        ade_values.append(average_displacement_error(prediction, sample.future))
        fde_values.append(final_displacement_error(prediction, sample.future))

    return CsvBaselineSummary(
        samples=len(samples),
        mean_ade=sum(ade_values) / len(ade_values),
        mean_fde=sum(fde_values) / len(fde_values),
    )
