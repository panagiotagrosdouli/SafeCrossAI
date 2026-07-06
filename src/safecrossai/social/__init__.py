"""Social interaction utilities for trajectory prediction.

This package contains reusable geometry, neighbor search,
interaction graph, and collision-risk utilities that will
be shared across classical and learning-based predictors.
"""

from .geometry import (
    distance,
    relative_position,
    relative_velocity,
    heading,
    bearing,
)

__all__ = [
    "distance",
    "relative_position",
    "relative_velocity",
    "heading",
    "bearing",
]
