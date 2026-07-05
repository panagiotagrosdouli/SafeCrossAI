import pytest

from safecrossai.experiments.baseline_experiment import run_constant_velocity_baseline


def test_constant_velocity_experiment_runs() -> None:
    result = run_constant_velocity_baseline()

    assert result.ade == pytest.approx(0.0)
    assert result.fde == pytest.approx(0.0)
