# System Architecture

SafeCrossAI is organized as a modular research stack. Each module should be independently testable and should avoid circular dependencies.

## High-Level Architecture

```text
Infrastructure Sensors / Simulation
        |
        v
Perception and Tracking        [Prototype]
        |
        v
Scene Representation           [Implemented scaffold]
        |
        v
Trajectory Prediction          [Baseline implemented]
        |
        v
Interaction Modelling          [Implemented]
        |
        v
Risk Estimation                [Baseline implemented]
        |
        v
Evaluation and Visualization   [Scaffold implemented]
```

## Module Responsibilities

### `safecrossai.datasets`
Provides toy data and future public-dataset loaders. Current implementation includes deterministic synthetic trajectories and demo scenarios.

### `safecrossai.prediction`
Contains trajectory-prediction models. Current implementation includes a constant-velocity baseline. Learning-based predictors are planned.

### `safecrossai.social`
Contains social-interaction utilities: geometry, agents, scenes, sequences, neighbor search, time-to-collision, closest point of approach, and interaction graphs.

### `safecrossai.risk`
Contains interpretable baseline risk scoring. Current scores combine proximity, time-to-interaction, and closest-approach information. They are not calibrated probabilities.

### `safecrossai.evaluation`
Contains trajectory and classification metrics. Current metrics support ADE, FDE, miss rate, precision, recall, F1, confusion matrix, ROC/PR points, and calibration error.

### `safecrossai.visualization`
Contains plotting and animation helpers for scientific communication.

### `safecrossai.perception`
Planned module for infrastructure-based object detection, tracking, and sensor fusion. No perception benchmark is claimed yet.

### `safecrossai.simulation`
Planned module for CARLA/SUMO digital-twin integration.

## Engineering Rationale

The architecture separates physical observations, state representation, prediction, interaction reasoning, risk scoring, and evaluation. This makes it possible to replace a baseline predictor with a neural model without changing the risk or evaluation APIs.

## Dependency Direction

Recommended dependency flow:

```text
datasets -> social -> prediction -> risk -> evaluation -> visualization
```

Visualization may depend on most modules, but core scientific modules should not depend on visualization.

## Future Extensions

- Add typed dataset interfaces.
- Add model registry for predictors.
- Add experiment registry for reproducible runs.
- Add benchmark result schema.
- Add CI checks for dependency direction.
