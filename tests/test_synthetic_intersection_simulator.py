from __future__ import annotations

import math

import pandas as pd

from safecrossai.simulation import SyntheticIntersectionSimulator
from safecrossai.simulation.intersection_simulator import _cpa, _ttc


def test_ttc_and_cpa_are_finite_for_head_on_pair() -> None:
    ttc = _ttc([0.0, 0.0], [1.0, 0.0], [5.0, 0.0], [-1.0, 0.0])
    time_to_cpa, distance_to_cpa = _cpa([0.0, 0.0], [1.0, 0.0], [5.0, 0.0], [-1.0, 0.0])
    assert math.isfinite(ttc)
    assert time_to_cpa > 0.0
    assert distance_to_cpa == 0.0


def test_synthetic_intersection_demo_writes_required_outputs(tmp_path) -> None:
    summary = SyntheticIntersectionSimulator().run(tmp_path)
    assert summary["label"] == "Synthetic Demo"
    required = [
        "scene_metadata.json",
        "observed_trajectories.csv",
        "ground_truth_future.csv",
        "predicted_trajectories.csv",
        "agent_states.csv",
        "interaction_edges.csv",
        "risk_scores.csv",
        "conflict_events.csv",
        "simulation_summary.json",
        "metrics/summary.json",
        "metrics/metrics.csv",
    ]
    for relative_path in required:
        assert (tmp_path / relative_path).exists()
    risks = pd.read_csv(tmp_path / "risk_scores.csv")
    assert {"risk_score", "risk_level", "recommended_warning_flag"}.issubset(risks.columns)
