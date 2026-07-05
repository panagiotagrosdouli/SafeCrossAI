import torch

from safecrossai.datasets.toy import make_linear_crossing_sample
from safecrossai.training.loops import fit_lstm_baseline


def test_fit_lstm_baseline_returns_history_and_model() -> None:
    sample = make_linear_crossing_sample(observation_steps=4, prediction_steps=3)

    model, history = fit_lstm_baseline([sample], epochs=2, hidden_dim=8)

    assert history.epochs == 2
    assert len(history.losses) == 2
    assert history.final_loss >= 0.0

    observed = torch.zeros(1, 4, 2)
    prediction = model(observed)
    assert prediction.shape == (1, 3, 2)
