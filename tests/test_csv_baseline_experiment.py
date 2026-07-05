from pathlib import Path

import pandas as pd

from safecrossai.experiments.csv_baseline_experiment import run_csv_constant_velocity_baseline


def test_csv_baseline_experiment_runs(tmp_path: Path) -> None:
    csv_path = tmp_path / "trajectories.csv"
    rows = []
    for frame in range(6):
        rows.append(
            {
                "scene_id": 1,
                "agent_id": 1,
                "frame": frame,
                "x": float(frame),
                "y": 0.0,
                "agent_type": "pedestrian",
            }
        )
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    result = run_csv_constant_velocity_baseline(
        csv_path,
        observation_steps=3,
        prediction_steps=2,
    )

    assert result.samples == 2
    assert result.mean_ade == 0.0
    assert result.mean_fde == 0.0
