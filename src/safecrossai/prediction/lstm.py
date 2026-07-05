"""LSTM trajectory prediction baseline."""

from __future__ import annotations

import torch
from torch import nn


class LSTMTrajectoryPredictor(nn.Module):
    """Simple encoder-decoder style LSTM trajectory predictor.

    The model encodes observed 2D positions and predicts a fixed number of
    future 2D positions from the final hidden state.
    """

    def __init__(
        self,
        input_dim: int = 2,
        hidden_dim: int = 64,
        num_layers: int = 1,
        prediction_steps: int = 12,
        output_dim: int = 2,
    ) -> None:
        super().__init__()
        if prediction_steps < 1:
            raise ValueError("prediction_steps must be positive")

        self.prediction_steps = prediction_steps
        self.output_dim = output_dim
        self.encoder = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
        )
        self.head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, prediction_steps * output_dim),
        )

    def forward(self, observed: torch.Tensor) -> torch.Tensor:
        """Predict future trajectories.

        Parameters
        ----------
        observed:
            Tensor with shape ``(batch, observation_steps, 2)``.

        Returns
        -------
        torch.Tensor
            Tensor with shape ``(batch, prediction_steps, 2)``.
        """
        if observed.ndim != 3 or observed.shape[-1] != 2:
            raise ValueError("observed must have shape (batch, observation_steps, 2)")

        _, (hidden, _) = self.encoder(observed)
        final_hidden = hidden[-1]
        output = self.head(final_hidden)
        return output.view(observed.shape[0], self.prediction_steps, self.output_dim)
