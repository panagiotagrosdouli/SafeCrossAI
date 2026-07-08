from __future__ import annotations

import numpy as np

from safecrossai.evaluation import (
    binary_confusion_matrix,
    expected_calibration_error,
    f1_score,
    precision,
    recall,
)


def test_binary_confusion_matrix_counts() -> None:
    y_true = np.array([1, 1, 0, 0], dtype=bool)
    y_pred = np.array([1, 0, 1, 0], dtype=bool)
    cm = binary_confusion_matrix(y_true, y_pred)
    assert cm.true_positive == 1
    assert cm.false_positive == 1
    assert cm.true_negative == 1
    assert cm.false_negative == 1


def test_precision_recall_f1() -> None:
    y_true = np.array([1, 1, 0, 0], dtype=bool)
    y_pred = np.array([1, 0, 1, 0], dtype=bool)
    assert precision(y_true, y_pred) == 0.5
    assert recall(y_true, y_pred) == 0.5
    assert f1_score(y_true, y_pred) == 0.5


def test_expected_calibration_error_range() -> None:
    y_true = np.array([1, 0, 1, 0], dtype=bool)
    probs = np.array([0.8, 0.2, 0.6, 0.1])
    ece = expected_calibration_error(y_true, probs, num_bins=2)
    assert 0.0 <= ece <= 1.0
