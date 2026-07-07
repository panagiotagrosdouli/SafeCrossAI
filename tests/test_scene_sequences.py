import numpy as np
import pytest

from safecrossai.social import SocialAgent, make_scene
from safecrossai.social.sequences import SceneSequence, build_scene_sequences


def test_scene_sequence_exposes_time_range_and_agent_ids() -> None:
    scenes = [
        make_scene(
            scene_id="s0",
            timestamp=0.0,
            agents=[SocialAgent(agent_id="b", position=np.array([0.0, 0.0]))],
        ),
        make_scene(
            scene_id="s1",
            timestamp=1.0,
            agents=[SocialAgent(agent_id="a", position=np.array([1.0, 0.0]))],
        ),
    ]

    sequence = SceneSequence(scenes)

    assert sequence.start_time == 0.0
    assert sequence.end_time == 1.0
    assert sequence.agent_ids() == ["a", "b"]


def test_scene_sequence_requires_non_empty_sorted_scenes() -> None:
    with pytest.raises(ValueError, match="scenes must not be empty"):
        SceneSequence([])

    scenes = [
        make_scene(scene_id="s1", timestamp=1.0, agents=[]),
        make_scene(scene_id="s0", timestamp=0.0, agents=[]),
    ]
    with pytest.raises(ValueError, match="scenes must be sorted by timestamp"):
        SceneSequence(scenes)


def test_build_scene_sequences_uses_sliding_windows() -> None:
    scenes = [make_scene(scene_id=f"s{i}", timestamp=float(i), agents=[]) for i in range(4)]

    sequences = build_scene_sequences(scenes, sequence_length=2, stride=1)

    assert len(sequences) == 3
    assert [sequence.start_time for sequence in sequences] == [0.0, 1.0, 2.0]


def test_build_scene_sequences_rejects_invalid_parameters() -> None:
    with pytest.raises(ValueError, match="sequence_length must be positive"):
        build_scene_sequences([], sequence_length=0)

    with pytest.raises(ValueError, match="stride must be positive"):
        build_scene_sequences([], sequence_length=1, stride=0)
