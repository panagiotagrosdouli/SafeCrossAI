"""Interaction graph utilities for social trajectory modeling."""

from __future__ import annotations

from dataclasses import dataclass

from safecrossai.social.neighbors import SocialAgent
from safecrossai.social.ttc import closest_point_of_approach


@dataclass(frozen=True)
class InteractionEdge:
    """Directed interaction edge between two agents."""

    source_id: str
    target_id: str
    distance: float
    time_to_closest_approach: float
    closest_approach_distance: float
    weight: float


@dataclass(frozen=True)
class InteractionGraph:
    """Lightweight interaction graph representation."""

    nodes: list[SocialAgent]
    edges: list[InteractionEdge]


def build_radius_interaction_graph(
    agents: list[SocialAgent],
    radius: float,
) -> InteractionGraph:
    """Build a directed radius-based interaction graph.

    Edges are created between distinct agents whose current distance is less
    than or equal to ``radius``. Edge weights use inverse distance so closer
    agents receive larger weights.
    """
    if radius < 0.0:
        raise ValueError("radius must be non-negative")

    edges: list[InteractionEdge] = []
    for source in agents:
        for target in agents:
            if source.agent_id == target.agent_id:
                continue
            source_velocity = source.velocity
            target_velocity = target.velocity
            if source_velocity is None or target_velocity is None:
                time_to_closest = 0.0
                closest_distance = float("nan")
            else:
                approach = closest_point_of_approach(
                    source.position,
                    source_velocity,
                    target.position,
                    target_velocity,
                )
                time_to_closest = approach.time
                closest_distance = approach.distance

            current_distance = float(
                ((source.position - target.position) ** 2).sum() ** 0.5
            )
            if current_distance <= radius:
                edges.append(
                    InteractionEdge(
                        source_id=source.agent_id,
                        target_id=target.agent_id,
                        distance=current_distance,
                        time_to_closest_approach=time_to_closest,
                        closest_approach_distance=closest_distance,
                        weight=1.0 / (1.0 + current_distance),
                    )
                )

    edges.sort(key=lambda edge: (edge.source_id, edge.target_id))
    return InteractionGraph(nodes=list(agents), edges=edges)
