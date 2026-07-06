# Benchmarks

SafeCrossAI includes a benchmark layer for comparing trajectory prediction baselines under reproducible evaluation protocols.

## Current Models

- Constant Velocity
- LSTM

## Current Metrics

- Mean Average Displacement Error
- Mean Final Displacement Error

## Benchmark Protocols

### 1. Same-samples protocol

The same samples are used for training and evaluation. This is useful only for smoke tests and early debugging.

```python
from safecrossai.benchmark.comparison import compare_constant_velocity_and_lstm
```

### 2. Train/test protocol

Samples are randomly split into train and test partitions. The LSTM is trained on train samples and evaluated on test samples. Constant velocity is evaluated on the same test samples.

```python
from safecrossai.benchmark.comparison import compare_with_train_test_split
```

### 3. Grouped train/test protocol

Samples are split by `group_id`, so all trajectory windows from the same track or scene stay either in train or test. This reduces data leakage and is preferred for real datasets.

```python
from safecrossai.benchmark.comparison import compare_with_grouped_train_test_split
```

For inD-style data, `group_id` is currently derived from `trackId`.

## CLI Examples

Toy benchmark:

```bash
safecrossai toy-benchmark --observation-steps 8 --prediction-steps 12
```

inD same-samples benchmark:

```bash
safecrossai ind-benchmark data/raw/ind/00_tracks.csv --classes pedestrian bicycle
```

inD grouped benchmark:

```bash
safecrossai ind-benchmark data/raw/ind/00_tracks.csv \
  --classes pedestrian bicycle \
  --grouped-split \
  --test-fraction 0.2 \
  --seed 42
```

Export paper-ready reports:

```bash
safecrossai ind-benchmark data/raw/ind/00_tracks.csv \
  --classes pedestrian bicycle \
  --grouped-split \
  --output-csv outputs/ind_results.csv \
  --output-json outputs/ind_results.json \
  --output-md outputs/ind_report.md
```

## Research Use

The benchmark layer makes it possible to compare classical and neural trajectory predictors under the same evaluation protocol. The grouped train/test protocol is the recommended default for real trajectory datasets because it reduces leakage between training and evaluation windows.
