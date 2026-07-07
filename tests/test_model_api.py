from pathlib import Path
from typing import Any, Iterable

import numpy as np

from safecrossai.models import PredictionOutput, TrajectoryPredictor


class DummyPredictor(TrajectoryPredictor):
    def fit(self, samples: Iterable[Any]) -> None:
        self.samples = list(samples)

    def predict(self, sample: Any) -> PredictionOutput:
        return PredictionOutput(
            trajectories=np.asarray(sample, dtype=float),
            confidence=1.0,
            metadata={"model": "dummy"},
        )

    def save(self, path: str | Path) -> None:
        Path(path).write_text("dummy", encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "DummyPredictor":
        Path(path).read_text(encoding="utf-8")
        return cls()


def test_prediction_output_stores_prediction_metadata() -> None:
    output = PredictionOutput(
        trajectories=np.array([[1.0, 2.0]]),
        confidence=0.9,
        runtime_seconds=0.01,
        metadata={"model": "test"},
    )

    np.testing.assert_allclose(output.trajectories, np.array([[1.0, 2.0]]))
    assert output.confidence == 0.9
    assert output.runtime_seconds == 0.01
    assert output.metadata["model"] == "test"


def test_predict_batch_uses_predict_for_each_sample() -> None:
    predictor = DummyPredictor()

    outputs = predictor.predict_batch([[[0.0, 0.0]], [[1.0, 1.0]]])

    assert len(outputs) == 2
    np.testing.assert_allclose(outputs[1].trajectories, np.array([[1.0, 1.0]]))
    assert outputs[0].metadata["model"] == "dummy"


def test_predictor_save_and_load(tmp_path: Path) -> None:
    path = tmp_path / "predictor.txt"
    predictor = DummyPredictor()

    predictor.save(path)
    loaded = DummyPredictor.load(path)

    assert isinstance(loaded, DummyPredictor)
