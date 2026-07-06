"""Social interaction utilities for trajectory prediction.

This package contains reusable geometry, neighbor search,
interaction graph, and collision-risk utilities that will
be shared across classical and learning-based predictors.
"""

from .geometry import (
    bearing,
    distance,
    heading,
    relative_position,
    relative_velocity,
)
from .neighbors import Neighbor, SocialAgent, find_neighbors, k_nearest_neighbors

__all__ = [
    "bearing",
    "distance",
    "heading",
    "relative_position",
    "relative_velocity",
    "Neighbor",
    "SocialAgent",
    "find_neighbors",
    "k_nearest_neighbors",
]
