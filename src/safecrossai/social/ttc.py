"""Time-to-collision and closest-approach utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ClosestApproach:
    """Closest point of approach between two moving agents."""

    time: float
    distance: float


def closest_point_of_approach(
    position_a: np.ndarray,
    velocity_a: np.ndarray,
    position_b: np.ndarray,
    velocity_b: np.ndarray,
) -> ClosestApproach:
    """Compute closest point of approach under constant velocity motion."""
    relative_position = np.asarray(position_b, dtype=float) - np.asarray(position_a, dtype=float)
    relative_velocity = np.asarray(velocity_b, dtype=float) - np.asarray(velocity_a, dtype=float)
    speed_squared = float(np.dot(relative_velocity, relative_velocity))

    if speed_squared == 0.0:
        return ClosestApproach(time=0.0, distance=float(np.linalg.norm(relative_position)))

    time = -float(np.dot(relative_position, relative_velocity)) / speed_squared
    time = max(0.0, time)
    closest_relative_position = relative_position + time * relative_velocity
    return ClosestApproach(time=time, distance=float(np.linalg.norm(closest_relative_position)))


def time_to_collision(
    position_a: np.ndarray,
    velocity_a: np.ndarray,
    position_b: np.ndarray,
    velocity_b: np.ndarray,
    collision_radius: float,
) -> float | None:
    """Estimate time until two circular agents collide.

    Returns ``None`` when the agents do not collide under constant velocity.
    """
    if collision_radius < 0.0:
        raise ValueError("collision_radius must be non-negative")

    relative_position = np.asarray(position_b, dtype=float) - np.asarray(position_a, dtype=float)
    relative_velocity = np.asarray(velocity_b, dtype=float) - np.asarray(velocity_a, dtype=float)

    a = float(np.dot(relative_velocity, relative_velocity))
    b = 2.0 * float(np.dot(relative_position, relative_velocity))
    c = float(np.dot(relative_position, relative_position)) - collision_radius**2

    if c <= 0.0:
        return 0.0
    if a == 0.0:
        return None

    discriminant = b * b - 4.0 * a * c
    if discriminant < 0.0:
        return None

    sqrt_discriminant = float(np.sqrt(discriminant))
    roots = [(-b - sqrt_discriminant) / (2.0 * a), (-b + sqrt_discriminant) / (2.0 * a)]
    future_roots = [root for root in roots if root >= 0.0]
    if not future_roots:
        return None
    return min(future_roots)
