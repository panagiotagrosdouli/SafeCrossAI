import numpy as np

from safecrossai.social import SocialAgent, make_scene
from safecrossai.social.sequences import SceneSequence
from safecrossai.social.temporal_features import extract_position_histories


def test_extract_position_histories_handles_missing_agents() -> None:
    sequence = SceneSequence(
        [
            make_scene(
                scene_id="s0",
                timestamp=0.0,
                agents=[
                    SocialAgent(agent_id="a", position=np.array([0.0, 0.0])),
                    SocialAgent(agent_id="b", position=np.array([2.0, 0.0])),
                ],
            ),
            make_scene(
                scene_id="s1",
                timestamp=1.0,
                agents=[SocialAgent(agent_id="a", position=np.array([1.0, 0.0]))],
            ),
        ]
    )

    histories = extract_position_histories(sequence)

    assert [history.agent_id for history in histories] == ["a", "b"]
    np.testing.assert_allclose(histories[0].positions, np.array([[0.0, 0.0], [1.0, 0.0]]))
    np.testing.assert_array_equal(histories[0].observed_mask, np.array([True, True]))
    assert np.isnan(histories[1].positions[1]).all()
    np.testing.assert_array_equal(histories[1].observed_mask, np.array([True, False]))
