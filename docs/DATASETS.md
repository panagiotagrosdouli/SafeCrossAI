# Datasets

SafeCrossAI currently includes only synthetic toy and demo scenarios. These are useful for smoke tests, examples, and visualization, but they are not benchmark datasets.

## Current Data

### Synthetic toy trajectory

Status: **Implemented**

Used for deterministic baseline testing.

### Synthetic demo scenario

Status: **Implemented**

Used for GIF/MP4 demo generation and visualization smoke tests.

## Common CSV Format

The simplest planned interchange format is a CSV file with the following columns:

| Column | Required | Description |
|---|---:|---|
| `scene_id` | yes | Unique scene or recording identifier. |
| `agent_id` | yes | Unique road-user identifier within the scene. |
| `frame` | yes | Temporal frame index. |
| `x` | yes | Local x coordinate in meters or normalized map units. |
| `y` | yes | Local y coordinate in meters or normalized map units. |
| `agent_type` | no | Road-user class, for example `pedestrian`, `cyclist`, `vehicle`, or `escooter`. |

## Planned Public Datasets

The following datasets are relevant to the research direction but are not yet implemented as loaders:

- inD Dataset
- rounD Dataset
- highD Dataset
- INTERACTION Dataset
- Argoverse 2 Motion Forecasting
- Waymo Open Motion Dataset
- nuScenes prediction-related data
- V2X and infrastructure-perception datasets

## Dataset Loader Requirements

Each loader must document:

- dataset source;
- license and citation;
- coordinate frame;
- sampling rate;
- agent types;
- map context availability;
- official splits if available;
- preprocessing steps;
- limitations.

## Data Policy

Raw datasets should not be committed to the repository. Store them locally under ignored directories such as:

```text
data/raw/
data/interim/
data/processed/
```

Only lightweight examples, schemas, and preprocessing code should be committed.

## No Fictional Datasets

This repository must not invent dataset names or report results on unavailable data. Synthetic scenarios must always be labelled synthetic.
