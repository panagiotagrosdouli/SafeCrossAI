"""Benchmark report formatting utilities."""

from __future__ import annotations

from safecrossai.benchmark.comparison import BenchmarkRow


def benchmark_rows_to_markdown(rows: list[BenchmarkRow]) -> str:
    """Format benchmark rows as a Markdown table."""
    if not rows:
        raise ValueError("rows must not be empty")

    lines = [
        "| Model | Samples | Mean ADE | Mean FDE |",
        "|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(f"| {row.model} | {row.samples} | {row.mean_ade:.6f} | {row.mean_fde:.6f} |")

    return "\n".join(lines)
