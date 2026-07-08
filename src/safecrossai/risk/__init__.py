"""Risk assessment utilities for SafeCrossAI.

The risk package contains interpretable, baseline risk models built from
geometric interaction features such as distance, time-to-collision, and closest
point of approach. These models are intentionally simple and should be treated
as baselines, not as validated safety predictors.
"""

from .scoring import (
    PairwiseRiskReport,
    RiskConfig,
    RiskLevel,
    assess_pairwise_risk,
    conflict_score,
    confidence_score,
    distance_risk,
    ttc_risk,
)
from .uncertainty import (
    PositionalUncertainty,
    uncertainty_confidence_penalty,
    uncertainty_inflated_distance,
)

__all__ = [
    "PairwiseRiskReport",
    "PositionalUncertainty",
    "RiskConfig",
    "RiskLevel",
    "assess_pairwise_risk",
    "conflict_score",
    "confidence_score",
    "distance_risk",
    "ttc_risk",
    "uncertainty_confidence_penalty",
    "uncertainty_inflated_distance",
]
