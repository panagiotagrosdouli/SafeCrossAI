"""Interpretable baseline risk scoring for road-user interactions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from safecrossai.social.neighbors import SocialAgent
from safecrossai.social.ttc import closest_point_of_approach, time_to_collision


class RiskLevel(str, Enum):
    """Discrete risk labels for reports."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    SEVERE = "severe"


@dataclass(frozen=True)
class RiskConfig:
    """Configuration for deterministic baseline risk scoring."""

    interaction_radius_m: float = 1.5
    ttc_horizon_s: float = 6.0
    distance_horizon_m: float = 12.0
    high_threshold: float = 0.65
    severe_threshold: float = 0.85

    def __post_init__(self) -> None:
        if self.interaction_radius_m < 0.0:
            raise ValueError("interaction_radius_m must be non-negative")
        if self.ttc_horizon_s <= 0.0:
            raise ValueError("ttc_horizon_s must be positive")
        if self.distance_horizon_m <= 0.0:
            raise ValueError("distance_horizon_m must be positive")
        if self.high_threshold > self.severe_threshold:
            raise ValueError("high_threshold must be <= severe_threshold")


@dataclass(frozen=True)
class PairwiseRiskReport:
    """Interpretable risk report for a pair of road users."""

    source_id: str
    target_id: str
    score: float
    level: RiskLevel
    distance_m: float
    time_to_intersection: float | None
    closest_approach_time: float
    closest_approach_distance_m: float
    confidence: float
    explanation: str


def _clip01(value: float) -> float:
    return float(np.clip(value, 0.0, 1.0))


def ttc_risk(ttc_seconds: float | None, horizon_seconds: float) -> float:
    """Convert time-to-interaction to a normalized score."""
    if horizon_seconds <= 0.0:
        raise ValueError("horizon_seconds must be positive")
    if ttc_seconds is None:
        return 0.0
    if ttc_seconds <= 0.0:
        return 1.0
    return _clip01(1.0 - ttc_seconds / horizon_seconds)


def distance_risk(distance_m: float, horizon_m: float) -> float:
    """Convert distance to a normalized proximity score."""
    if horizon_m <= 0.0:
        raise ValueError("horizon_m must be positive")
    if distance_m < 0.0:
        raise ValueError("distance_m must be non-negative")
    return _clip01(1.0 - distance_m / horizon_m)


def confidence_score(has_velocity_a: bool, has_velocity_b: bool) -> float:
    """Return confidence for a constant-velocity pairwise estimate."""
    if has_velocity_a and has_velocity_b:
        return 1.0
    if has_velocity_a or has_velocity_b:
        return 0.5
    return 0.25


def conflict_score(
    *,
    distance_m: float,
    ttc_seconds: float | None,
    closest_approach_distance_m: float,
    config: RiskConfig,
) -> float:
    """Compute a baseline conflict score in [0, 1]."""
    current_distance_component = distance_risk(distance_m, config.distance_horizon_m)
    ttc_component = ttc_risk(ttc_seconds, config.ttc_horizon_s)
    closest_component = distance_risk(max(closest_approach_distance_m, 0.0), config.distance_horizon_m)
    return _clip01(0.50 * ttc_component + 0.30 * closest_component + 0.20 * current_distance_component)


def _level_from_score(score: float, config: RiskConfig) -> RiskLevel:
    if score >= config.severe_threshold:
        return RiskLevel.SEVERE
    if score >= config.high_threshold:
        return RiskLevel.HIGH
    if score >= 0.35:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def assess_pairwise_risk(source: SocialAgent, target: SocialAgent, config: RiskConfig) -> PairwiseRiskReport:
    """Assess pairwise interaction risk between two agents."""
    source_position = np.asarray(source.position, dtype=float)
    target_position = np.asarray(target.position, dtype=float)
    distance_m = float(np.linalg.norm(target_position - source_position))

    has_source_velocity = source.velocity is not None
    has_target_velocity = target.velocity is not None

    if has_source_velocity and has_target_velocity:
        source_velocity = np.asarray(source.velocity, dtype=float)
        target_velocity = np.asarray(target.velocity, dtype=float)
        ttc = time_to_collision(
            source_position,
            source_velocity,
            target_position,
            target_velocity,
            collision_radius=config.interaction_radius_m,
        )
        approach = closest_point_of_approach(source_position, source_velocity, target_position, target_velocity)
        closest_time = approach.time
        closest_distance = approach.distance
    else:
        ttc = None
        closest_time = 0.0
        closest_distance = distance_m

    score = conflict_score(
        distance_m=distance_m,
        ttc_seconds=ttc,
        closest_approach_distance_m=closest_distance,
        config=config,
    )
    level = _level_from_score(score, config)
    confidence = confidence_score(has_source_velocity, has_target_velocity)
    explanation = (
        f"{level.value} baseline interaction risk; distance={distance_m:.2f} m, "
        f"closest_approach={closest_distance:.2f} m, ttc={ttc}."
    )
    return PairwiseRiskReport(
        source_id=source.agent_id,
        target_id=target.agent_id,
        score=score,
        level=level,
        distance_m=distance_m,
        time_to_intersection=ttc,
        closest_approach_time=closest_time,
        closest_approach_distance_m=closest_distance,
        confidence=confidence,
        explanation=explanation,
    )
