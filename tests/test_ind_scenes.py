from pathlib import Path

import pandas as pd

from safecrossai.datasets.ind.scenes import build_ind_scene_sequences, build_ind_scenes


def test_build_ind_scenes_from_tracks_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "tracks.csv"
    pd.DataFrame(
        [
            {
                "trackId": 2,
                "frame": 0,
                "xCenter": 2.0,
                "yCenter": 0.0,
                "xVelocity": 1.0,
                "yVelocity": 0.0,
                "class": "bicycle",
            },
            {
                "trackId": 1,
                "frame": 0,
                "xCenter": 0.0,
                "yCenter": 0.0,
                "xVelocity": 0.5,
                "yVelocity": 0.0,
                "class": "pedestrian",
            },
            {
                "trackId": 1,
                "frame": 1,
                "xCenter": 0.5,
                "yCenter": 0.0,
                "xVelocity": 0.5,
                "yVelocity": 0.0,
                "class": "pedestrian",
            },
        ]
    ).to_csv(csv_path, index=False)

    scenes = build_ind_scenes(csv_path)

    assert len(scenes) == 2
    assert scenes[0].scene_id == "frame:0"
    assert scenes[0].agent_ids() == ["1", "2"]
    assert scenes[0].agents[0].agent_type == "pedestrian"
    assert scenes[0].agents[0].velocity is not None


def test_build_ind_scenes_filters_classes(tmp_path: Path) -> None:
    csv_path = tmp_path / "tracks.csv"
    pd.DataFrame(
        [
            {"trackId": 1, "frame": 0, "xCenter": 0.0, "yCenter": 0.0, "class": "pedestrian"},
            {"trackId": 2, "frame": 0, "xCenter": 2.0, "yCenter": 0.0, "class": "car"},
        ]
    ).to_csv(csv_path, index=False)

    scenes = build_ind_scenes(csv_path, classes={"pedestrian"})

    assert len(scenes) == 1
    assert scenes[0].agent_ids() == ["1"]


def test_build_ind_scene_sequences(tmp_path: Path) -> None:
    csv_path = tmp_path / "tracks.csv"
    rows = []
    for frame in range(4):
        rows.append(
            {
                "trackId": 1,
                "frame": frame,
                "xCenter": float(frame),
                "yCenter": 0.0,
                "class": "pedestrian",
            }
        )
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    sequences = build_ind_scene_sequences(
        csv_path,
        sequence_length=2,
        stride=2,
        classes={"pedestrian"},
    )

    assert len(sequences) == 2
    assert sequences[0].start_time == 0.0
    assert sequences[1].start_time == 2.0
    assert sequences[0].agent_ids() == ["1"]
