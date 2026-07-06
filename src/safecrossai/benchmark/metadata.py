"""Benchmark metadata models."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class BenchmarkMetadata:
    """Metadata describing a benchmark run."""

    dataset: str
    protocol: str
    observation_steps: int
    prediction_steps: int
    lstm_epochs: int
    hidden_dim: int
    samples: int
    classes: list[str] | None = None
    test_fraction: float | None = None
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return metadata as a serializable dictionary."""
        return asdict(self)
