# Repository Audit and Research-Grade Roadmap

This audit records the repository state inspected during the SafeCrossAI research transformation. It is intentionally conservative: it distinguishes implemented baselines from prototypes and avoids claiming experimental results that have not been produced by committed, reproducible scripts.

## Audit Scope

Inspected components include the public README, packaging metadata, dependency declarations, trajectory-prediction baseline code, evaluation metrics, classification/calibration utilities, social-neighbor abstractions, deterministic risk scoring, research documentation, and recent repository history.

## Strengths

| Severity | Finding | Impact |
|---|---|---|
| Positive | Clear scientific identity around intelligent infrastructure, VRU prediction, interaction analysis, and uncertainty-aware risk estimation. | Strong basis for MSc/PhD portfolio positioning. |
| Positive | README explicitly states that the repository is early-stage and does not claim SOTA performance, deployment, or completed benchmarks. | Reduces scientific overclaiming risk. |
| Positive | `pyproject.toml` declares package metadata, Python version, dependencies, optional dev/demo/vision/graph extras, and Black/Ruff/pytest/mypy configuration. | Supports reproducibility and maintainability. |
| Positive | Constant-velocity and linear deterministic prediction baselines are present. | Provides sanity-check baselines before learned models. |
| Positive | Pairwise TTC/CPA-based risk scoring returns interpretable reports with distance, closest approach, score, level, and confidence. | Provides a transparent baseline for safety-critical interaction analysis. |
| Positive | Precision, recall, F1, miss rate, confusion matrix, ROC, precision-recall, and calibration helpers are implemented. | Establishes evaluation infrastructure beyond ADE/FDE. |

## Issues Ranked by Severity

### Critical

| Issue | Why it matters | Recommended action | Status |
|---|---|---|---|
| No real dataset benchmark results | The project cannot support scientific claims without reproducible public-dataset evaluation. | Add dataset loaders, split definitions, experiment configs, and result-generation scripts before reporting numbers. | Planned |
| Learning-based prediction not implemented | The research question requires interaction-aware and uncertainty-aware forecasting beyond deterministic baselines. | Add model interfaces, train/eval loops, reproducibility metadata, and baseline comparisons. | Prototype / Planned |
| Infrastructure perception missing | The problem statement includes AI-based perception, but current code focuses mainly on trajectories and risk. | Add perception interfaces first; only add models after dataset/licensing clarity. | Prototype |
| Uncertainty estimation incomplete | Risk scoring has a confidence heuristic but not calibrated predictive uncertainty. | Add probabilistic prediction outputs, calibration metrics, reliability diagrams, and uncertainty-aware risk propagation. | Prototype |

### High

| Issue | Why it matters | Recommended action | Status |
|---|---|---|---|
| Documentation may outrun implementation | README and docs describe a complete research platform, but some modules are still scaffolds. | Keep implemented/prototype/planned labels in every public-facing document. | In progress |
| Repository structure uses `src/safecrossai/` rather than top-level `safecrossai/` | The target tree listed `safecrossai/` at root; `src/` layout is still acceptable but should be explicit. | Document that `src/` layout is intentional for packaging hygiene. | In progress |
| No verified local CI run in this environment | The execution environment could not clone GitHub directly, so tests were not run locally here. | Run `python -m pip install -e .[dev,demo]`, `ruff check .`, and `pytest` in GitHub Actions/local checkout. | Open |
| Demo GIF/MP4 claims require generated artifacts | The README lists expected demo outputs, but generated binary assets should be reproducible rather than manually fabricated. | Keep scripts deterministic and commit only small representative assets if desired. | In progress |

### Medium

| Issue | Why it matters | Recommended action | Status |
|---|---|---|---|
| Linear prediction baseline was missing | The roadmap requested a Linear Model, while only constant velocity was initially confirmed. | Implement independent least-squares linear extrapolation and tests. | Implemented |
| Risk thresholds are heuristic | Deterministic risk thresholds are interpretable but not calibrated to empirical near-miss labels. | Treat thresholds as baseline hyperparameters and calibrate only after dataset validation. | Prototype |
| Dataset directory is mostly policy/scaffold | Dataset support needs actual parsers, schema validation, and licensing notes. | Add CSV/common-schema loader first, then public datasets. | Planned |
| Website is likely scaffold-only | A full Next.js/Tailwind/Framer Motion site is large and should not block core science. | Keep as documentation scaffold until research assets stabilize. | Prototype |

### Low

| Issue | Why it matters | Recommended action | Status |
|---|---|---|---|
| README asset placeholders | Placeholders are acceptable early, but final presentation should include generated architecture/pipeline figures. | Generate deterministic diagrams from scripts. | Planned |
| More API examples needed | Users need short examples for each module. | Add notebooks/examples after API stabilizes. | Planned |
| Benchmarks should include timing | Baseline runtime and scalability should be measured. | Add benchmark scripts for neighbor search, prediction, and risk scoring. | Planned |

## Duplicated Logic

No severe duplication was identified in the inspected modules. Geometry, neighbor search, TTC/CPA, prediction, evaluation, and risk scoring appear conceptually separated. Future work should avoid reimplementing distance/TTC logic inside visualization or scripts; those should call the library modules.

## Bad Software Practices to Avoid

- Do not hard-code benchmark numbers into README or papers.
- Do not label synthetic demos as real-world experiments.
- Do not hide incomplete features behind polished marketing language.
- Do not introduce neural models without train/eval scripts, seeds, and documented data splits.
- Do not mix plotting, metrics, and model logic in the same module.

## Scalability Risks

Current neighbor and interaction utilities are suitable for small scenes and deterministic demos. Large-scale public datasets will require batching, vectorization, spatial indexing, caching, and robust experiment configuration.

## Reproducibility Risks

The repository needs committed experiment configs, deterministic random seeds, dataset-version metadata, environment setup, CI artifacts, and clear result provenance before any benchmark table is valid.

## Implementation Roadmap

### Milestone 1: Baseline Integrity

- Keep constant-velocity and linear baselines simple and tested.
- Add tests for ADE/FDE, miss rate, ROC/PR curves, TTC/CPA, and risk reports.
- Ensure `ruff`, `black --check`, and `pytest` pass in CI.

### Milestone 2: Data and Evaluation

- Define a canonical scene schema.
- Add a documented CSV loader and synthetic scenario loader.
- Add dataset cards and license notes for all external datasets.
- Add reproducible evaluation scripts that write machine-readable result files.

### Milestone 3: Interaction-Aware Prediction

- Add model interface for predictors.
- Add graph-based feature extraction.
- Implement a simple learned baseline only after data loading and evaluation are stable.

### Milestone 4: Uncertainty and Risk

- Extend predictors to output multiple futures or covariance estimates.
- Add calibration curves and expected calibration error for risk outputs.
- Validate risk scoring against near-miss/conflict labels when available.

### Milestone 5: Publication Assets

- Generate architecture, pipeline, interaction graph, risk overlay, ROC, PR, calibration, and confusion-matrix figures from scripts.
- Add paper skeleton with reproducibility checklist.
- Prepare a workshop paper only after real, reproducible results exist.

## Change Log for This Audit Pass

- Added a least-squares linear trajectory prediction baseline.
- Added unit tests for the linear baseline.
- Added an explicit implementation/prototype policy document.
- Updated this repository audit and roadmap.
