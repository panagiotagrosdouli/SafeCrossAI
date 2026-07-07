"""Temporal feature extraction from scene sequences."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from safecrossai.social.sequences import SceneSequence


@dataclass(frozen=True)
class AgentPositionHistory:
    """Position history for one agent over a scene sequence."""

    agent_id: str
    positions: np.ndarray
    observed_mask: np.ndarray


@dataclass(frozen=True)
class TemporalTensor:
    """Tensor-style temporal representation for model inputs."""

    agent_ids: list[str]
    positions: np.ndarray
    observed_mask: np.ndarray


def extract_position_histories(sequence: SceneSequence) -> list[AgentPositionHistory]:
    """Extract per-agent position histories from a scene sequence.

    Missing agents are represented with NaN positions and ``False`` in the
    observed mask. Histories are returned in sorted agent-id order.
    """
    agent_ids = sequence.agent_ids()
    histories: list[AgentPositionHistory] = []

    for agent_id in agent_ids:
        positions = np.full((len(sequence.scenes), 2), np.nan, dtype=float)
        observed_mask = np.zeros(len(sequence.scenes), dtype=bool)

        for scene_index, scene in enumerate(sequence.scenes):
            for agent in scene.agents:
                if agent.agent_id == agent_id:
                    positions[scene_index] = agent.position
                    observed_mask[scene_index] = True
                    break

        histories.append(
            AgentPositionHistory(
                agent_id=agent_id,
                positions=positions,
                observed_mask=observed_mask,
            )
        )

    return histories


def sequence_to_temporal_tensor(sequence: SceneSequence) -> TemporalTensor:
    """Convert a scene sequence into stacked position and mask arrays.

    The returned position tensor has shape ``(num_agents, num_steps, 2)`` and
    the observed mask has shape ``(num_agents, num_steps)``.
    """
    histories = extract_position_histories(sequence)
    if not histories:
        return TemporalTensor(
            agent_ids=[],
            positions=np.empty((0, len(sequence.scenes), 2), dtype=float),
            observed_mask=np.empty((0, len(sequence.scenes)), dtype=bool),
        )

    return TemporalTensor(
        agent_ids=[history.agent_id for history in histories],
        positions=np.stack([history.positions for history in histories]),
        observed_mask=np.stack([history.observed_mask for history in histories]),
    )
