import numpy as np

from safecrossai.datasets.toy import make_linear_crossing_sample
from safecrossai.evaluation.lstm import evaluate_lstm_model
from safecrossai.training.loops import fit_lstm_baseline


def test_evaluate_lstm_model_returns_finite_metrics() -> None:
    sample = make_linear_crossing_sample(observation_steps=4, prediction_steps=3)
    model, _ = fit_lstm_baseline([sample], epochs=1, hidden_dim=8)

    summary = evaluate_lstm_model(model, [sample])

    assert summary.samples == 1
    assert np.isfinite(summary.mean_ade)
    assert np.isfinite(summary.mean_fde)
    assert summary.mean_ade >= 0.0
    assert summary.mean_fde >= 0.0
