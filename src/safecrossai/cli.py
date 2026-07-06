"""Command line interface for SafeCrossAI."""

from __future__ import annotations

import argparse
from pathlib import Path

from safecrossai.benchmark.comparison import compare_constant_velocity_and_lstm
from safecrossai.benchmark.report import benchmark_rows_to_markdown
from safecrossai.datasets.toy import make_linear_crossing_sample
from safecrossai.experiments.baseline_experiment import run_constant_velocity_baseline
from safecrossai.experiments.csv_baseline_experiment import run_csv_constant_velocity_baseline


def build_parser() -> argparse.ArgumentParser:
    """Build the SafeCrossAI command line parser."""
    parser = argparse.ArgumentParser(
        prog="safecrossai",
        description="Run SafeCrossAI baseline trajectory prediction experiments.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "toy-baseline",
        help="Run the constant-velocity baseline on a synthetic crossing trajectory.",
    )

    csv_parser = subparsers.add_parser(
        "csv-baseline",
        help="Run the constant-velocity baseline on a trajectory CSV file.",
    )
    csv_parser.add_argument("path", type=Path, help="Path to trajectory CSV file.")
    csv_parser.add_argument("--observation-steps", type=int, default=8)
    csv_parser.add_argument("--prediction-steps", type=int, default=12)

    benchmark_parser = subparsers.add_parser(
        "toy-benchmark",
        help="Compare constant velocity and LSTM on a synthetic trajectory.",
    )
    benchmark_parser.add_argument("--observation-steps", type=int, default=8)
    benchmark_parser.add_argument("--prediction-steps", type=int, default=12)
    benchmark_parser.add_argument("--lstm-epochs", type=int, default=1)
    benchmark_parser.add_argument("--hidden-dim", type=int, default=8)

    return parser


def main() -> None:
    """Run the SafeCrossAI CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "toy-baseline":
        result = run_constant_velocity_baseline()
        print("samples: 1")
        print(f"mean_ade: {result.ade:.6f}")
        print(f"mean_fde: {result.fde:.6f}")
        return

    if args.command == "csv-baseline":
        result = run_csv_constant_velocity_baseline(
            args.path,
            observation_steps=args.observation_steps,
            prediction_steps=args.prediction_steps,
        )
        print(f"samples: {result.samples}")
        print(f"mean_ade: {result.mean_ade:.6f}")
        print(f"mean_fde: {result.mean_fde:.6f}")
        return

    if args.command == "toy-benchmark":
        sample = make_linear_crossing_sample(
            observation_steps=args.observation_steps,
            prediction_steps=args.prediction_steps,
        )
        rows = compare_constant_velocity_and_lstm(
            [sample],
            lstm_epochs=args.lstm_epochs,
            hidden_dim=args.hidden_dim,
        )
        print(benchmark_rows_to_markdown(rows))
        return

    parser.error(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()
