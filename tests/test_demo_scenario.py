from __future__ import annotations

from safecrossai.datasets.demo import make_intersection_demo_scenario


def test_demo_scenario_has_requested_length() -> None:
    scenario = make_intersection_demo_scenario(num_steps=5, dt=0.1)
    assert len(scenario.scenes) == 5
    assert scenario.dt == 0.1


def test_demo_scenario_has_agents() -> None:
    scenario = make_intersection_demo_scenario(num_steps=2)
    scene = scenario.scenes[0]
    assert len(scene.agents) == 3
    assert sorted(scene.agent_ids()) == ["cyclist_1", "pedestrian_1", "vehicle_1"]
