from pathlib import Path

import pandas as pd

from safecrossai.datasets.ind.samples import build_ind_samples


def test_build_ind_samples_from_tracks_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "tracks.csv"
    rows = []
    for frame in range(5):
        rows.append(
            {
                "trackId": 10,
                "frame": frame,
                "xCenter": float(frame),
                "yCenter": 0.5 * frame,
                "class": "pedestrian",
            }
        )
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    samples = build_ind_samples(csv_path, observation_steps=3, prediction_steps=2)

    assert len(samples) == 1
    assert samples[0].observed.shape == (3, 2)
    assert samples[0].future.shape == (2, 2)
    assert samples[0].agent_type == "pedestrian"


def test_build_ind_samples_filters_classes(tmp_path: Path) -> None:
    csv_path = tmp_path / "tracks.csv"
    rows = []
    for track_id, agent_class in [(1, "pedestrian"), (2, "car")]:
        for frame in range(5):
            rows.append(
                {
                    "trackId": track_id,
                    "frame": frame,
                    "xCenter": float(frame),
                    "yCenter": 0.0,
                    "class": agent_class,
                }
            )
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    samples = build_ind_samples(
        csv_path,
        observation_steps=3,
        prediction_steps=2,
        classes={"pedestrian"},
    )

    assert len(samples) == 1
    assert samples[0].agent_type == "pedestrian"
