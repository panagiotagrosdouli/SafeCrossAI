# Research Overview

## Motivation

Urban intersections combine dense interactions, heterogeneous road users, occlusions, traffic-control rules, and time-critical decisions. Vulnerable road users (VRUs) such as pedestrians, cyclists, and micromobility riders are especially difficult to model because their future behaviour can be multi-modal and strongly influenced by nearby agents and infrastructure context.

SafeCrossAI studies intelligent infrastructure as an anticipatory system: instead of reacting only after a dangerous configuration appears, the system should represent the scene, forecast likely futures, estimate uncertainty, and identify safety-critical interactions early enough for decision support.

## Central Research Question

> How can intelligent infrastructure anticipate vulnerable road-user behaviour and identify safety-critical interactions before conflicts occur using AI-based perception, trajectory prediction, and uncertainty-aware risk estimation?

## Scientific Hypothesis

Interaction-aware trajectory prediction combined with interpretable risk estimation can provide earlier and more transparent safety signals than independent single-agent prediction alone.

This hypothesis is not yet validated in this repository. The current software establishes the baseline and scaffold required to evaluate it.

## Current Capabilities

Implemented:

- synthetic trajectory sample generation;
- constant-velocity prediction baseline;
- ADE and FDE trajectory metrics;
- agent, scene, and scene-sequence abstractions;
- geometric social-interaction utilities;
- neighbor search;
- time-to-collision and closest-point-of-approach utilities;
- directed radius-based interaction graphs;
- deterministic baseline risk scoring;
- visualization and demo generation scaffold.

## Current Limitations

- No public dataset benchmark has been reported.
- No trained neural trajectory-prediction model is included.
- No infrastructure perception model is implemented.
- No calibrated uncertainty model exists yet.
- No real-world smart-intersection deployment is claimed.

## Intended Contributions

1. A reproducible research scaffold for VRU trajectory prediction and intelligent-intersection safety.
2. A clean separation between prediction, interaction modelling, risk estimation, evaluation, and visualization.
3. Deterministic baselines that can be used before introducing learning-based models.
4. A documentation structure suitable for a publication-oriented robotics repository.

## Potential PhD Extensions

- Graph neural networks for interaction-aware forecasting.
- Multi-modal future prediction and calibrated uncertainty.
- Infrastructure-to-vehicle cooperative perception.
- Digital-twin evaluation in CARLA or SUMO.
- Risk-aware decision support for autonomous vehicles or traffic infrastructure.
- Rare-event safety evaluation and near-miss mining.

## Publication Roadmap

A publication should only be prepared after reproducible results exist. A plausible roadmap is:

1. publish baseline and dataset-loader scaffold;
2. reproduce constant-velocity and simple learned baselines on a public dataset;
3. add interaction-aware risk scoring;
4. evaluate conflict-detection metrics;
5. submit to an intelligent-transportation or robotics workshop before targeting a full conference paper.
