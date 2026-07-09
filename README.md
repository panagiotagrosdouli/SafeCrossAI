# SafeCrossAI

<p align="center"><strong>SafeCrossAI — Synthetic Demo intelligent-intersection risk assessment for vulnerable road-user safety.</strong></p>

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Tests](https://img.shields.io/badge/tests-pytest-green) ![Demo](https://img.shields.io/badge/results-Synthetic%20Demo-orange)

SafeCrossAI asks: **How can intelligent intersections anticipate vulnerable road-user behaviour and identify safety-critical interactions before collisions occur?**

This repository is a working research prototype, not only documentation. It generates deterministic synthetic intersection trajectories, predicts futures with transparent baselines, builds interaction graphs, computes time-to-collision and closest-point-of-approach risk scores, detects conflicts, evaluates metrics, and creates figures, `demo.gif`, and `demo.mp4` from code. All generated demo outputs are explicitly labelled **Synthetic Demo** and must not be interpreted as real-world benchmark evidence.

## Run the full Synthetic Demo

```bash
python -m pip install -e .[dev,demo]
python scripts/run_all.py
pytest
```

`python scripts/run_all.py` produces:

- `results/scene_metadata.json`
- `results/observed_trajectories.csv`
- `results/ground_truth_future.csv`
- `results/predicted_trajectories.csv`
- `results/agent_states.csv`
- `results/interaction_edges.csv`
- `results/risk_scores.csv`
- `results/conflict_events.csv`
- `results/simulation_summary.json`
- `results/metrics/summary.json`
- `results/metrics/metrics.csv`
- `results/figures/*.png`
- `results/videos/safecrossai_demo.gif`
- `results/videos/safecrossai_demo.mp4`
- `assets/figures/*.png`
- `assets/gifs/demo.gif`
- `assets/videos/demo.mp4`

## Implemented / Prototype / Planned

| Area | Status | Notes |
|---|---:|---|
| Synthetic intelligent-intersection simulation | Implemented | Pedestrian, cyclist, vehicles, observed trajectories, future ground truth, lanes/crosswalk/conflict-zone metadata. |
| Constant-velocity future prediction | Implemented | Transparent baseline only. |
| Interaction graph with TTC and CPA | Implemented | Pairwise distance, relative speed, TTC, closest approach, edge status. |
| Interpretable risk scoring and conflict detection | Implemented | LOW/MEDIUM/HIGH/CRITICAL with warning flags and explanations. |
| Evaluation metrics | Implemented | ADE, FDE, miss rate and generated summary metrics. |
| Generated figures, GIF, MP4 | Implemented | Produced from code by `scripts/run_all.py`. |
| Dataset loaders | Prototype | Custom CSV and public dataset scaffolds; datasets are not redistributed. |
| Learning-based/GNN prediction | Planned | No neural benchmark claims. |
| Real-world benchmark results | Planned | No fabricated results. |

## Scientific motivation

Trajectory prediction alone is insufficient for intelligent-intersection safety because accurate average forecasts may still hide safety-critical interactions. SafeCrossAI couples motion extrapolation with interpretable interaction features, TTC, CPA, and thresholded risk states so the output can be inspected as a safety argument.

## Docker

```bash
docker build -t safecrossai .
docker run --rm -v "$PWD/results:/app/results" safecrossai
```

## Limitations

The current demo is deterministic and synthetic. It does not model perception errors beyond placeholders, does not calibrate uncertainty as probability, and does not claim deployment readiness or state-of-the-art performance.

## Citation

Use `CITATION.cff`. A formal paper citation will be added only after a validated manuscript exists.
