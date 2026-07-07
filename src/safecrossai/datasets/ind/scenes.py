"""Build unified scenes from inD-style tracks CSV files."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from safecrossai.datasets.ind.loader import load_ind_tracks_csv
from safecrossai.social import Scene, SocialAgent, make_scene


def build_ind_scenes(
    path: str | Path,
    classes: set[str] | None = None,
) -> list[Scene]:
    """Build frame-level scenes from an inD-style tracks CSV file.

    Each frame becomes one :class:`Scene`. Agent positions are read from
    ``xCenter`` and ``yCenter``. Velocities are read from ``xVelocity`` and
    ``yVelocity`` when available.
    """
    data = load_ind_tracks_csv(path)
    scenes: list[Scene] = []

    for frame, frame_data in data.groupby("frame"):
        agents: list[SocialAgent] = []
        for _, row in frame_data.sort_values("trackId").iterrows():
            agent_type = str(row["class"]) if "class" in frame_data.columns else "unknown"
            if classes is not None and agent_type not in classes:
                continue

            velocity = None
            if "xVelocity" in frame_data.columns and "yVelocity" in frame_data.columns:
                velocity = np.array([float(row["xVelocity"]), float(row["yVelocity"])])

            agents.append(
                SocialAgent(
                    agent_id=str(row["trackId"]),
                    position=np.array([float(row["xCenter"]), float(row["yCenter"])]),
                    velocity=velocity,
                    agent_type=agent_type,
                )
            )

        if agents:
            scenes.append(
                make_scene(
                    scene_id=f"frame:{frame}",
                    timestamp=float(frame),
                    agents=agents,
                    metadata={"source": "inD", "frame": int(frame)},
                )
            )

    return scenes
