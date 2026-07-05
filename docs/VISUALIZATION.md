# Visualization

SafeCrossAI includes lightweight trajectory visualization utilities for inspecting prediction results.

## Trajectory Prediction Plot

The core visualization shows:

- observed trajectory,
- ground-truth future trajectory,
- predicted future trajectory,
- final observed position.

## Example Usage

```python
from safecrossai.datasets.toy import make_linear_crossing_sample
from safecrossai.prediction.baseline import constant_velocity_predict
from safecrossai.visualization.trajectories import plot_trajectory_prediction

sample = make_linear_crossing_sample()
prediction = constant_velocity_predict(sample.observed, horizon=len(sample.future))

figure = plot_trajectory_prediction(
    observed=sample.observed,
    future=sample.future,
    prediction=prediction,
    save_path="outputs/toy_prediction.png",
)
```

## Research Use

Visualization is useful for:

- debugging trajectory preprocessing,
- checking whether baseline models behave correctly,
- comparing predicted and true future motion,
- preparing figures for reports, presentations, and papers.

Future visualization modules may include:

- multi-agent scene plots,
- conflict-zone visualization,
- uncertainty ellipses,
- smart-intersection dashboards,
- simulation replay videos.
