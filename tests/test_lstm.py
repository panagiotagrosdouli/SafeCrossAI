import pytest
import torch

from safecrossai.prediction.lstm import LSTMTrajectoryPredictor


def test_lstm_predictor_output_shape() -> None:
    model = LSTMTrajectoryPredictor(hidden_dim=16, prediction_steps=5)
    observed = torch.zeros(4, 8, 2)

    prediction = model(observed)

    assert prediction.shape == (4, 5, 2)


def test_lstm_predictor_rejects_invalid_input_shape() -> None:
    model = LSTMTrajectoryPredictor(hidden_dim=16, prediction_steps=5)

    with pytest.raises(ValueError, match="observed must have shape"):
        model(torch.zeros(8, 2))
