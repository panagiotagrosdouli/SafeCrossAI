from safecrossai.benchmark.comparison import evaluate_constant_velocity
from safecrossai.datasets.toy import make_linear_crossing_sample


def test_evaluate_constant_velocity_linear_sample() -> None:
    sample = make_linear_crossing_sample(observation_steps=4, prediction_steps=3)

    row = evaluate_constant_velocity([sample])

    assert row.model == "constant_velocity"
    assert row.samples == 1
    assert row.mean_ade == 0.0
    assert row.mean_fde == 0.0
