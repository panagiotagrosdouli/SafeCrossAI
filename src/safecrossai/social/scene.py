"""Unified scene representation for social trajectory modeling."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from safecrossai.social.graph import InteractionGraph, build_radius_interaction_graph
from safecrossai.social.neighbors import SocialAgent


@dataclass(frozen=True)
class Scene:
    """A traffic scene snapshot at a single timestamp."""

    scene_id: str
    timestamp: float
    agents: list[SocialAgent]
    metadata: dict[str, Any] = field(default_factory=dict)

    def build_interaction_graph(self, radius: float) -> InteractionGraph:
        """Build a radius-based interaction graph for this scene."""
        return build_radius_interaction_graph(self.agents, radius=radius)

    def agent_ids(self) -> list[str]:
        """Return deterministic agent identifiers in scene order."""
        return [agent.agent_id for agent in self.agents]


def make_scene(
    scene_id: str,
    timestamp: float,
    agents: list[SocialAgent],
    metadata: dict[str, Any] | None = None,
) -> Scene:
    """Create a scene with optional metadata."""
    return Scene(
        scene_id=scene_id,
        timestamp=timestamp,
        agents=agents,
        metadata={} if metadata is None else dict(metadata),
    )
