#!/usr/bin/env python
"""Run the deterministic constant-velocity baseline."""

from __future__ import annotations

from safecrossai.experiments.baseline_experiment import run_constant_velocity_baseline


def main() -> None:
    result = run_constant_velocity_baseline()
    print("SafeCrossAI constant-velocity baseline on synthetic toy sample")
    print(f"ADE: {result.ade:.6f}")
    print(f"FDE: {result.fde:.6f}")
    print("Note: this is a synthetic smoke test, not a benchmark result.")


if __name__ == "__main__":
    main()
