"""Baseline comparison utilities."""

from __future__ import annotations

from dataclasses import dataclass

from safecrossai.datasets.toy import TrajectorySample
from safecrossai.evaluation.lstm import evaluate_lstm_model
from safecrossai.evaluation.metrics import average_displacement_error, final_displacement_error
from safecrossai.prediction.baseline import constant_velocity_predict
from safecrossai.training.loops import fit_lstm_baseline


@dataclass(frozen=True)
class BenchmarkRow:
    """One model row in a benchmark table."""

    model: str
    samples: int
    mean_ade: float
    mean_fde: float


def evaluate_constant_velocity(samples: list[TrajectorySample]) -> BenchmarkRow:
    """Evaluate the constant-velocity baseline on trajectory samples."""
    if not samples:
        raise ValueError("samples must not be empty")

    ade_values: list[float] = []
    fde_values: list[float] = []

    for sample in samples:
        prediction = constant_velocity_predict(sample.observed, horizon=len(sample.future))
        ade_values.append(average_displacement_error(prediction, sample.future))
        fde_values.append(final_displacement_error(prediction, sample.future))

    return BenchmarkRow(
        model="constant_velocity",
        samples=len(samples),
        mean_ade=sum(ade_values) / len(ade_values),
        mean_fde=sum(fde_values) / len(fde_values),
    )


def compare_constant_velocity_and_lstm(
    samples: list[TrajectorySample],
    lstm_epochs: int = 1,
    hidden_dim: int = 8,
) -> list[BenchmarkRow]:
    """Compare constant velocity and LSTM on the same trajectory samples."""
    constant_velocity = evaluate_constant_velocity(samples)
    lstm_model, _ = fit_lstm_baseline(samples, epochs=lstm_epochs, hidden_dim=hidden_dim)
    lstm_summary = evaluate_lstm_model(lstm_model, samples)

    return [
        constant_velocity,
        BenchmarkRow(
            model="lstm",
            samples=lstm_summary.samples,
            mean_ade=lstm_summary.mean_ade,
            mean_fde=lstm_summary.mean_fde,
        ),
    ]
