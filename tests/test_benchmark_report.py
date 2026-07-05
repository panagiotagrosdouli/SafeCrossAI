from safecrossai.benchmark.comparison import BenchmarkRow
from safecrossai.benchmark.report import benchmark_rows_to_markdown


def test_benchmark_rows_to_markdown_formats_table() -> None:
    rows = [BenchmarkRow(model="constant_velocity", samples=1, mean_ade=0.0, mean_fde=0.0)]

    table = benchmark_rows_to_markdown(rows)

    assert "| Model | Samples | Mean ADE | Mean FDE |" in table
    assert "constant_velocity" in table
