#!/usr/bin/env python
"""Run a deterministic pairwise interaction-risk demo."""

from __future__ import annotations

from safecrossai.datasets.demo import make_intersection_demo_scenario
from safecrossai.risk import RiskConfig, assess_pairwise_risk


def main() -> None:
    scenario = make_intersection_demo_scenario(num_steps=1)
    scene = scenario.scenes[0]
    config = RiskConfig()

    print(f"Scene: {scene.scene_id} t={scene.timestamp:.2f}s")
    for i, source in enumerate(scene.agents):
        for target in scene.agents[i + 1 :]:
            report = assess_pairwise_risk(source, target, config=config)
            print(
                f"{report.source_id} -> {report.target_id}: "
                f"level={report.level.value}, score={report.score:.3f}, "
                f"distance={report.distance_m:.2f}m, ttc={report.time_to_intersection}"
            )
            print(f"  {report.explanation}")


if __name__ == "__main__":
    main()
