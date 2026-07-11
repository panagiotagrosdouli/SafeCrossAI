# Scientific Report

## Scope

SafeCrossAI is a research-grade scaffold for intelligent-intersection analysis, vulnerable road-user trajectory prediction, interaction modelling, and uncertainty-aware risk estimation. It is currently a baseline and infrastructure project, not a validated deployment system.

## Research Question

How can intelligent infrastructure anticipate vulnerable road-user behaviour and identify safety-critical interactions before collisions occur using perception, trajectory prediction, social interaction modelling, and interpretable risk metrics?

## Implemented Contributions

- Synthetic trajectory generation for deterministic smoke tests.
- Constant-velocity and least-squares linear trajectory baselines.
- ADE/FDE trajectory metrics and risk/conflict utilities.
- Social-agent abstractions and radius/k-nearest-neighbour interaction graphs.
- Time-to-collision and closest-point-of-approach reasoning.
- Visualization scaffold for trajectory, graph, and risk overlays.

## Scientific Impact

The project provides a transparent foundation for future research in infrastructure-assisted VRU safety. Its main value is methodological: it separates scene representation, prediction, interaction graphs, risk estimation, and evaluation so that future neural models and public datasets can be added without hiding assumptions.

## Limitations

- Current demos are synthetic and should not be interpreted as real-world benchmark evidence.
- Public dataset loaders and benchmark protocols are planned, not validated.
- Neural predictors and uncertainty calibration are prototype/planned items.
- Infrastructure perception is not yet connected to real sensors.
- No deployment, safety certification, or state-of-the-art performance claim is made.

## Future Research Directions

1. Add public dataset loaders with explicit license and split documentation.
2. Add interaction-aware neural predictors and uncertainty calibration.
3. Validate risk metrics on real intersection datasets.
4. Add CARLA/SUMO digital-twin experiments.
5. Compare against established trajectory-prediction baselines after reproducible data support exists.
