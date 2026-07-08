from pathlib import Path

import pandas as pd

from safecrossai.cli import main


def test_ind_scene_summary_cli(tmp_path: Path, capsys) -> None:
    csv_path = tmp_path / "tracks.csv"
    pd.DataFrame(
        [
            {
                "trackId": 1,
                "frame": 0,
                "xCenter": 0.0,
                "yCenter": 0.0,
                "class": "pedestrian",
            },
            {
                "trackId": 2,
                "frame": 0,
                "xCenter": 1.0,
                "yCenter": 0.0,
                "class": "bicycle",
            },
            {
                "trackId": 1,
                "frame": 1,
                "xCenter": 0.5,
                "yCenter": 0.0,
                "class": "pedestrian",
            },
            {
                "trackId": 1,
                "frame": 2,
                "xCenter": 1.0,
                "yCenter": 0.0,
                "class": "pedestrian",
            },
        ]
    ).to_csv(csv_path, index=False)

    _run_cli(
        [
            "ind-scene-summary",
            str(csv_path),
            "--radius",
            "2.0",
            "--sequence-length",
            "2",
            "--stride",
            "1",
            "--classes",
            "pedestrian",
            "bicycle",
        ]
    )

    output = capsys.readouterr().out
    assert "scenes: 3" in output
    assert "agents: 4" in output
    assert "interaction_edges: 2" in output
    assert "scene_sequences: 2" in output
    assert "sequence_length: 2" in output
    assert "sequence_stride: 1" in output


def _run_cli(args: list[str]) -> None:
    import sys

    original_argv = sys.argv
    try:
        sys.argv = ["safecrossai", *args]
        main()
    finally:
        sys.argv = original_argv
