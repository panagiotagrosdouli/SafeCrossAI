#!/usr/bin/env python
"""Generate reproducible scientific figures for SafeCrossAI.

The generated figures use deterministic synthetic examples only. They are meant
for explaining the software pipeline and algorithms, not for reporting benchmark
performance on real datasets.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from safecrossai.datasets.demo import make_intersection_demo_scenario
from safecrossai.evaluation.classification import (
    binary_confusion_matrix,
    precision_recall_curve_points,
    roc_curve_points,
)
from safecrossai.prediction.baseline import constant_velocity_predict
from safecrossai.prediction.linear import linear_regression_predict
from safecrossai.risk import RiskConfig, assess_pairwise_risk
from safecrossai.visualization import render_scene


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("assets"))
    parser.add_argument("--num-steps", type=int, default=30)
    parser.add_argument("--dt", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    """Generate all deterministic explanatory figures."""
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    scenario = make_intersection_demo_scenario(num_steps=args.num_steps, dt=args.dt)
    _save_architecture_diagram(args.output_dir / "architecture_diagram.png")
    _save_pipeline_diagram(args.output_dir / "pipeline_diagram.png")
    _save_dependency_graph(args.output_dir / "module_dependency_graph.png")
    _save_prediction_figure(args.output_dir / "trajectory_prediction.png")
    _save_interaction_graph_figure(scenario, args.output_dir / "interaction_graph.png")
    _save_risk_overlay_figure(scenario, args.output_dir / "risk_overlay.png")
    _save_evaluation_figures(args.output_dir)
    print(f"Saved figures to {args.output_dir}")


def _save_box_diagram(labels: list[str], path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(9.0, 2.8), dpi=160)
    ax.set_title(title)
    ax.axis("off")
    xs = np.linspace(0.08, 0.92, len(labels))
    for index, (x_coord, label) in enumerate(zip(xs, labels, strict=True)):
        ax.text(
            x_coord,
            0.55,
            label,
            ha="center",
            va="center",
            bbox={"boxstyle": "round,pad=0.35", "linewidth": 1.2, "facecolor": "white"},
            transform=ax.transAxes,
        )
        if index < len(labels) - 1:
            ax.annotate(
                "",
                xy=(xs[index + 1] - 0.07, 0.55),
                xytext=(x_coord + 0.07, 0.55),
                arrowprops={"arrowstyle": "->", "linewidth": 1.2},
                xycoords=ax.transAxes,
            )
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _save_architecture_diagram(path: Path) -> None:
    labels = ["Sensors", "Perception\nPrototype", "Prediction", "Interaction", "Risk", "Evaluation"]
    _save_box_diagram(labels, path, "SafeCrossAI research architecture")


def _save_pipeline_diagram(path: Path) -> None:
    labels = ["Scene", "CV / Linear", "TTC / CPA", "Risk report", "Figures"]
    _save_box_diagram(labels, path, "Deterministic baseline pipeline")


def _save_dependency_graph(path: Path) -> None:
    labels = ["datasets", "prediction", "social", "risk", "evaluation", "visualization"]
    _save_box_diagram(labels, path, "Module dependency graph")


def _save_prediction_figure(path: Path) -> None:
    history = np.array([[0.0, 0.0], [1.0, 0.4], [2.0, 0.9], [3.0, 1.5]])
    horizon = 5
    cv_prediction = constant_velocity_predict(history, horizon=horizon)
    linear_prediction = linear_regression_predict(history, horizon=horizon)

    fig, ax = plt.subplots(figsize=(5.5, 4.0), dpi=160)
    ax.plot(history[:, 0], history[:, 1], marker="o", label="observed history")
    ax.plot(cv_prediction[:, 0], cv_prediction[:, 1], marker="x", label="constant velocity")
    ax.plot(linear_prediction[:, 0], linear_prediction[:, 1], marker="s", label="linear baseline")
    ax.set_title("Trajectory prediction baselines")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.grid(True, linewidth=0.4, alpha=0.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _save_interaction_graph_figure(scenario, path: Path) -> None:
    scene = scenario.scenes[len(scenario.scenes) // 2]
    fig, ax = plt.subplots(figsize=(7.0, 4.5), dpi=160)
    render_scene(scene, ax=ax)
    ax.set_title("Interaction graph example")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _save_risk_overlay_figure(scenario, path: Path) -> None:
    scene = scenario.scenes[len(scenario.scenes) // 2]
    config = RiskConfig()
    fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=160)
    ax.set_title("Pairwise baseline risk scores")
    ax.set_xlabel("Agent pair")
    ax.set_ylabel("Risk score")
    labels: list[str] = []
    scores: list[float] = []
    for source in scene.agents:
        for target in scene.agents:
            if source.agent_id == target.agent_id:
                continue
            report = assess_pairwise_risk(source, target, config=config)
            labels.append(f"{source.agent_id}\n→ {target.agent_id}")
            scores.append(report.score)
    ax.bar(np.arange(len(scores)), scores)
    ax.set_xticks(np.arange(len(labels)), labels, rotation=45, ha="right")
    ax.set_ylim(0.0, 1.0)
    ax.grid(True, axis="y", linewidth=0.4, alpha=0.35)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _save_evaluation_figures(output_dir: Path) -> None:
    y_true = np.array([0, 0, 1, 1, 0, 1, 0, 1], dtype=bool)
    scores = np.array([0.05, 0.20, 0.62, 0.82, 0.30, 0.74, 0.41, 0.91])
    predictions = scores >= 0.5

    _save_confusion_matrix(y_true, predictions, output_dir / "confusion_matrix.png")
    _save_roc_curve(y_true, scores, output_dir / "roc_curve.png")
    _save_precision_recall_curve(y_true, scores, output_dir / "precision_recall_curve.png")
    _save_calibration_curve(y_true, scores, output_dir / "calibration_curve.png")


def _save_confusion_matrix(y_true: np.ndarray, predictions: np.ndarray, path: Path) -> None:
    matrix = binary_confusion_matrix(y_true, predictions)
    values = np.array(
        [
            [matrix.true_negative, matrix.false_positive],
            [matrix.false_negative, matrix.true_positive],
        ]
    )
    fig, ax = plt.subplots(figsize=(4.0, 3.6), dpi=160)
    image = ax.imshow(values)
    ax.set_xticks([0, 1], ["Pred 0", "Pred 1"])
    ax.set_yticks([0, 1], ["True 0", "True 1"])
    ax.set_title("Synthetic confusion matrix")
    for row in range(2):
        for col in range(2):
            ax.text(col, row, str(values[row, col]), ha="center", va="center")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _save_roc_curve(y_true: np.ndarray, scores: np.ndarray, path: Path) -> None:
    false_positive_rate, true_positive_rate = roc_curve_points(y_true, scores)
    fig, ax = plt.subplots(figsize=(4.5, 4.0), dpi=160)
    ax.plot(false_positive_rate, true_positive_rate)
    ax.plot([0, 1], [0, 1], linestyle="--", linewidth=1.0)
    ax.set_title("Synthetic ROC curve")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.grid(True, linewidth=0.4, alpha=0.35)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _save_precision_recall_curve(y_true: np.ndarray, scores: np.ndarray, path: Path) -> None:
    precision, recall = precision_recall_curve_points(y_true, scores)
    fig, ax = plt.subplots(figsize=(4.5, 4.0), dpi=160)
    ax.plot(recall, precision)
    ax.set_title("Synthetic precision-recall curve")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.grid(True, linewidth=0.4, alpha=0.35)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _save_calibration_curve(y_true: np.ndarray, scores: np.ndarray, path: Path) -> None:
    bins = np.linspace(0.0, 1.0, 6)
    centers: list[float] = []
    empirical: list[float] = []
    for lower, upper in zip(bins[:-1], bins[1:], strict=True):
        mask = (scores >= lower) & (scores < upper if upper < 1.0 else scores <= upper)
        if not np.any(mask):
            continue
        centers.append(float(scores[mask].mean()))
        empirical.append(float(y_true[mask].mean()))

    fig, ax = plt.subplots(figsize=(4.5, 4.0), dpi=160)
    ax.plot([0, 1], [0, 1], linestyle="--", linewidth=1.0)
    ax.plot(centers, empirical, marker="o")
    ax.set_title("Synthetic calibration plot")
    ax.set_xlabel("Mean predicted risk")
    ax.set_ylabel("Empirical frequency")
    ax.grid(True, linewidth=0.4, alpha=0.35)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


if __name__ == "__main__":
    main()
