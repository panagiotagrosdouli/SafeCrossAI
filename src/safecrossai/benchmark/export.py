"""Export benchmark results to files."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from safecrossai.benchmark.comparison import BenchmarkRow


def export_benchmark_csv(rows: list[BenchmarkRow], path: str | Path) -> None:
    """Export benchmark rows to CSV."""
    if not rows:
        raise ValueError("rows must not be empty")

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["model", "samples", "mean_ade", "mean_fde"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "model": row.model,
                    "samples": row.samples,
                    "mean_ade": row.mean_ade,
                    "mean_fde": row.mean_fde,
                }
            )


def export_benchmark_json(rows: list[BenchmarkRow], path: str | Path) -> None:
    """Export benchmark rows to JSON."""
    if not rows:
        raise ValueError("rows must not be empty")

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = [
        {
            "model": row.model,
            "samples": row.samples,
            "mean_ade": row.mean_ade,
            "mean_fde": row.mean_fde,
        }
        for row in rows
    ]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
