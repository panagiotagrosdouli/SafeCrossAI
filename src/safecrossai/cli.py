"""Command line interface for SafeCrossAI."""

from __future__ import annotations

import argparse
from pathlib import Path

from safecrossai.benchmark.comparison import (
    compare_constant_velocity_and_lstm,
    compare_with_grouped_train_test_split,
    compare_with_train_test_split,
)
from safecrossai.benchmark.export import (
    export_benchmark_csv,
    export_benchmark_json,
    export_benchmark_markdown,
)
from safecrossai.benchmark.metadata import BenchmarkMetadata
from safecrossai.benchmark.report import benchmark_rows_to_markdown
from safecrossai.datasets.ind.samples import build_ind_samples
from safecrossai.datasets.ind.scenes import build_ind_scenes
from safecrossai.datasets.toy import make_linear_crossing_sample
from safecrossai.experiments.baseline_experiment import run_constant_velocity_baseline
from safecrossai.experiments.csv_baseline_experiment import run_csv_constant_velocity_baseline
from safecrossai.social import build_scene_sequences


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
    benchmark_parser.add_argument("--output-csv", type=Path, default=None)
    benchmark_parser.add_argument("--output-json", type=Path, default=None)
    benchmark_parser.add_argument("--output-md", type=Path, default=None)

    ind_parser = subparsers.add_parser(
        "ind-benchmark",
        help="Compare constant velocity and LSTM on an inD-style tracks CSV file.",
    )
    ind_parser.add_argument("path", type=Path, help="Path to inD-style tracks CSV file.")
    ind_parser.add_argument("--observation-steps", type=int, default=8)
    ind_parser.add_argument("--prediction-steps", type=int, default=12)
    ind_parser.add_argument("--lstm-epochs", type=int, default=1)
    ind_parser.add_argument("--hidden-dim", type=int, default=8)
    ind_parser.add_argument("--max-samples", type=int, default=32)
    ind_parser.add_argument("--train-test", action="store_true")
    ind_parser.add_argument("--grouped-split", action="store_true")
    ind_parser.add_argument("--test-fraction", type=float, default=0.2)
    ind_parser.add_argument("--seed", type=int, default=42)
    ind_parser.add_argument("--output-csv", type=Path, default=None)
    ind_parser.add_argument("--output-json", type=Path, default=None)
    ind_parser.add_argument("--output-md", type=Path, default=None)
    ind_parser.add_argument(
        "--classes",
        nargs="*",
        default=None,
        help="Optional inD classes to keep, for example: pedestrian bicycle.",
    )

    scene_parser = subparsers.add_parser(
        "ind-scene-summary",
        help="Summarize frame-level scenes from an inD-style tracks CSV file.",
    )
    scene_parser.add_argument("path", type=Path, help="Path to inD-style tracks CSV file.")
    scene_parser.add_argument("--radius", type=float, default=5.0)
    scene_parser.add_argument("--sequence-length", type=int, default=None)
    scene_parser.add_argument("--stride", type=int, default=1)
    scene_parser.add_argument(
        "--classes",
        nargs="*",
        default=None,
        help="Optional inD classes to keep, for example: pedestrian bicycle.",
    )

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
        metadata = BenchmarkMetadata(
            dataset="toy",
            protocol="same_samples",
            observation_steps=args.observation_steps,
            prediction_steps=args.prediction_steps,
            lstm_epochs=args.lstm_epochs,
            hidden_dim=args.hidden_dim,
            samples=1,
        )
        _export_rows(rows, args.output_csv, args.output_json, args.output_md, metadata)
        print(benchmark_rows_to_markdown(rows))
        return

    if args.command == "ind-benchmark":
        classes = set(args.classes) if args.classes else None
        samples = build_ind_samples(
            args.path,
            observation_steps=args.observation_steps,
            prediction_steps=args.prediction_steps,
            classes=classes,
        )
        if args.max_samples > 0:
            samples = samples[: args.max_samples]
        if args.grouped_split:
            protocol = "grouped_train_test"
            rows = compare_with_grouped_train_test_split(
                samples,
                test_fraction=args.test_fraction,
                seed=args.seed,
                lstm_epochs=args.lstm_epochs,
                hidden_dim=args.hidden_dim,
            )
        elif args.train_test:
            protocol = "train_test"
            rows = compare_with_train_test_split(
                samples,
                test_fraction=args.test_fraction,
                seed=args.seed,
                lstm_epochs=args.lstm_epochs,
                hidden_dim=args.hidden_dim,
            )
        else:
            protocol = "same_samples"
            rows = compare_constant_velocity_and_lstm(
                samples,
                lstm_epochs=args.lstm_epochs,
                hidden_dim=args.hidden_dim,
            )
        metadata = BenchmarkMetadata(
            dataset="inD",
            protocol=protocol,
            observation_steps=args.observation_steps,
            prediction_steps=args.prediction_steps,
            lstm_epochs=args.lstm_epochs,
            hidden_dim=args.hidden_dim,
            samples=len(samples),
            classes=sorted(classes) if classes is not None else None,
            test_fraction=args.test_fraction if (args.train_test or args.grouped_split) else None,
            seed=args.seed if (args.train_test or args.grouped_split) else None,
        )
        _export_rows(rows, args.output_csv, args.output_json, args.output_md, metadata)
        print(benchmark_rows_to_markdown(rows))
        return

    if args.command == "ind-scene-summary":
        classes = set(args.classes) if args.classes else None
        scenes = build_ind_scenes(args.path, classes=classes)
        edge_counts = [len(scene.build_interaction_graph(radius=args.radius).edges) for scene in scenes]
        agent_counts = [len(scene.agents) for scene in scenes]
        print(f"scenes: {len(scenes)}")
        print(f"agents: {sum(agent_counts)}")
        print(f"mean_agents_per_scene: {_mean(agent_counts):.2f}")
        print(f"interaction_edges: {sum(edge_counts)}")
        print(f"mean_edges_per_scene: {_mean(edge_counts):.2f}")
        if args.sequence_length is not None:
            sequences = build_scene_sequences(
                scenes,
                sequence_length=args.sequence_length,
                stride=args.stride,
            )
            print(f"scene_sequences: {len(sequences)}")
            print(f"sequence_length: {args.sequence_length}")
            print(f"sequence_stride: {args.stride}")
        return

    parser.error(f"unknown command: {args.command}")


def _export_rows(
    rows,
    output_csv: Path | None,
    output_json: Path | None,
    output_md: Path | None,
    metadata: BenchmarkMetadata | None = None,
) -> None:
    if output_csv is not None:
        export_benchmark_csv(rows, output_csv)
    if output_json is not None:
        export_benchmark_json(rows, output_json, metadata=metadata)
    if output_md is not None:
        export_benchmark_markdown(rows, output_md, metadata=metadata)


def _mean(values: list[int]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


if __name__ == "__main__":
    main()
