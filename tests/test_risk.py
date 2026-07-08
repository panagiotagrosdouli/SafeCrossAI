from __future__ import annotations

import numpy as np

from safecrossai.risk import RiskConfig, assess_pairwise_risk, distance_risk, ttc_risk
from safecrossai.social import SocialAgent


def test_distance_risk_bounds() -> None:
    assert distance_risk(0.0, 10.0) == 1.0
    assert distance_risk(10.0, 10.0) == 0.0
    assert distance_risk(20.0, 10.0) == 0.0


def test_ttc_risk_none_is_zero() -> None:
    assert ttc_risk(None, 5.0) == 0.0


def test_pairwise_risk_report_has_valid_score() -> None:
    source = SocialAgent(
        agent_id="a",
        position=np.array([0.0, 0.0]),
        velocity=np.array([1.0, 0.0]),
    )
    target = SocialAgent(
        agent_id="b",
        position=np.array([5.0, 0.0]),
        velocity=np.array([-1.0, 0.0]),
    )
    report = assess_pairwise_risk(source, target, RiskConfig())
    assert 0.0 <= report.score <= 1.0
    assert 0.0 <= report.confidence <= 1.0
    assert report.source_id == "a"
    assert report.target_id == "b"
