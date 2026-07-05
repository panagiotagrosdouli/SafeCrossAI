# LSTM Baseline

SafeCrossAI includes a minimal PyTorch LSTM trajectory-prediction baseline.

## Purpose

The LSTM baseline is not intended to be the final research contribution. It provides a standard neural baseline against which more advanced models can be compared.

## Model

The model receives observed 2D positions:

```text
batch x observation_steps x 2
```

and predicts future 2D positions:

```text
batch x prediction_steps x 2
```

## Example

```python
import torch

from safecrossai.prediction.lstm import LSTMTrajectoryPredictor

model = LSTMTrajectoryPredictor(hidden_dim=64, prediction_steps=12)
observed = torch.zeros(4, 8, 2)
prediction = model(observed)

print(prediction.shape)  # torch.Size([4, 12, 2])
```

## Research Role

This baseline supports the diploma thesis by providing a first neural model for comparison with:

- constant-velocity prediction,
- graph neural networks,
- transformer-based motion forecasting,
- uncertainty-aware predictors,
- interaction-aware models.

## Next Steps

- Add a lightweight training loop.
- Add CSV-based tensor conversion.
- Add model checkpointing.
- Add evaluation against ADE and FDE.
- Compare LSTM against the constant-velocity baseline.
