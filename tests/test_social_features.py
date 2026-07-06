import numpy as np
import pytest

from safecrossai.social.features import extract_social_features
from safecrossai.social.neighbors import SocialAgent


def test_extract_social_features() -> None:
    target = SocialAgent(
        agent_id="a",
        position=np.array([0.0, 0.0]),
        velocity=np.array([1.0, 0.0]),
    )
    neighbor = SocialAgent(
        agent_id="b",
        position=np.array([3.0, 4.0]),
        velocity=np.array([2.0, 0.0]),
    )

    features = extract_social_features(target, neighbor)

    assert features.distance == pytest.approx(5.0)
    assert features.relative_speed == pytest.approx(1.0)
    assert features.bearing > 0.0
