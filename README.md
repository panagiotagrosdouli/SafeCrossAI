# SafeCrossAI

Interpretable trajectory prediction and interaction-risk reasoning for vulnerable road users.

SafeCrossAI is a synthetic research prototype for studying hazardous interactions among pedestrians, cyclists, and vehicles. It combines future-motion prediction, dynamic interaction graphs, relative-motion analysis, time-to-collision, closest-point-of-approach reasoning, and interpretable risk states.

## Method

The current implementation includes:

- deterministic intersection scenarios
- constant-velocity trajectory prediction
- heterogeneous interaction graphs
- TTC and CPA analysis
- distance, relative-speed, and conflict-zone reasoning
- interpretable risk states and warning traces
- ADE, FDE, and miss-rate evaluation
- figure, GIF, and video generation

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

## Scope

The current environment is deterministic and synthetic, and the predictor assumes constant velocity. Occlusion, perception errors, public-dataset evaluation, and physical-intersection validation remain incomplete.

Risk categories are heuristic research diagnostics, not calibrated collision probabilities or a standalone traffic-safety system.

[Greek documentation](README_GR.md)