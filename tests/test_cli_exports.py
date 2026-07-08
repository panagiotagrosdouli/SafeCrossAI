from pathlib import Path

from safecrossai.cli import main


def test_toy_benchmark_cli_writes_exports(tmp_path: Path) -> None:
    csv_path = tmp_path / "results.csv"
    json_path = tmp_path / "results.json"
    md_path = tmp_path / "results.md"

    _run_cli(
        [
            "toy-benchmark",
            "--observation-steps",
            "4",
            "--prediction-steps",
            "3",
            "--lstm-epochs",
            "1",
            "--hidden-dim",
            "8",
            "--output-csv",
            str(csv_path),
            "--output-json",
            str(json_path),
            "--output-md",
            str(md_path),
        ]
    )

    assert csv_path.exists()
    assert json_path.exists()
    assert md_path.exists()
    assert "constant_velocity" in csv_path.read_text(encoding="utf-8")
    assert "lstm" in json_path.read_text(encoding="utf-8")
    assert "| Model | Samples | Mean ADE | Mean FDE |" in md_path.read_text(encoding="utf-8")


def _run_cli(args: list[str]) -> None:
    import sys

    original_argv = sys.argv
    try:
        sys.argv = ["safecrossai", *args]
        main()
    finally:
        sys.argv = original_argv
