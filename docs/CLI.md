# Command Line Interface

SafeCrossAI provides a small CLI for running baseline trajectory prediction experiments.

## Installation

```bash
python -m pip install -e .[dev]
```

## Toy Baseline

Run the constant-velocity baseline on the built-in synthetic crossing trajectory:

```bash
safecrossai toy-baseline
```

Expected output:

```text
samples: 1
mean_ade: 0.000000
mean_fde: 0.000000
```

## CSV Baseline

Run the constant-velocity baseline on a CSV trajectory file:

```bash
safecrossai csv-baseline examples/sample_trajectories.csv --observation-steps 3 --prediction-steps 2
```

The CSV file must follow the common SafeCrossAI format described in `docs/DATASETS.md`.

## Why This Matters

The CLI makes experiments easier to reproduce and easier to demonstrate to supervisors, research labs, and collaborators.
