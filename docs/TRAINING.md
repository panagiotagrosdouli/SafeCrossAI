# Training Utilities

SafeCrossAI now includes a lightweight training path for the LSTM baseline.

## Components

- `training/tensors.py`: converts trajectory samples to PyTorch tensors.
- `training/steps.py`: runs one supervised optimization step.
- `training/loops.py`: fits an LSTM baseline for a small number of epochs.

## Example

```python
from safecrossai.datasets.toy import make_linear_crossing_sample
from safecrossai.training.loops import fit_lstm_baseline

sample = make_linear_crossing_sample(observation_steps=8, prediction_steps=12)
model, history = fit_lstm_baseline([sample], epochs=5)

print(history.losses)
print(history.final_loss)
```

## Research Use

This is the first neural training path in SafeCrossAI. It is intentionally simple so it can serve as a reproducible baseline before adding more advanced models.

## Next Steps

- Train LSTM on CSV trajectory samples.
- Add evaluation after training.
- Add model checkpoint saving and loading.
- Add CLI support for LSTM training.
- Compare LSTM with the constant-velocity baseline.
