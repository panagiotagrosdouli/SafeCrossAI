#!/usr/bin/env python
"""Run deterministic Synthetic Demo benchmark scenarios.

These are software smoke benchmarks only. They are not real-world dataset results.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from safecrossai.simulation import SyntheticIntersectionSimulator


def main() -> None:
    rows = []
    for seed in [7, 13, 21]:
        summary = SyntheticIntersectionSimulator(seed=seed).run("results")
        rows.append({"scenario": "high_risk_conflict", **summary})
    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    Path("results/reports").mkdir(parents=True, exist_ok=True)
    table = pd.DataFrame(rows)
    table.to_csv("results/metrics/benchmark_summary.csv", index=False)
    Path("results/reports/benchmark_report.md").write_text(
        "# Synthetic Demo Benchmark Report\n\n"
        "Generated only from deterministic synthetic smoke scenarios. "
        "No real-world benchmark or state-of-the-art claim is made.\n\n"
        "```json\n" + json.dumps(rows, indent=2) + "\n```\n",
        encoding="utf-8",
    )
    print("Synthetic Demo benchmark report generated.")


if __name__ == "__main__":
    main()
