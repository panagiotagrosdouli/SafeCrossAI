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

Optional velocity columns are also supported for scene construction:

| Column | Required | Description |
|---|---:|---|
| `xVelocity` | no | Agent x velocity. |
| `yVelocity` | no | Agent y velocity. |

Additional columns are preserved by the loader but not required for trajectory-window generation.

## Trajectory Sample Usage

```python
from safecrossai.datasets.ind.samples import build_ind_samples
from safecrossai.benchmark.comparison import compare_constant_velocity_and_lstm
from safecrossai.benchmark.report import benchmark_rows_to_markdown

samples = build_ind_samples(
    "data/raw/ind/00_tracks.csv",
    observation_steps=8,
    prediction_steps=12,
    classes={"pedestrian", "bicycle"},
)

rows = compare_constant_velocity_and_lstm(samples[:32], lstm_epochs=1)
print(benchmark_rows_to_markdown(rows))
```

## Scene Usage

The inD adapter can also build frame-level `Scene` objects for social-interaction modeling.

```python
from safecrossai.datasets.ind.scenes import build_ind_scenes

scenes = build_ind_scenes(
    "data/raw/ind/00_tracks.csv",
    classes={"pedestrian", "bicycle"},
)

scene = scenes[0]
graph = scene.build_interaction_graph(radius=5.0)

print(scene.agent_ids())
print(graph.edges)
```

## Scene Sequence Usage

Frame-level scenes can be converted into temporal `SceneSequence` windows for future Social-LSTM, GNN, Transformer, and Diffusion models.

```python
from safecrossai.datasets.ind.scenes import build_ind_scene_sequences

sequences = build_ind_scene_sequences(
    "data/raw/ind/00_tracks.csv",
    sequence_length=8,
    stride=1,
    classes={"pedestrian", "bicycle"},
)

print(sequences[0].start_time)
print(sequences[0].end_time)
print(sequences[0].agent_ids())
```

This connects real inD-style tracks to SafeCrossAI's unified social representation:

```text
inD tracks CSV
      ↓
frame-level Scene
      ↓
SceneSequence
      ↓
SocialAgent nodes over time
      ↓
temporal interaction graphs
      ↓
future Social-LSTM / GNN / Transformer models
```

## CLI Scene Summary

Use the CLI to quickly inspect how many scenes, agents, interaction edges, and optional scene sequences an inD-style tracks file produces.

```bash
safecrossai ind-scene-summary data/raw/ind/00_tracks.csv \
  --radius 5.0 \
  --sequence-length 8 \
  --stride 1 \
  --classes pedestrian bicycle
```

Example output:

```text
scenes: 1200
agents: 8421
mean_agents_per_scene: 7.02
interaction_edges: 18432
mean_edges_per_scene: 15.36
scene_sequences: 1193
sequence_length: 8
sequence_stride: 1
```

This command is useful before training interaction-aware models because it checks whether the selected radius, class filters, and temporal window length produce meaningful social inputs.

## Data Policy

Do not commit raw inD dataset files to the repository. Store them locally under:

```text
data/raw/ind/
```

This path is ignored by `.gitignore`.

## Current Scope

The current adapter supports:

- track-level trajectory extraction,
- class filtering,
- frame-level scene construction,
- social-agent conversion,
- interaction graph construction from scenes,
- scene sequence construction,
- CLI scene summary for social graph and temporal sequence inspection.

Future versions may add:

- recording metadata,
- map context,
- lane and crosswalk context,
- scene-level train/validation/test splitting,
- map-aware interaction graphs.
