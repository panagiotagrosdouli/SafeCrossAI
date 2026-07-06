import numpy as np

from safecrossai.benchmark.comparison import compare_with_grouped_train_test_split
from safecrossai.datasets.toy import make_linear_crossing_sample


def test_compare_with_grouped_train_test_split_returns_rows() -> None:
    samples = []
    for index in range(4):
        samples.append(
            make_linear_crossing_sample(
                observation_steps=4,
                prediction_steps=3,
                group_id=f"track_{index}",
            )
        )

    rows = compare_with_grouped_train_test_split(samples, test_fraction=0.5, lstm_epochs=1)

    assert [row.model for row in rows] == ["constant_velocity", "lstm"]
    assert all(np.isfinite(row.mean_ade) for row in rows)
    assert all(np.isfinite(row.mean_fde) for row in rows)
