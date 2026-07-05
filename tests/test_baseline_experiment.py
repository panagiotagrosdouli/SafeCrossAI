from safecrossai.experiments.baseline_experiment import run_constant_velocity_baseline


def test_constant_velocity_experiment_runs() -> None:
    result = run_constant_velocity_baseline()

    assert result.ade == 0.0
    assert result.fde == 0.0
