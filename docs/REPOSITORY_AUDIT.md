# SafeCrossAI Repository Audit

This audit records the state of the repository before the research-grade transformation work. It is intentionally conservative: it does not claim that unavailable or uninspected files are complete.

## Audit Scope

The audit inspected the accessible repository metadata and the following files:

- `README.md`
- `pyproject.toml`
- `src/safecrossai/__init__.py`
- `src/safecrossai/datasets/toy.py`
- `src/safecrossai/prediction/baseline.py`
- `src/safecrossai/evaluation/metrics.py`
- `src/safecrossai/experiments/baseline_experiment.py`
- `src/safecrossai/social/__init__.py`
- `src/safecrossai/social/geometry.py`
- `src/safecrossai/social/neighbors.py`
- `src/safecrossai/social/graph.py`
- `src/safecrossai/social/ttc.py`
- `src/safecrossai/social/scene.py`
- `src/safecrossai/social/sequences.py`
- `src/safecrossai/social/temporal_features.py`

Limitations: the connector-based search did not provide a full directory tree. Therefore, this audit is based on files that were directly retrievable and search-visible.

## Strengths

1. **Clear research theme already present** — the README frames the project around intelligent intersections, vulnerable road-user safety, trajectory prediction, and risk assessment.
2. **Baseline prediction exists** — `constant_velocity_predict` provides a deterministic baseline suitable for smoke tests and early evaluation.
3. **Toy dataset exists** — `make_linear_crossing_sample` supports reproducible synthetic experiments.
4. **Basic ADE/FDE metrics exist** — foundational trajectory-prediction metrics are implemented.
5. **Social-interaction foundation exists** — agents, neighbor search, distance/bearing/relative velocity, TTC, closest point of approach, scene representation, sequence windows, and interaction graphs are present.
6. **Packaging exists** — `pyproject.toml` defines project metadata and dependencies.

## Critical Issues

| Severity | Issue | Evidence | Impact | Recommended Action |
|---|---|---|---|---|
| Critical | No complete risk module visible | README promises risk assessment, but inspected code focuses on social/TTC utilities | The main safety contribution is underdeveloped | Add `safecrossai.risk` with risk scoring, conflict reports, TTC risk, confidence, and uncertainty placeholders |
| Critical | No reproducible demo GIF pipeline visible | README mentions research platform but not generated demo assets | Weak project communication for external reviewers | Add deterministic scenario + `scripts/make_demo_gif.py` |
| Critical | No full evaluation protocol visible | ADE/FDE only | Insufficient for publication-style reporting | Add miss rate, classification metrics, curves, calibration, and `docs/EVALUATION_PROTOCOL.md` |
| Critical | README over-broad relative to current implementation | It mentions many future capabilities such as perception, digital twins, and neural models | Risk of overclaiming | Rewrite README with Implemented / Prototype / Planned taxonomy |

## Major Issues

| Severity | Issue | Impact | Recommended Action |
|---|---|---|---|
| High | Public dataset support is only aspirational | Cannot claim dataset results | Add `docs/DATASETS.md` and loader scaffold marked Planned |
| High | Learning-based prediction is not implemented | Neural forecasting claims must remain future work | Add placeholder interfaces only if clearly labelled Prototype |
| High | No visible visualization package | Results are hard to communicate | Add trajectory, interaction, and risk visualization utilities |
| High | No visible CI workflow | Quality cannot be checked automatically | Add GitHub Actions for tests/ruff |
| High | No documented roadmap with milestones | Reviewers cannot assess maturity | Add staged roadmap with honest maturity labels |

## Moderate Issues

| Severity | Issue | Impact | Recommended Action |
|---|---|---|---|
| Medium | `torch` is a core dependency although no inspected neural model uses it | Heavy install for baseline users | Keep optional or document why it is included |
| Medium | Graph module builds directed edges for all pairs within radius | May double-count interactions for undirected analysis | Document directed semantics and provide aggregation later |
| Medium | Risk interpretation is not yet separated from geometric features | Hard to evaluate safety claims | Separate geometry/TTC from risk scoring |
| Medium | No API reference | Hard for external users | Add `docs/API_REFERENCE.md` |
| Medium | No figure-generation scripts | Hard to make paper-quality assets | Add scripts for demo figures |

## Minor Issues

| Severity | Issue | Recommendation |
|---|---|---|
| Low | Some docstrings are concise but not full Google style | Expand docstrings for public APIs |
| Low | No visible `requirements.txt` inspected | Add or align with `pyproject.toml` |
| Low | No visible `CITATION.cff` inspected | Add citation metadata |

## Scientific Weaknesses

- No real benchmark dataset results.
- No uncertainty calibration experiment yet.
- No neural model comparison yet.
- No perception/tracking model implementation yet.
- No conflict-detection labels or evaluation dataset yet.
- No statistically meaningful multi-seed experiment results yet.

## Reproducibility Weaknesses

- No visible config-driven experiment runner beyond the simple baseline function.
- No documented splits, seeds, horizons, or reporting protocol.
- No generated result tables.
- No experiment registry.

## Maintainability Weaknesses

- Existing modules are a good start, but risk, visualization, evaluation, perception, and simulation should be separated into independent packages.
- The README should not be the only source of research positioning.
- CI, type checking, formatting, and documentation checks should be automated.

## Implementation Roadmap

### Phase 1 — Research identity
- Rewrite README with clear Implemented / Prototype / Planned taxonomy.
- Add research overview, system architecture, pipeline, datasets, evaluation, roadmap, API, and visualization documentation.

### Phase 2 — Scientific modules
- Add risk scoring module.
- Extend evaluation metrics.
- Add visualization module.
- Add reproducible synthetic demo scenario.

### Phase 3 — Demo assets
- Add `scripts/make_demo_gif.py`.
- Generate GIF/MP4 from deterministic synthetic scenario.
- Add architecture and pipeline placeholders until generated assets are produced.

### Phase 4 — Engineering quality
- Add CI workflow, pre-commit, Ruff/Black/Mypy configuration, Dockerfile, and tests.

### Phase 5 — Research maturity
- Add public dataset loaders only after dataset format and license notes are documented.
- Add neural predictors only after baseline protocol is stable.
- Add benchmark tables only from reproducible scripts.
