import numpy as np
import pytest

from safecrossai.social.neighbors import SocialAgent, find_neighbors, k_nearest_neighbors


def test_find_neighbors_returns_agents_within_radius_sorted_by_distance() -> None:
    target = SocialAgent(agent_id="target", position=np.array([0.0, 0.0]))
    agents = [
        SocialAgent(agent_id="far", position=np.array([10.0, 0.0])),
        SocialAgent(agent_id="near", position=np.array([1.0, 0.0])),
        SocialAgent(agent_id="mid", position=np.array([3.0, 0.0])),
    ]

    neighbors = find_neighbors(target, agents, radius=5.0)

    assert [neighbor.agent.agent_id for neighbor in neighbors] == ["near", "mid"]
    assert [neighbor.distance for neighbor in neighbors] == [1.0, 3.0]


def test_find_neighbors_skips_target_agent() -> None:
    target = SocialAgent(agent_id="same", position=np.array([0.0, 0.0]))
    agents = [
        SocialAgent(agent_id="same", position=np.array([0.0, 0.0])),
        SocialAgent(agent_id="other", position=np.array([1.0, 0.0])),
    ]

    neighbors = find_neighbors(target, agents, radius=2.0)

    assert [neighbor.agent.agent_id for neighbor in neighbors] == ["other"]


def test_k_nearest_neighbors_returns_limited_sorted_neighbors() -> None:
    target = SocialAgent(agent_id="target", position=np.array([0.0, 0.0]))
    agents = [
        SocialAgent(agent_id="c", position=np.array([3.0, 0.0])),
        SocialAgent(agent_id="a", position=np.array([1.0, 0.0])),
        SocialAgent(agent_id="b", position=np.array([2.0, 0.0])),
    ]

    neighbors = k_nearest_neighbors(target, agents, k=2)

    assert [neighbor.agent.agent_id for neighbor in neighbors] == ["a", "b"]


def test_neighbor_search_rejects_invalid_parameters() -> None:
    target = SocialAgent(agent_id="target", position=np.array([0.0, 0.0]))

    with pytest.raises(ValueError, match="radius must be non-negative"):
        find_neighbors(target, [], radius=-1.0)

    with pytest.raises(ValueError, match="k must be positive"):
        k_nearest_neighbors(target, [], k=0)
