# SafeCrossAI

**SafeCrossAI** is an AI-powered research platform for intelligent urban intersections, focused on vulnerable road user (VRU) safety, trajectory prediction, risk assessment, and cooperative perception for connected and autonomous mobility.

The project investigates how infrastructure-based sensing and machine learning can help smart intersections understand complex multi-agent traffic scenes and anticipate dangerous interactions between pedestrians, cyclists, e-scooter riders, vehicles, and connected/autonomous vehicles.

## Research Vision

Urban intersections are among the most safety-critical environments in road transportation. Vulnerable road users interact with human-driven vehicles, connected vehicles, autonomous vehicles, traffic lights, occlusions, and dynamic urban infrastructure. SafeCrossAI aims to develop an end-to-end research framework that combines perception, behavior understanding, trajectory forecasting, uncertainty estimation, and real-time risk assessment.

The long-term objective is to move beyond single-agent trajectory prediction and toward an intelligent intersection system capable of:

- detecting and tracking heterogeneous traffic participants,
- modeling interactions between vehicles and vulnerable road users,
- predicting multi-modal future trajectories,
- estimating collision risk and uncertainty,
- supporting connected and autonomous driving applications,
- enabling reproducible research through simulation and public datasets.

## Core Research Problem

**How can an intelligent intersection use infrastructure-based perception and AI to predict the motion of vulnerable road users and prevent safety-critical conflicts with connected and autonomous vehicles?**

## Current Stage

SafeCrossAI now includes a first Stage 1 baseline pipeline:

```text
synthetic crossing sample -> constant-velocity prediction -> ADE/FDE evaluation
```

This validates the repository structure before integrating real trajectory datasets.

## Quick Start

```bash
git clone https://github.com/panagiotagrosdouli/SafeCrossAI.git
cd SafeCrossAI
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
pytest
```

Minimal Python usage:

```python
from safecrossai.experiments.baseline_experiment import run_constant_velocity_baseline

result = run_constant_velocity_baseline()
print(result)
```

## Main Research Directions

### 1. Infrastructure-Based Perception

SafeCrossAI considers cameras, LiDAR, radar, roadside units, and V2X communication as components of an intelligent intersection perception stack.

### 2. Scene Understanding

The platform aims to represent the intersection as a dynamic multi-agent scene containing pedestrians, cyclists, micromobility users, vehicles, lane geometry, traffic lights, crosswalks, and semantic context.

### 3. VRU Intention and Behavior Modeling

The project studies whether vulnerable road users are likely to cross, stop, accelerate, change direction, or interact with other agents.

### 4. Multi-Agent Trajectory Prediction

SafeCrossAI will compare and extend models such as LSTMs, graph neural networks, transformer-based predictors, diffusion models, and interaction-aware forecasting methods.

### 5. Risk Assessment and Decision Support

Predicted trajectories will be translated into interpretable safety indicators such as collision probability, time-to-collision, post-encroachment time, conflict severity, and uncertainty-aware risk scores.

### 6. Digital Twin and Simulation

The project will use simulation environments such as CARLA and SUMO to prototype intelligent intersections, generate scenarios, and evaluate safety interventions before real-world deployment.

## Proposed System Architecture

```text
Roadside Sensors / Simulation
          |
          v
Perception Layer
(Object Detection, Tracking, Sensor Fusion)
          |
          v
Scene Representation
(Agents, Map, Crosswalks, Traffic Lights, Interactions)
          |
          v
Behavior and Trajectory Prediction
(Intention, Multi-Agent Forecasting, Uncertainty)
          |
          v
Risk Assessment
(Collision Risk, TTC, PET, Conflict Zones)
          |
          v
Decision Support
(Warnings, V2X Messages, Visualization, Evaluation)
```

## Planned Modules

```text
safecrossai/
├── perception/          # Detection, tracking, sensor fusion
├── prediction/          # Trajectory and intention prediction models
├── risk/                # Safety metrics and risk assessment
├── simulation/          # CARLA/SUMO integration
├── datasets/            # Dataset loaders and preprocessing tools
├── visualization/       # Plots, dashboards, scenario visualization
└── evaluation/          # Metrics, benchmarks, experiment utilities
```

## Candidate Datasets

The platform is designed to support public datasets relevant to autonomous driving, intelligent intersections, and multi-agent trajectory prediction, such as:

- INTERACTION Dataset
- inD Dataset
- rounD Dataset
- highD Dataset
- Argoverse 2 Motion Forecasting
- nuScenes
- Waymo Open Motion Dataset
- V2X and infrastructure-based cooperative perception datasets

## Technology Stack

- Python
- PyTorch
- PyTorch Geometric
- NumPy / pandas
- OpenCV
- ROS 2
- CARLA
- SUMO
- Docker
- FastAPI or Streamlit for demos
- Matplotlib / Plotly for visualization

## Initial Milestones

1. Define the research scope and system architecture.
2. Implement baseline trajectory prediction models.
3. Add dataset preprocessing for intersection-based trajectory datasets.
4. Implement safety metrics for conflict and collision risk.
5. Build a minimal visualization dashboard.
6. Extend the project with graph-based and transformer-based models.
7. Create a simulation-based smart intersection digital twin.
8. Prepare results for a conference or journal submission.

## Example Research Questions

- How can infrastructure-based perception improve VRU trajectory prediction compared with vehicle-only perception?
- Which interaction representations are most effective for predicting pedestrian and cyclist motion at intersections?
- How can uncertainty-aware prediction improve safety-critical decision support?
- Can graph neural networks model complex interactions between VRUs, vehicles, traffic lights, and road geometry?
- How can digital twins support the evaluation of rare but dangerous traffic conflicts?

## Status

This repository is at the initial research-platform stage. The first objective is to establish a clean, reproducible foundation for experiments in VRU trajectory prediction and intelligent intersection safety.

## Citation

If you use this project in academic work, please cite the repository once a formal publication or preprint becomes available.

## License

This project is released under the MIT License unless otherwise specified.
