from pathlib import Path

import pandas as pd

from safecrossai.datasets.ind.loader import load_ind_tracks_csv


def test_load_ind_tracks_csv_sorts_tracks(tmp_path: Path) -> None:
    csv_path = tmp_path / "tracks.csv"
    pd.DataFrame(
        [
            {"trackId": 2, "frame": 2, "xCenter": 2.0, "yCenter": 0.0},
            {"trackId": 1, "frame": 1, "xCenter": 1.0, "yCenter": 0.0},
            {"trackId": 1, "frame": 0, "xCenter": 0.0, "yCenter": 0.0},
        ]
    ).to_csv(csv_path, index=False)

    data = load_ind_tracks_csv(csv_path)

    assert data["trackId"].tolist() == [1, 1, 2]
    assert data["frame"].tolist() == [0, 1, 2]
