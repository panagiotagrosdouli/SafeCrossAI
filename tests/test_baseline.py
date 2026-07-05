import numpy as np

from safecrossai.evaluation.metrics import average_displacement_error, final_displacement_error
from safecrossai.prediction.baseline import constant_velocity_predict
from safecrossai.risk.safety_metrics import minimum_distance, simple_conflict_score


def test_constant_velocity_predicts_linear_motion() -> None:
    history = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]])
    prediction = constant_velocity_predict(history, horizon=3)
    expected = np.array([[3.0, 3.0], [4.0, 4.0], [5.0, 5.0]])
    np.testing.assert_allclose(prediction, expected)


def test_trajectory_metrics_are_zero_for_identical_paths() -> None:
    trajectory = np.array([[0.0, 0.0], [1.0, 1.0]])
    assert average_displacement_error(trajectory, trajectory) == 0.0
    assert final_displacement_error(trajectory, trajectory) == 0.0


def test_safety_metrics_detect_close_interaction() -> None:
    agent_a = np.array([[0.0, 0.0], [1.0, 1.0]])
    agent_b = np.array([[0.0, 1.0], [1.0, 1.2]])
    assert minimum_distance(agent_a, agent_b) < 1.0
    assert simple_conflict_score(agent_a, agent_b, safety_distance=2.0) > 0.0
