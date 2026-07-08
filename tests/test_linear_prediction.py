import numpy as np
import pytest

from safecrossai.prediction.linear import linear_regression_predict


def test_linear_regression_predict_extrapolates_constant_velocity_motion() -> None:
    history = np.array(
        [
            [0.0, 1.0],
            [1.0, 3.0],
            [2.0, 5.0],
            [3.0, 7.0],
        ]
    )

    prediction = linear_regression_predict(history, horizon=3)

    expected = np.array(
        [
            [4.0, 9.0],
            [5.0, 11.0],
            [6.0, 13.0],
        ]
    )
    np.testing.assert_allclose(prediction, expected, atol=1e-10)


def test_linear_regression_predict_rejects_invalid_shape() -> None:
    with pytest.raises(ValueError, match="history must have shape"):
        linear_regression_predict(np.array([1.0, 2.0]), horizon=4)


def test_linear_regression_predict_rejects_non_positive_horizon() -> None:
    history = np.array([[0.0, 0.0], [1.0, 1.0]])

    with pytest.raises(ValueError, match="horizon must be positive"):
        linear_regression_predict(history, horizon=0)
