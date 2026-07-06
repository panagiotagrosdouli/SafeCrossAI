import numpy as np
import pytest

from safecrossai.social.ttc import closest_point_of_approach, time_to_collision


def test_closest_point_of_approach_for_head_on_agents() -> None:
    result = closest_point_of_approach(
        position_a=np.array([0.0, 0.0]),
        velocity_a=np.array([1.0, 0.0]),
        position_b=np.array([10.0, 0.0]),
        velocity_b=np.array([-1.0, 0.0]),
    )

    assert result.time == pytest.approx(5.0)
    assert result.distance == pytest.approx(0.0)


def test_time_to_collision_for_head_on_agents() -> None:
    ttc = time_to_collision(
        position_a=np.array([0.0, 0.0]),
        velocity_a=np.array([1.0, 0.0]),
        position_b=np.array([10.0, 0.0]),
        velocity_b=np.array([-1.0, 0.0]),
        collision_radius=1.0,
    )

    assert ttc == pytest.approx(4.5)


def test_time_to_collision_returns_none_when_agents_do_not_collide() -> None:
    ttc = time_to_collision(
        position_a=np.array([0.0, 0.0]),
        velocity_a=np.array([1.0, 0.0]),
        position_b=np.array([0.0, 10.0]),
        velocity_b=np.array([1.0, 0.0]),
        collision_radius=1.0,
    )

    assert ttc is None


def test_time_to_collision_returns_zero_when_agents_overlap() -> None:
    ttc = time_to_collision(
        position_a=np.array([0.0, 0.0]),
        velocity_a=np.array([0.0, 0.0]),
        position_b=np.array([0.5, 0.0]),
        velocity_b=np.array([0.0, 0.0]),
        collision_radius=1.0,
    )

    assert ttc == 0.0


def test_time_to_collision_rejects_negative_collision_radius() -> None:
    with pytest.raises(ValueError, match="collision_radius must be non-negative"):
        time_to_collision(
            position_a=np.array([0.0, 0.0]),
            velocity_a=np.array([0.0, 0.0]),
            position_b=np.array([1.0, 0.0]),
            velocity_b=np.array([0.0, 0.0]),
            collision_radius=-1.0,
        )
