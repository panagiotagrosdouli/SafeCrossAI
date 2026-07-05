from pathlib import Path

import pandas as pd

from safecrossai.datasets.csv_loader import build_samples_from_csv, load_trajectory_csv


def test_load_trajectory_csv_sorts_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "trajectories.csv"
    pd.DataFrame(
        [
            {"scene_id": 1, "agent_id": 1, "frame": 2, "x": 2.0, "y": 0.0},
            {"scene_id": 1, "agent_id": 1, "frame": 1, "x": 1.0, "y": 0.0},
        ]
    ).to_csv(csv_path, index=False)

    data = load_trajectory_csv(csv_path)

    assert data["frame"].tolist() == [1, 2]


def test_build_samples_from_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "trajectories.csv"
    rows = []
    for frame in range(5):
        rows.append(
            {
                "scene_id": 1,
                "agent_id": 7,
                "frame": frame,
                "x": float(frame),
                "y": 0.0,
                "agent_type": "cyclist",
            }
        )
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    samples = build_samples_from_csv(csv_path, observation_steps=3, prediction_steps=2)

    assert len(samples) == 1
    assert samples[0].observed.shape == (3, 2)
    assert samples[0].future.shape == (2, 2)
    assert samples[0].agent_type == "cyclist"
