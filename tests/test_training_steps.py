import torch

from safecrossai.datasets.toy import make_linear_crossing_sample
from safecrossai.prediction.lstm import LSTMTrajectoryPredictor
from safecrossai.training.steps import lstm_update_step
from safecrossai.training.tensors import samples_to_tensors


def test_lstm_update_step_returns_finite_loss() -> None:
    sample = make_linear_crossing_sample(observation_steps=4, prediction_steps=3)
    observed, future = samples_to_tensors([sample])
    model = LSTMTrajectoryPredictor(hidden_dim=8, prediction_steps=3)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    loss = lstm_update_step(model, observed, future, optimizer)

    assert loss >= 0.0
    assert torch.isfinite(torch.tensor(loss))
