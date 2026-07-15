<div align="center">

# SafeCrossAI

## Interpretable Trajectory Prediction and Interaction-Risk Reasoning for Intelligent Intersections

A synthetic research framework for anticipating vulnerable-road-user motion and explaining safety-critical interactions before collision.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](.) [![Status](https://img.shields.io/badge/status-research%20prototype-orange)](.) [![Evidence](https://img.shields.io/badge/evidence-synthetic%20demo-yellow)](.)

**English** · [Ελληνικά](README_GR.md)

</div>

<p align="center"><img src="assets/readme/safecrossai_pipeline.svg" alt="SafeCrossAI research pipeline" width="100%" /></p>

<p align="center"><em>Conceptual synthetic research figure. It is not a real-intersection benchmark, calibrated collision probability, or traffic-control safety guarantee.</em></p>

## Abstract

SafeCrossAI investigates how intelligent intersections can anticipate hazardous interactions among pedestrians, cyclists, and vehicles. The repository combines deterministic trajectory generation, a transparent motion-prediction baseline, dynamic interaction graphs, relative-motion analysis, time-to-collision, closest-point-of-approach reasoning, risk classification, event detection, and interpretable warning evidence.

The project treats traffic safety as more than displacement prediction. A trajectory model can achieve low average error while still missing a rare critical interaction. SafeCrossAI therefore evaluates prediction and interaction safety jointly, while keeping every warning traceable to the agents, predicted paths, geometric indicators, context, and triggering rule.

## Research question

> How can an intelligent intersection combine trajectory prediction, interaction reasoning, and interpretable risk indicators to detect dangerous road-user encounters early enough to support preventive action?

## Architecture

```text
intersection scenario
  → observed pedestrian, cyclist, and vehicle trajectories
  → future-motion prediction
  → dynamic pairwise interaction graph
  → distance and relative-velocity analysis
  → TTC and CPA estimation
  → LOW / MEDIUM / HIGH / CRITICAL risk state
  → conflict event, explanation, metrics, and media
```

## Safety formulation

For relative position `r` and relative velocity `v`,

```math
t_{TTC}=-\frac{r^Tv}{\|v\|^2}
```

when agents are converging. Closest approach is evaluated using

```math
t_{CPA}=\max\left(0,-\frac{r^Tv}{\|v\|^2}\right),
\qquad
d_{CPA}=\|r+t_{CPA}v\|.
```

These indicators are combined with distance, speed, agent type, and conflict-zone context. The resulting risk categories are interpretable research diagnostics, not calibrated collision probabilities.

## Research contributions

- reproducible synthetic intersection laboratory;
- transparent constant-velocity baseline;
- dynamic heterogeneous interaction graph;
- TTC, CPA, distance, relative-speed, and conflict-zone reasoning;
- inspectable risk states and warning explanations;
- end-to-end generation of trajectories, events, metrics, figures, GIF, and MP4;
- claim-disciplined separation of implemented, prototype, and planned capabilities.

## Verified scope

| Area | Status |
|---|---|
| Synthetic intersection simulation | Implemented |
| Constant-velocity prediction | Implemented |
| Interaction graph construction | Implemented |
| Interpretable risk scoring | Implemented |
| Conflict-event detection | Implemented |
| ADE, FDE, and miss-rate evaluation | Implemented |
| Figures, GIF, and MP4 generation | Implemented |
| Dataset loaders | Prototype |
| Perception uncertainty | Prototype / planned |
| Learning-based prediction | Planned |
| Real-world intersection validation | Pending |

## Reproduce

```bash
git clone https://github.com/panagiotagrosdouli/SafeCrossAI.git
cd SafeCrossAI
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,demo]"
python scripts/run_all.py
pytest
```

## Evaluation protocol

Prediction metrics include ADE, FDE, miss rate, and per-agent-type error. Safety metrics should include conflict precision and recall, warning lead time, minimum predicted separation, TTC/CPA error, false alerts, missed critical interactions, and risk-state stability. Learning-based baselines should not be reported without committed models, splits, seeds, configurations, and outputs.

## Limitations

- The environment is deterministic and synthetic.
- The current predictor assumes constant velocity.
- Occlusion, missed detections, identity switches, and perception noise are simplified.
- TTC and CPA rely on simplified relative-motion assumptions.
- Risk categories are heuristic and uncalibrated.
- Public-dataset and physical-intersection validation remain pending.
- The system is not a standalone collision-avoidance or traffic-control system.

## Responsible use

SafeCrossAI outputs are diagnostic research signals and must not be used as the sole basis for real-world traffic-control, collision-avoidance, or public-safety decisions.
