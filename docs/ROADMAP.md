# Roadmap

SafeCrossAI uses explicit maturity labels to avoid overclaiming.

## Maturity Labels

- **Implemented**: code exists, tests or smoke tests can run, and limitations are documented.
- **Prototype**: scaffold exists, but the feature is not validated or benchmarked.
- **Planned**: research direction is documented, but no implementation should be assumed.

## Phase 0 — Baseline Foundation

Status: **Implemented / in progress**

- Synthetic trajectory samples.
- Constant-velocity baseline.
- ADE/FDE metrics.
- Social agents and interaction graph.
- TTC and closest-approach utilities.
- Baseline risk score.
- Deterministic demo GIF pipeline.

## Phase 1 — Reproducible Research Infrastructure

Status: **Prototype**

- Config-driven experiment runner.
- CI with pytest and Ruff.
- Pre-commit hooks.
- Dockerfile.
- Result schema.
- Figure-generation scripts.

## Phase 2 — Dataset Integration

Status: **Planned**

- Dataset license documentation.
- inD loader.
- rounD loader.
- INTERACTION loader.
- Argoverse-style trajectory loader.
- Common scene representation.

## Phase 3 — Learning-Based Prediction

Status: **Planned**

- Linear model baseline.
- LSTM or GRU baseline.
- Graph-neural predictor.
- Transformer-based predictor.
- Multi-modal trajectory output.

## Phase 4 — Uncertainty and Risk

Status: **Prototype / planned**

- Confidence score baseline.
- Calibration metrics.
- Uncertainty-aware risk score.
- Reliability diagrams.
- Near-miss evaluation.

## Phase 5 — Intelligent Infrastructure

Status: **Planned**

- Infrastructure sensor abstraction.
- Perception/tracking interface.
- V2X message abstraction.
- Digital-twin simulation with CARLA/SUMO.

## Phase 6 — Publication Readiness

Status: **Planned**

- Reproducible benchmark table.
- Ablation study.
- Failure-case analysis.
- Paper figures.
- Workshop paper or preprint.

## Near-Term Priorities

1. Make all baseline scripts runnable from a clean checkout.
2. Add tests for risk scoring and visualization smoke tests.
3. Add a small config-driven experiment runner.
4. Add generated figures and GIF under `assets/`.
5. Implement a first public dataset loader after documenting license constraints.
