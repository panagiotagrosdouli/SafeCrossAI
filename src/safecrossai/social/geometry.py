"""Basic geometry utilities for social interaction modeling."""

from __future__ import annotations

import math

import numpy as np


def distance(a: np.ndarray, b: np.ndarray) -> float:
    """Euclidean distance between two 2D points."""
    return float(np.linalg.norm(np.asarray(a, dtype=float) - np.asarray(b, dtype=float)))


def relative_position(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Return the vector from point a to point b."""
    return np.asarray(b, dtype=float) - np.asarray(a, dtype=float)


def relative_velocity(v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
    """Return the relative velocity vector."""
    return np.asarray(v2, dtype=float) - np.asarray(v1, dtype=float)


def heading(vector: np.ndarray) -> float:
    """Return heading angle in radians."""
    x, y = np.asarray(vector, dtype=float)
    return math.atan2(y, x)


def bearing(a: np.ndarray, b: np.ndarray) -> float:
    """Return bearing angle from point a to point b."""
    return heading(relative_position(a, b))
