"""Social interaction feature extraction utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from safecrossai.social.geometry import bearing, distance, heading, relative_velocity
from safecrossai.social.neighbors import SocialAgent


@dataclass(frozen=True)
class SocialFeatures:
    distance: float
    relative_speed: float
    heading_difference: float
    bearing: float


def extract_social_features(target: SocialAgent, neighbor: SocialAgent) -> SocialFeatures:
    """Extract basic pairwise social interaction features."""
    target_velocity = target.velocity if target.velocity is not None else np.zeros(2)
    neighbor_velocity = neighbor.velocity if neighbor.velocity is not None else np.zeros(2)
    rv = relative_velocity(target_velocity, neighbor_velocity)
    return SocialFeatures(
        distance=distance(target.position, neighbor.position),
        relative_speed=float(np.linalg.norm(rv)),
        heading_difference=heading(neighbor_velocity) - heading(target_velocity),
        bearing=bearing(target.position, neighbor.position),
    )
