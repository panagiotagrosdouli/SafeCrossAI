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
