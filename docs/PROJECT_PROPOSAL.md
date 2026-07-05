# SafeCrossAI Research Project Proposal

## Title

**SafeCrossAI: AI-Powered Infrastructure-Based Trajectory Prediction and Risk Assessment for Vulnerable Road Users at Intelligent Intersections**

## Abstract

SafeCrossAI proposes an intelligent-intersection research platform for improving urban road safety and supporting connected and autonomous driving. The project focuses on predicting the future motion of vulnerable road users, including pedestrians, cyclists, and micromobility users, in complex intersection scenarios. The platform combines infrastructure-based perception, multi-agent scene representation, trajectory prediction, uncertainty estimation, and safety-critical risk assessment.

The project is designed as a research foundation that can evolve from a diploma thesis into a larger doctoral research agenda. Its scientific contribution lies in integrating trajectory forecasting with interpretable safety metrics and intelligent-intersection decision support.

## Motivation

Intersections are high-risk areas because they involve heterogeneous agents, conflicting paths, traffic-signal phases, occlusions, and rapid behavioral changes. Vulnerable road users are particularly difficult to model because their motion is flexible, context-dependent, and often influenced by social interactions, infrastructure layout, and vehicle behavior.

Autonomous vehicles and connected mobility systems require reliable predictions not only from on-board sensors but also from intelligent road infrastructure. Roadside perception can provide a more global view of the scene and may help overcome occlusions and limited vehicle-centric perception.

## Objectives

1. Develop a modular software framework for intelligent-intersection research.
2. Implement baseline trajectory prediction methods for vulnerable road users.
3. Create interaction-aware trajectory prediction models using graph and transformer architectures.
4. Integrate uncertainty estimation into predicted trajectories.
5. Translate predicted trajectories into road-safety indicators.
6. Evaluate the framework on public datasets and simulated smart-intersection scenarios.
7. Prepare the project for research collaboration, publication, and PhD applications.

## Scientific Questions

- How can infrastructure-based perception improve the prediction of vulnerable road user motion?
- How should interactions between pedestrians, cyclists, vehicles, traffic lights, and road geometry be represented?
- Which models are most effective for multi-agent prediction in urban intersections?
- How can uncertainty-aware prediction be used for risk assessment?
- How can trajectory prediction outputs be transformed into interpretable safety indicators?

## Methodology

### Phase 1: Baseline System

- Implement constant-velocity, LSTM, and simple encoder-decoder baselines.
- Evaluate using Average Displacement Error and Final Displacement Error.
- Establish reproducible experiment configuration.

### Phase 2: Interaction-Aware Prediction

- Model road users as nodes in a dynamic graph.
- Use spatial and temporal relationships as edges.
- Include traffic lights, crosswalks, and lane geometry as contextual information.

### Phase 3: Safety-Aware Prediction

- Estimate minimum predicted distance between agents.
- Compute conflict probability, time-to-collision, post-encroachment time, and severity scores.
- Rank predicted scenarios by risk.

### Phase 4: Intelligent Intersection Digital Twin

- Build simulation scenarios in CARLA and/or SUMO.
- Generate controlled interactions between vehicles and vulnerable road users.
- Test warning and decision-support logic.

## Expected Contributions

- A modular open-source framework for intelligent-intersection AI research.
- A benchmark pipeline for vulnerable road user trajectory prediction.
- A safety-aware prediction layer that connects forecasting with road-safety metrics.
- A digital-twin-ready architecture for simulation-based validation.
- A research portfolio suitable for laboratory applications and doctoral research proposals.

## Potential Publications

1. Baseline and benchmark paper on VRU trajectory prediction at intersections.
2. Graph-based interaction modeling paper.
3. Uncertainty-aware risk assessment paper.
4. Digital twin and smart-intersection decision-support paper.

## Target Venues

- IEEE Intelligent Vehicles Symposium
- IEEE International Conference on Intelligent Transportation Systems
- IEEE Transactions on Intelligent Transportation Systems
- Transportation Research Part C
- ICRA / IROS workshops on autonomous driving and intelligent transportation
- CVPR / ICCV / ECCV workshops on autonomous driving and motion forecasting
