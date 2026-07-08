#!/usr/bin/env python
"""Generate a reproducible SafeCrossAI demo GIF and optional MP4.

The demo uses a deterministic synthetic scenario. It is intended for pipeline
communication and software smoke testing, not for benchmark claims.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from safecrossai.datasets.demo import make_intersection_demo_scenario
from safecrossai.visualization import render_scenario_frame, save_scenario_gif


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames-dir", type=Path, default=Path("assets/demo_frames"))
    parser.add_argument("--output", type=Path, default=Path("assets/demo.gif"))
    parser.add_argument("--mp4", type=Path, default=Path("assets/demo.mp4"))
    parser.add_argument("--num-steps", type=int, default=30)
    parser.add_argument("--dt", type=float, default=0.2)
    parser.add_argument("--duration-ms", type=int, default=120)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenario = make_intersection_demo_scenario(num_steps=args.num_steps, dt=args.dt)
    args.frames_dir.mkdir(parents=True, exist_ok=True)

    frame_paths = []
    for index, scene in enumerate(scenario.scenes):
        frame_path = args.frames_dir / f"frame_{index:04d}.png"
        frame_paths.append(render_scenario_frame(scene, frame_path))

    gif_path = save_scenario_gif(frame_paths, args.output, duration_ms=args.duration_ms)
    print(f"Saved GIF: {gif_path}")

    try:
        import imageio.v2 as imageio

        frames = [imageio.imread(path) for path in frame_paths]
        imageio.mimsave(args.mp4, frames, fps=max(1, round(1000 / args.duration_ms)))
        print(f"Saved MP4: {args.mp4}")
    except Exception as exc:  # pragma: no cover - optional codec support varies by environment
        print(f"MP4 export skipped: {exc}")


if __name__ == "__main__":
    main()
