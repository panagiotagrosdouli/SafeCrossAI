"""Uncertainty-aware risk interfaces.

This module provides a lightweight scaffold for uncertainty-aware risk analysis.
It does not implement calibrated probabilistic forecasting yet. The current
implementation supports deterministic covariance containers and simple risk
inflation based on positional uncertainty so future neural or Bayesian models
can plug into a stable interface.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PositionalUncertainty:
    """Gaussian positional uncertainty for one 2D agent state.

    Args:
        covariance: 2x2 positive semi-definite covariance matrix in square metres.

    Prototype:
        This class is a data interface. It does not claim that any model in this
        repository currently produces calibrated covariance estimates.
    """

    covariance: np.ndarray

    def __post_init__(self) -> None:
        covariance = np.asarray(self.covariance, dtype=float)
        if covariance.shape != (2, 2):
            raise ValueError("covariance must have shape (2, 2)")
        if not np.allclose(covariance, covariance.T):
            raise ValueError("covariance must be symmetric")
        eigenvalues = np.linalg.eigvalsh(covariance)
        if np.any(eigenvalues < -1e-9):
            raise ValueError("covariance must be positive semi-definite")
        object.__setattr__(self, "covariance", covariance)

    @property
    def radial_std_m(self) -> float:
        """Return an isotropic radial standard-deviation summary in metres."""
        return float(np.sqrt(np.trace(self.covariance)))


def uncertainty_inflated_distance(
    distance_m: float,
    source_uncertainty: PositionalUncertainty | None,
    target_uncertainty: PositionalUncertainty | None,
    sigma_scale: float = 1.0,
) -> float:
    """Return a conservative distance reduced by uncertainty radius.

    Args:
        distance_m: Deterministic Euclidean distance between agents.
        source_uncertainty: Optional uncertainty for the source agent.
        target_uncertainty: Optional uncertainty for the target agent.
        sigma_scale: Number of radial standard deviations used for inflation.

    Returns:
        Non-negative conservative distance estimate.
    """
    if distance_m < 0.0:
        raise ValueError("distance_m must be non-negative")
    if sigma_scale < 0.0:
        raise ValueError("sigma_scale must be non-negative")

    source_radius = 0.0 if source_uncertainty is None else source_uncertainty.radial_std_m
    target_radius = 0.0 if target_uncertainty is None else target_uncertainty.radial_std_m
    inflated_margin = sigma_scale * (source_radius + target_radius)
    return float(max(0.0, distance_m - inflated_margin))


def uncertainty_confidence_penalty(
    source_uncertainty: PositionalUncertainty | None,
    target_uncertainty: PositionalUncertainty | None,
    reference_std_m: float = 2.0,
) -> float:
    """Return a multiplicative confidence penalty in ``[0, 1]``.

    The penalty is a transparent heuristic for prototype experiments. It should
    be replaced by empirical calibration once probabilistic predictors and
    labelled validation data are available.
    """
    if reference_std_m <= 0.0:
        raise ValueError("reference_std_m must be positive")

    source_radius = 0.0 if source_uncertainty is None else source_uncertainty.radial_std_m
    target_radius = 0.0 if target_uncertainty is None else target_uncertainty.radial_std_m
    total_std = source_radius + target_radius
    return float(np.clip(1.0 - total_std / reference_std_m, 0.0, 1.0))
