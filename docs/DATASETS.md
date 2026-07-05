# Datasets

SafeCrossAI is designed to support multiple trajectory-prediction datasets through a common internal format.

## Common CSV Format

The simplest supported format is a CSV file with the following columns:

| Column | Required | Description |
|---|---:|---|
| `scene_id` | yes | Unique scene or recording identifier. |
| `agent_id` | yes | Unique road-user identifier within the scene. |
| `frame` | yes | Temporal frame index. |
| `x` | yes | Local x coordinate in meters or normalized map units. |
| `y` | yes | Local y coordinate in meters or normalized map units. |
| `agent_type` | no | Road-user class, for example `pedestrian`, `cyclist`, `vehicle`, or `escooter`. |

## Example

```csv
scene_id,agent_id,frame,x,y,agent_type
1,10,0,0.0,0.0,pedestrian
1,10,1,0.5,0.2,pedestrian
1,10,2,1.0,0.4,pedestrian
1,10,3,1.5,0.6,pedestrian
1,10,4,2.0,0.8,pedestrian
```

## Windowing

A trajectory is converted into samples using two parameters:

- `observation_steps`: number of past positions given to the model.
- `prediction_steps`: number of future positions the model must predict.

For example, with `observation_steps=8` and `prediction_steps=12`, each sample contains 20 consecutive positions.

## Planned Dataset Adapters

- `inD`: intersection drone-based road-user trajectories.
- `rounD`: roundabout road-user trajectories.
- `INTERACTION`: interaction-rich driving scenarios.
- `Argoverse 2 Motion Forecasting`: autonomous-driving motion forecasting.
- `nuScenes`: autonomous-driving dataset with perception and tracking context.
- `Waymo Open Motion Dataset`: large-scale motion forecasting benchmark.

## Data Policy

Raw datasets should not be committed to the repository. Store them locally under ignored directories such as:

```text
data/raw/
data/interim/
data/processed/
```

Only lightweight examples, schemas, and preprocessing code should be committed.
