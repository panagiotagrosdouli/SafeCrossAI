import json
from pathlib import Path

from safecrossai.benchmark.comparison import BenchmarkRow
from safecrossai.benchmark.export import (
    export_benchmark_csv,
    export_benchmark_json,
    export_benchmark_markdown,
)


def test_export_benchmark_csv(tmp_path: Path) -> None:
    path = tmp_path / "results.csv"
    rows = [BenchmarkRow(model="constant_velocity", samples=2, mean_ade=0.1, mean_fde=0.2)]

    export_benchmark_csv(rows, path)

    text = path.read_text(encoding="utf-8")
    assert "model,samples,mean_ade,mean_fde" in text
    assert "constant_velocity" in text


def test_export_benchmark_json(tmp_path: Path) -> None:
    path = tmp_path / "results.json"
    rows = [BenchmarkRow(model="lstm", samples=2, mean_ade=0.3, mean_fde=0.4)]

    export_benchmark_json(rows, path)

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload[0]["model"] == "lstm"
    assert payload[0]["samples"] == 2


def test_export_benchmark_markdown(tmp_path: Path) -> None:
    path = tmp_path / "results.md"
    rows = [BenchmarkRow(model="lstm", samples=2, mean_ade=0.3, mean_fde=0.4)]

    export_benchmark_markdown(rows, path)

    text = path.read_text(encoding="utf-8")
    assert "| Model | Samples | Mean ADE | Mean FDE |" in text
    assert "lstm" in text
