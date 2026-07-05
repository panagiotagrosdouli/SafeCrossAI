# Benchmarks

SafeCrossAI includes a first benchmark layer for comparing trajectory prediction baselines on the same samples.

## Current Models

- Constant Velocity
- LSTM

## Current Metrics

- Mean Average Displacement Error
- Mean Final Displacement Error

## Example

```python
from safecrossai.benchmark.comparison import compare_constant_velocity_and_lstm
from safecrossai.benchmark.report import benchmark_rows_to_markdown
from safecrossai.datasets.toy import make_linear_crossing_sample

sample = make_linear_crossing_sample(observation_steps=8, prediction_steps=12)
rows = compare_constant_velocity_and_lstm([sample], lstm_epochs=1)
print(benchmark_rows_to_markdown(rows))
```

## Research Use

The benchmark layer makes it possible to compare classical and neural trajectory predictors under the same evaluation protocol. This is the foundation for later comparisons with graph neural networks, transformers, and uncertainty-aware models.
