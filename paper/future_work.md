# Future Work

## Dataset Integration

Implement dataset loaders with clear license and citation notes for public trajectory datasets. The first target should be a dataset with intersection or roundabout interactions.

## Learning-Based Prediction

Add learning-based predictors only after the baseline protocol is stable. Candidate models include linear sequence models, recurrent networks, graph neural networks, and transformer-based predictors.

## Uncertainty

Develop calibrated uncertainty estimates for future trajectories. Calibration should be evaluated explicitly before risk scores are interpreted probabilistically.

## Risk Evaluation

Add labelled interaction or near-miss evaluation when an appropriate dataset is available. Until then, risk visualizations should remain synthetic demonstrations.

## Simulation

Explore CARLA or SUMO integration for controlled scenario generation, but keep simulation claims separate from real-world dataset evaluation.
