# Stage 1 Baseline Pipeline

This stage turns SafeCrossAI into a minimal reproducible research pipeline for vulnerable road user trajectory prediction.

## Current Pipeline

1. Generate a synthetic crossing trajectory.
2. Split the trajectory into observed and future positions.
3. Predict the future positions with a constant-velocity baseline.
4. Evaluate the prediction with ADE and FDE.

## Why This Matters

The synthetic dataset is not the final scientific contribution. It is a controlled first step that validates the architecture before integrating real datasets.

Once the pipeline works, the same structure can be reused for datasets such as INTERACTION, inD, rounD, Argoverse 2, nuScenes, or infrastructure-based V2X datasets.

## Next Technical Steps

- Add a command-line entry point for running experiments.
- Add CSV loading for simple trajectory files.
- Add a first real public dataset adapter.
- Add LSTM and transformer baselines.
- Add visualization of observed, predicted, and ground-truth trajectories.

## Current Metrics

- Average Displacement Error
- Final Displacement Error

## Next Metrics

- Minimum predicted distance
- Time-to-collision
- Post-encroachment time
- Conflict probability
- Uncertainty-aware risk score
