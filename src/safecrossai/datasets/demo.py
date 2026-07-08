"""Deterministic demo scenarios for SafeCrossAI visualizations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from safecrossai.social import Scene, SocialAgent, make_scene


@dataclass(frozen=True)
class DemoScenario:
    """Multi-agent synthetic scenario used for demos and smoke tests."""

    scenes: list[Scene]
    dt: float


def make_intersection_demo_scenario(num_steps: int = 30, dt: float = 0.2) -> DemoScenario:
    """Create a deterministic synthetic intersection scenario.

    The scenario contains a pedestrian, a cyclist, and a vehicle moving through
    a simplified 2D intersection. It is not a real dataset and must not be used
    as benchmark evidence.
    """
    if num_steps < 2:
        raise ValueError("num_steps must be at least 2")
    if dt <= 0.0:
        raise ValueError("dt must be positive")

    initial_states = {
        "pedestrian_1": (np.array([-4.0, -1.5]), np.array([0.45, 0.12]), "pedestrian"),
        "cyclist_1": (np.array([-3.5, 3.0]), np.array([0.75, -0.25]), "cyclist"),
        "vehicle_1": (np.array([7.0, 0.15]), np.array([-1.20, 0.0]), "vehicle"),
    }

    scenes: list[Scene] = []
    for step in range(num_steps):
        timestamp = step * dt
        agents: list[SocialAgent] = []
        for agent_id, (position0, velocity, agent_type) in initial_states.items():
            position = position0 + timestamp * velocity
            agents.append(
                SocialAgent(
                    agent_id=agent_id,
                    position=position.astype(float),
                    velocity=velocity.astype(float),
                    agent_type=agent_type,
                )
            )
        scenes.append(
            make_scene(
                scene_id=f"demo_{step:03d}",
                timestamp=timestamp,
                agents=agents,
                metadata={"synthetic": True, "dt": dt},
            )
        )
    return DemoScenario(scenes=scenes, dt=dt)
