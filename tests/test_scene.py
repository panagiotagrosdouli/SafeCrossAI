import numpy as np

from safecrossai.social.neighbors import SocialAgent
from safecrossai.social.scene import make_scene


def test_make_scene_stores_agents_and_metadata() -> None:
    metadata = {"location": "intersection_a"}
    agents = [SocialAgent(agent_id="a", position=np.array([0.0, 0.0]))]

    scene = make_scene(scene_id="scene_1", timestamp=1.5, agents=agents, metadata=metadata)
    metadata["location"] = "changed"

    assert scene.scene_id == "scene_1"
    assert scene.timestamp == 1.5
    assert scene.agent_ids() == ["a"]
    assert scene.metadata["location"] == "intersection_a"


def test_scene_builds_interaction_graph() -> None:
    agents = [
        SocialAgent(agent_id="a", position=np.array([0.0, 0.0]), velocity=np.array([1.0, 0.0])),
        SocialAgent(agent_id="b", position=np.array([1.0, 0.0]), velocity=np.array([0.0, 0.0])),
    ]
    scene = make_scene(scene_id="scene_1", timestamp=0.0, agents=agents)

    graph = scene.build_interaction_graph(radius=2.0)

    assert len(graph.nodes) == 2
    assert len(graph.edges) == 2
