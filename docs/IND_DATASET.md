# inD Dataset Adapter

SafeCrossAI includes an initial adapter for inD-style track CSV files.

## Expected Input

The adapter expects a tracks CSV file with at least the following columns:

| Column | Required | Description |
|---|---:|---|
| `trackId` | yes | Unique tracked road-user identifier. |
| `frame` | yes | Frame index. |
| `xCenter` | yes | Agent x position. |
| `yCenter` | yes | Agent y position. |
| `class` | no | Agent class, such as pedestrian, bicycle, car, or truck. |

Additional columns are preserved by the loader but not required for trajectory-window generation.

## Example Usage

```python
from safecrossai.datasets.ind.samples import build_ind_samples
from safecrossai.benchmark.comparison import compare_constant_velocity_and_lstm
from safecrossai.benchmark.report import benchmark_rows_to_markdown

samples = build_ind_samples(
    "data/raw/ind/00_tracks.csv",
    observation_steps=8,
    prediction_steps=12,
)

rows = compare_constant_velocity_and_lstm(samples[:32], lstm_epochs=1)
print(benchmark_rows_to_markdown(rows))
```

## Data Policy

Do not commit raw inD dataset files to the repository. Store them locally under:

```text
data/raw/ind/
```

This path is ignored by `.gitignore`.

## Current Scope

The current adapter supports track-level trajectory extraction. Future versions may add:

- recording metadata,
- map context,
- lane and crosswalk context,
- class filtering,
- train/validation/test splitting,
- interaction-aware multi-agent scene construction.
