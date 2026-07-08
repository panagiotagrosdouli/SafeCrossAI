# API Reference

This is a high-level reference for the current public API. It is not a substitute for generated documentation.

## Prediction

### `safecrossai.prediction.baseline.constant_velocity_predict(history, horizon)`

Predicts future 2D positions by extrapolating the last observed displacement.

- Input: `history` with shape `(T, 2)`.
- Output: prediction with shape `(horizon, 2)`.
- Status: **Implemented baseline**.

## Datasets

### `safecrossai.datasets.toy.make_linear_crossing_sample(...)`

Creates a deterministic synthetic trajectory for smoke tests.

### `safecrossai.datasets.demo.make_intersection_demo_scenario(...)`

Creates a deterministic multi-agent synthetic intersection scenario for visualization and demo generation.

## Social Interaction

### `SocialAgent`

Lightweight representation of one road user with id, position, optional velocity, and agent type.

### `find_neighbors(target, agents, radius)`

Finds agents within a radius of the target.

### `k_nearest_neighbors(target, agents, k)`

Returns the k nearest agents.

### `closest_point_of_approach(...)`

Computes the future time and distance of closest approach under constant-velocity assumptions.

### `time_to_collision(...)`

Analytic time-to-interaction for circular agents under constant-velocity assumptions. Returns `None` when no interaction occurs under the model.

### `build_radius_interaction_graph(agents, radius)`

Builds a directed graph between agents within a radius.

## Risk

### `RiskConfig`

Configuration for deterministic baseline risk scoring.

### `assess_pairwise_risk(source, target, config)`

Returns an interpretable pairwise risk report containing score, level, distance, time-to-interaction, closest-approach information, confidence, and explanation.

Risk scores are not calibrated probabilities.

## Evaluation

### Trajectory metrics

- `average_displacement_error`
- `final_displacement_error`
- `miss_rate`

### Binary risk metrics

- `binary_confusion_matrix`
- `precision`
- `recall`
- `f1_score`
- `roc_curve_points`
- `precision_recall_curve_points`
- `expected_calibration_error`

## Visualization

### `render_scene(scene, ax, risk_radius=8.0)`

Renders one scene with agents, velocity arrows, interaction edges, and risk-weighted overlays.

### `render_scenario_frame(scene, output_path)`

Exports one scene as a PNG frame.

### `save_scenario_gif(frame_paths, output_path, duration_ms=120)`

Assembles PNG frames into a GIF.
