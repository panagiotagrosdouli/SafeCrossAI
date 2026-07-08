import numpy as np
import pytest

from safecrossai.risk import (
    PositionalUncertainty,
    uncertainty_confidence_penalty,
    uncertainty_inflated_distance,
)


def test_positional_uncertainty_computes_radial_std() -> None:
    uncertainty = PositionalUncertainty(np.diag([0.25, 0.75]))

    assert uncertainty.radial_std_m == pytest.approx(1.0)


def test_positional_uncertainty_rejects_invalid_covariance() -> None:
    with pytest.raises(ValueError, match="shape"):
        PositionalUncertainty(np.eye(3))

    with pytest.raises(ValueError, match="symmetric"):
        PositionalUncertainty(np.array([[1.0, 0.5], [0.0, 1.0]]))

    with pytest.raises(ValueError, match="positive semi-definite"):
        PositionalUncertainty(np.diag([1.0, -0.1]))


def test_uncertainty_inflated_distance_is_conservative() -> None:
    source = PositionalUncertainty(np.diag([0.25, 0.0]))
    target = PositionalUncertainty(np.diag([0.25, 0.0]))

    distance = uncertainty_inflated_distance(3.0, source, target, sigma_scale=1.0)

    assert distance == pytest.approx(2.0)


def test_uncertainty_confidence_penalty_decreases_with_uncertainty() -> None:
    source = PositionalUncertainty(np.diag([0.25, 0.0]))
    target = PositionalUncertainty(np.diag([0.25, 0.0]))

    penalty = uncertainty_confidence_penalty(source, target, reference_std_m=2.0)

    assert penalty == pytest.approx(0.5)
