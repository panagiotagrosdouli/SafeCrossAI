import numpy as np

from safecrossai.benchmark.comparison import compare_constant_velocity_and_lstm
from safecrossai.datasets.toy import make_linear_crossing_sample


def test_compare_constant_velocity_and_lstm_returns_two_rows() -> None:
    sample = make_linear_crossing_sample(observation_steps=4, prediction_steps=3)

    rows = compare_constant_velocity_and_lstm([sample], lstm_epochs=1, hidden_dim=8)

    assert [row.model for row in rows] == ["constant_velocity", "lstm"]
    assert all(row.samples == 1 for row in rows)
    assert all(np.isfinite(row.mean_ade) for row in rows)
    assert all(np.isfinite(row.mean_fde) for row in rows)
