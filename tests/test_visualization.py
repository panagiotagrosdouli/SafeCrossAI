from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from safecrossai.visualization.trajectories import plot_trajectory_prediction


def test_plot_trajectory_prediction_saves_file(tmp_path: Path) -> None:
    observed = np.array([[0.0, 0.0], [1.0, 0.5], [2.0, 1.0]])
    future = np.array([[3.0, 1.5], [4.0, 2.0]])
    prediction = np.array([[3.0, 1.4], [4.1, 2.1]])
    save_path = tmp_path / "trajectory.png"

    figure = plot_trajectory_prediction(observed, future, prediction, save_path=save_path)

    assert save_path.exists()
    assert figure.axes
    plt.close(figure)
