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


def _run_cli(args: list[str]) -> None:
    import sys

    original_argv = sys.argv
    try:
        sys.argv = ["safecrossai", *args]
        main()
    finally:
        sys.argv = original_argv
