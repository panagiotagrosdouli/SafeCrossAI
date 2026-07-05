# LSTM Evaluation

SafeCrossAI includes an evaluation helper for LSTM trajectory prediction models.

## Metrics

The current LSTM evaluation pipeline reports:

- number of evaluated samples,
- mean Average Displacement Error,
- mean Final Displacement Error.

## Example

```python
from safecrossai.datasets.toy import make_linear_crossing_sample
from safecrossai.evaluation.lstm import evaluate_lstm_model
from safecrossai.training.loops import fit_lstm_baseline

sample = make_linear_crossing_sample(observation_steps=8, prediction_steps=12)
model, history = fit_lstm_baseline([sample], epochs=5)
summary = evaluate_lstm_model(model, [sample])

print(summary.mean_ade)
print(summary.mean_fde)
```

## Research Use

This makes the LSTM baseline directly comparable with the constant-velocity baseline. The next step is to evaluate both baselines on the same CSV or public-dataset samples.
