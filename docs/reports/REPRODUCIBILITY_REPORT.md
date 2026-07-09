# Reproducibility Report

## Position

SafeCrossAI should report only results produced by reproducible scripts. Synthetic scenarios are useful for development and visualization, but they are not substitutes for public-dataset evaluation or real-world deployment studies.

## Required Experiment Metadata

Every result should record:

- dataset or synthetic scenario identifier;
- train/validation/test split when applicable;
- prediction horizon and observation horizon;
- random seed;
- model or baseline name;
- metric definitions;
- command-line invocation;
- generated output path;
- execution timestamp;
- status: `Implemented`, `Prototype`, `Pending`, or `Failed`.

## Benchmark Integrity

If a public dataset loader, neural model, or comparison baseline is not implemented, benchmark tables must mark the item as `Pending`. Numeric results must not be invented or inferred from unrelated sources.

## Current Status

- Synthetic demo generation: implemented.
- Deterministic trajectory baselines: implemented.
- Risk utilities and interaction graph scaffolds: implemented.
- Docker support: strengthened in this branch.
- CI smoke tests: strengthened in this branch.
- Public dataset benchmarks: pending.
- Neural trajectory prediction benchmarks: pending.
- Real-world infrastructure deployment: pending.
