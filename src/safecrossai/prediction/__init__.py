"""Trajectory prediction baselines and model interfaces."""

from safecrossai.prediction.baseline import constant_velocity_predict
from safecrossai.prediction.linear import linear_regression_predict

__all__ = ["constant_velocity_predict", "linear_regression_predict"]
