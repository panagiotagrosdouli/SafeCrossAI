import pytest

from safecrossai.datasets.toy import make_linear_crossing_sample
from safecrossai.training.tensors import samples_to_tensors


def test_samples_to_tensors_shapes() -> None:
    sample = make_linear_crossing_sample(observation_steps=4, prediction_steps=3)

    observed, future = samples_to_tensors([sample])

    assert observed.shape == (1, 4, 2)
    assert future.shape == (1, 3, 2)


def test_samples_to_tensors_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="samples must not be empty"):
        samples_to_tensors([])
