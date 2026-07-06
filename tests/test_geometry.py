import math

import numpy as np
import pytest

from safecrossai.social.geometry import (
    bearing,
    distance,
    heading,
    relative_position,
    relative_velocity,
)


def test_distance_between_points() -> None:
    a = np.array([0.0, 0.0])
    b = np.array([3.0, 4.0])

    assert distance(a, b) == pytest.approx(5.0)


def test_relative_position_returns_vector_from_first_to_second_point() -> None:
    a = np.array([1.0, 2.0])
    b = np.array([4.0, 6.0])

    result = relative_position(a, b)

    np.testing.assert_allclose(result, np.array([3.0, 4.0]))


def test_relative_velocity_returns_velocity_difference() -> None:
    v1 = np.array([1.0, 0.5])
    v2 = np.array([2.5, -0.5])

    result = relative_velocity(v1, v2)

    np.testing.assert_allclose(result, np.array([1.5, -1.0]))


def test_heading_returns_angle_in_radians() -> None:
    assert heading(np.array([1.0, 0.0])) == pytest.approx(0.0)
    assert heading(np.array([0.0, 1.0])) == pytest.approx(math.pi / 2)


def test_bearing_returns_angle_from_first_point_to_second_point() -> None:
    a = np.array([0.0, 0.0])
    b = np.array([0.0, 2.0])

    assert bearing(a, b) == pytest.approx(math.pi / 2)
