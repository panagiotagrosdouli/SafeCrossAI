"""Neighbor search utilities for social trajectory modeling."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np

from safecrossai.social.geometry import distance


@dataclass(frozen=True)
class SocialAgent:
    """Lightweight representation of an agent in a social scene."""

    agent_id: str
    position: np.ndarray
    velocity: np.ndarray | None = None
    agent_type: str = "unknown"


@dataclass(frozen=True)
class Neighbor:
    """Neighboring agent with distance to the target agent."""

    agent: SocialAgent
    distance: float


def find_neighbors(
    target: SocialAgent,
    agents: Iterable[SocialAgent],
    radius: float,
) -> list[Neighbor]:
    """Find agents within a radius of the target agent.

    The target itself is skipped when an agent with the same ``agent_id`` is
    present in the candidate list. Results are sorted by distance and then by
    agent id for deterministic behavior.
    """
    if radius < 0.0:
        raise ValueError("radius must be non-negative")

    neighbors: list[Neighbor] = []
    for agent in agents:
        if agent.agent_id == target.agent_id:
            continue
        agent_distance = distance(target.position, agent.position)
        if agent_distance <= radius:
            neighbors.append(Neighbor(agent=agent, distance=agent_distance))

    return sorted(neighbors, key=lambda item: (item.distance, item.agent.agent_id))


def k_nearest_neighbors(
    target: SocialAgent,
    agents: Iterable[SocialAgent],
    k: int,
) -> list[Neighbor]:
    """Return the k nearest agents to the target agent."""
    if k < 1:
        raise ValueError("k must be positive")

    neighbors: list[Neighbor] = []
    for agent in agents:
        if agent.agent_id == target.agent_id:
            continue
        neighbors.append(
            Neighbor(
                agent=agent,
                distance=distance(target.position, agent.position),
            )
        )

    return sorted(neighbors, key=lambda item: (item.distance, item.agent.agent_id))[:k]
