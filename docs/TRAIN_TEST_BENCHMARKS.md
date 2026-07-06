# Train/Test Benchmark Protocol

SafeCrossAI supports a simple deterministic train/test protocol for baseline comparison.

## Why Train/Test Splitting Matters

A neural model such as LSTM should not be evaluated only on the same samples used for training. The train/test split provides a more scientifically meaningful comparison.

## Current Protocol

1. Split trajectory samples into train and test partitions.
2. Train the LSTM baseline on the train partition.
3. Evaluate the LSTM baseline on the test partition.
4. Evaluate constant velocity on the same test partition.
5. Report ADE and FDE for both models.

## Example

```python
from safecrossai.benchmark.comparison import compare_with_train_test_split
from safecrossai.benchmark.report import benchmark_rows_to_markdown
from safecrossai.datasets.ind.samples import build_ind_samples

samples = build_ind_samples(
    "data/raw/ind/00_tracks.csv",
    observation_steps=8,
    prediction_steps=12,
    classes={"pedestrian", "bicycle"},
)

rows = compare_with_train_test_split(samples, test_fraction=0.2, lstm_epochs=5)
print(benchmark_rows_to_markdown(rows))
```

## Notes

This is still a lightweight protocol. Future versions should add scene-level splits so that trajectories from the same recording are not split across train and test partitions.
