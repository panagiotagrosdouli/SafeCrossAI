import numpy as np

from safecrossai.social import SocialAgent, distance, find_neighbors


def test_social_package_exports_geometry_and_neighbors() -> None:
    target = SocialAgent(agent_id="target", position=np.array([0.0, 0.0]))
    other = SocialAgent(agent_id="other", position=np.array([1.0, 0.0]))

    assert distance(target.position, other.position) == 1.0
    assert find_neighbors(target, [other], radius=2.0)[0].agent.agent_id == "other"
