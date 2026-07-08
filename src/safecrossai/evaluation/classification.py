"""Classification and calibration metrics for interaction-risk evaluation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BinaryConfusionMatrix:
    """Binary confusion matrix counts."""

    true_positive: int
    false_positive: int
    true_negative: int
    false_negative: int


def _as_bool_array(values: np.ndarray | list[bool] | list[int]) -> np.ndarray:
    return np.asarray(values, dtype=bool)


def binary_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> BinaryConfusionMatrix:
    """Compute binary confusion matrix counts."""
    truth = _as_bool_array(y_true)
    pred = _as_bool_array(y_pred)
    if truth.shape != pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    return BinaryConfusionMatrix(
        true_positive=int(np.logical_and(truth, pred).sum()),
        false_positive=int(np.logical_and(~truth, pred).sum()),
        true_negative=int(np.logical_and(~truth, ~pred).sum()),
        false_negative=int(np.logical_and(truth, ~pred).sum()),
    )


def precision(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute binary precision."""
    cm = binary_confusion_matrix(y_true, y_pred)
    denom = cm.true_positive + cm.false_positive
    return 0.0 if denom == 0 else cm.true_positive / denom


def recall(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute binary recall."""
    cm = binary_confusion_matrix(y_true, y_pred)
    denom = cm.true_positive + cm.false_negative
    return 0.0 if denom == 0 else cm.true_positive / denom


def f1_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute binary F1 score."""
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 0.0 if p + r == 0.0 else 2.0 * p * r / (p + r)


def miss_rate(prediction: np.ndarray, target: np.ndarray, threshold: float) -> float:
    """Compute trajectory miss rate from final displacement threshold."""
    if threshold < 0.0:
        raise ValueError("threshold must be non-negative")
    if prediction.shape != target.shape:
        raise ValueError("prediction and target must have the same shape")
    if prediction.ndim == 2:
        errors = np.array([np.linalg.norm(prediction[-1] - target[-1])])
    elif prediction.ndim == 3:
        errors = np.linalg.norm(prediction[:, -1, :] - target[:, -1, :], axis=1)
    else:
        raise ValueError("trajectories must have shape (T, 2) or (N, T, 2)")
    return float((errors > threshold).mean())


def roc_curve_points(y_true: np.ndarray, scores: np.ndarray, num_thresholds: int = 101) -> tuple[np.ndarray, np.ndarray]:
    """Return false-positive and true-positive rates for thresholds in [0, 1]."""
    truth = _as_bool_array(y_true)
    score_array = np.asarray(scores, dtype=float)
    if truth.shape != score_array.shape:
        raise ValueError("y_true and scores must have the same shape")
    thresholds = np.linspace(0.0, 1.0, num_thresholds)
    fpr_values: list[float] = []
    tpr_values: list[float] = []
    for threshold in thresholds:
        pred = score_array >= threshold
        cm = binary_confusion_matrix(truth, pred)
        fpr_denom = cm.false_positive + cm.true_negative
        tpr_denom = cm.true_positive + cm.false_negative
        fpr_values.append(0.0 if fpr_denom == 0 else cm.false_positive / fpr_denom)
        tpr_values.append(0.0 if tpr_denom == 0 else cm.true_positive / tpr_denom)
    return np.asarray(fpr_values), np.asarray(tpr_values)


def precision_recall_curve_points(
    y_true: np.ndarray,
    scores: np.ndarray,
    num_thresholds: int = 101,
) -> tuple[np.ndarray, np.ndarray]:
    """Return precision and recall values for thresholds in [0, 1]."""
    truth = _as_bool_array(y_true)
    score_array = np.asarray(scores, dtype=float)
    if truth.shape != score_array.shape:
        raise ValueError("y_true and scores must have the same shape")
    thresholds = np.linspace(0.0, 1.0, num_thresholds)
    precisions: list[float] = []
    recalls: list[float] = []
    for threshold in thresholds:
        pred = score_array >= threshold
        precisions.append(precision(truth, pred))
        recalls.append(recall(truth, pred))
    return np.asarray(precisions), np.asarray(recalls)


def expected_calibration_error(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    num_bins: int = 10,
) -> float:
    """Compute expected calibration error for binary risk probabilities."""
    if num_bins < 1:
        raise ValueError("num_bins must be positive")
    truth = _as_bool_array(y_true).astype(float)
    probs = np.asarray(probabilities, dtype=float)
    if truth.shape != probs.shape:
        raise ValueError("y_true and probabilities must have the same shape")
    if np.any((probs < 0.0) | (probs > 1.0)):
        raise ValueError("probabilities must be in [0, 1]")

    edges = np.linspace(0.0, 1.0, num_bins + 1)
    ece = 0.0
    for lower, upper in zip(edges[:-1], edges[1:]):
        mask = (probs >= lower) & (probs < upper if upper < 1.0 else probs <= upper)
        if not np.any(mask):
            continue
        confidence = float(probs[mask].mean())
        accuracy = float(truth[mask].mean())
        ece += float(mask.mean()) * abs(confidence - accuracy)
    return float(ece)
