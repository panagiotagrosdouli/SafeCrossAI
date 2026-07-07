"""Multi-frame scene sequence representation."""

from __future__ import annotations

from dataclasses import dataclass

from safecrossai.social.scene import Scene


@dataclass(frozen=True)
class SceneSequence:
    """Ordered sequence of traffic scene snapshots."""

    scenes: list[Scene]

    def __post_init__(self) -> None:
        if not self.scenes:
            raise ValueError("scenes must not be empty")
        timestamps = [scene.timestamp for scene in self.scenes]
        if timestamps != sorted(timestamps):
            raise ValueError("scenes must be sorted by timestamp")

    @property
    def start_time(self) -> float:
        """Return the first scene timestamp."""
        return self.scenes[0].timestamp

    @property
    def end_time(self) -> float:
        """Return the last scene timestamp."""
        return self.scenes[-1].timestamp

    def agent_ids(self) -> list[str]:
        """Return sorted unique agent ids appearing in the sequence."""
        return sorted({agent.agent_id for scene in self.scenes for agent in scene.agents})


def build_scene_sequences(
    scenes: list[Scene],
    sequence_length: int,
    stride: int = 1,
) -> list[SceneSequence]:
    """Build sliding-window scene sequences from ordered scenes."""
    if sequence_length < 1:
        raise ValueError("sequence_length must be positive")
    if stride < 1:
        raise ValueError("stride must be positive")
    if not scenes:
        return []

    ordered_scenes = sorted(scenes, key=lambda scene: scene.timestamp)
    sequences: list[SceneSequence] = []
    for start in range(0, len(ordered_scenes) - sequence_length + 1, stride):
        sequences.append(SceneSequence(ordered_scenes[start : start + sequence_length]))
    return sequences
