import numpy as np
import pytest

from safecrossai.social.graph import build_radius_interaction_graph
from safecrossai.social.neighbors import SocialAgent


def test_build_radius_interaction_graph_creates_directed_edges_within_radius() -> None:
    agents = [
        SocialAgent(
            agent_id="a",
            position=np.array([0.0, 0.0]),
            velocity=np.array([1.0, 0.0]),
        ),
        SocialAgent(
            agent_id="b",
            position=np.array([1.0, 0.0]),
            velocity=np.array([0.0, 0.0]),
        ),
        SocialAgent(
            agent_id="c",
            position=np.array([10.0, 0.0]),
            velocity=np.array([0.0, 0.0]),
        ),
    ]

    graph = build_radius_interaction_graph(agents, radius=2.0)

    assert len(graph.nodes) == 3
    assert [(edge.source_id, edge.target_id) for edge in graph.edges] == [("a", "b"), ("b", "a")]
    assert graph.edges[0].distance == pytest.approx(1.0)
    assert graph.edges[0].weight == pytest.approx(0.5)


def test_build_radius_interaction_graph_rejects_negative_radius() -> None:
    with pytest.raises(ValueError, match="radius must be non-negative"):
        build_radius_interaction_graph([], radius=-1.0)
