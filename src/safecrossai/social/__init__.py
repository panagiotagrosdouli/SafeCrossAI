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
from .graph import InteractionEdge, InteractionGraph, build_radius_interaction_graph
from .neighbors import Neighbor, SocialAgent, find_neighbors, k_nearest_neighbors
from .scene import Scene, make_scene
from .sequences import SceneSequence, build_scene_sequences
from .temporal_features import (
    AgentPositionHistory,
    TemporalTensor,
    extract_position_histories,
    sequence_to_temporal_tensor,
)
from .ttc import ClosestApproach, closest_point_of_approach, time_to_collision

__all__ = [
    "bearing",
    "distance",
    "heading",
    "relative_position",
    "relative_velocity",
    "InteractionEdge",
    "InteractionGraph",
    "build_radius_interaction_graph",
    "Neighbor",
    "SocialAgent",
    "find_neighbors",
    "k_nearest_neighbors",
    "Scene",
    "make_scene",
    "SceneSequence",
    "build_scene_sequences",
    "AgentPositionHistory",
    "TemporalTensor",
    "extract_position_histories",
    "sequence_to_temporal_tensor",
    "ClosestApproach",
    "closest_point_of_approach",
    "time_to_collision",
]
