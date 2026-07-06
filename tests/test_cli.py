from pathlib import Path

import pandas as pd

from safecrossai.cli import main


def test_toy_baseline_cli(capsys) -> None:
    main_args = ["toy-baseline"]
    _run_cli(main_args)

    output = capsys.readouterr().out
    assert "samples: 1" in output
    assert "mean_ade:" in output
    assert "mean_fde:" in output


def test_csv_baseline_cli(tmp_path: Path, capsys) -> None:
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

    _run_cli([
        "csv-baseline",
        str(csv_path),
        "--observation-steps",
        "3",
        "--prediction-steps",
        "2",
    ])

    output = capsys.readouterr().out
    assert "samples: 2" in output
    assert "mean_ade:" in output
    assert "mean_fde:" in output


def test_toy_benchmark_cli(capsys) -> None:
    _run_cli([
        "toy-benchmark",
        "--observation-steps",
        "4",
        "--prediction-steps",
        "3",
        "--lstm-epochs",
        "1",
        "--hidden-dim",
        "8",
    ])

    output = capsys.readouterr().out
    assert "| Model | Samples | Mean ADE | Mean FDE |" in output
    assert "constant_velocity" in output
    assert "lstm" in output


def test_ind_benchmark_cli(tmp_path: Path, capsys) -> None:
    csv_path = tmp_path / "tracks.csv"
    rows = []
    for frame in range(5):
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

    _run_cli([
        "ind-benchmark",
        str(csv_path),
        "--observation-steps",
        "3",
        "--prediction-steps",
        "2",
        "--lstm-epochs",
        "1",
        "--hidden-dim",
        "8",
    ])

    output = capsys.readouterr().out
    assert "| Model | Samples | Mean ADE | Mean FDE |" in output
    assert "constant_velocity" in output
    assert "lstm" in output


def test_ind_train_test_benchmark_cli(tmp_path: Path, capsys) -> None:
    csv_path = tmp_path / "tracks.csv"
    rows = []
    for track_id in range(4):
        for frame in range(5):
            rows.append(
                {
                    "trackId": track_id,
                    "frame": frame,
                    "xCenter": float(frame),
                    "yCenter": 0.0,
                    "class": "pedestrian",
                }
            )
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    _run_cli([
        "ind-benchmark",
        str(csv_path),
        "--observation-steps",
        "3",
        "--prediction-steps",
        "2",
        "--train-test",
        "--test-fraction",
        "0.5",
        "--lstm-epochs",
        "1",
        "--hidden-dim",
        "8",
    ])

    output = capsys.readouterr().out
    assert "| Model | Samples | Mean ADE | Mean FDE |" in output
    assert "constant_velocity" in output
    assert "lstm" in output


def _run_cli(args: list[str]) -> None:
    import sys

    original_argv = sys.argv
    try:
        sys.argv = ["safecrossai", *args]
        main()
    finally:
        sys.argv = original_argv
