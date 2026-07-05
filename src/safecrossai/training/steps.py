"""Small optimization-step helpers for neural baselines."""

from __future__ import annotations

import torch
from torch import nn

from safecrossai.prediction.lstm import LSTMTrajectoryPredictor


def lstm_update_step(
    model: LSTMTrajectoryPredictor,
    observed: torch.Tensor,
    future: torch.Tensor,
    optimizer: torch.optim.Optimizer,
) -> float:
    """Run one supervised update step and return the loss value."""
    model.train()
    optimizer.zero_grad()
    prediction = model(observed)
    loss = nn.functional.mse_loss(prediction, future)
    loss.backward()
    optimizer.step()
    return float(loss.detach().cpu().item())
