#!/usr/bin/env python
"""Run the complete SafeCrossAI Synthetic Demo transformation pipeline."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

COMMANDS = [
    ["scripts/run_synthetic_demo.py"],
    ["scripts/generate_figures.py", "--output-dir", "results/figures"],
    [
        "scripts/make_demo_gif.py",
        "--frames-dir",
        "results/videos/frames",
        "--output",
        "results/videos/safecrossai_demo.gif",
        "--mp4",
        "results/videos/safecrossai_demo.mp4",
    ],
    ["scripts/run_benchmarks.py"],
]


def main() -> None:
    for command in COMMANDS:
        subprocess.check_call([sys.executable, *command])
    Path("assets/figures").mkdir(parents=True, exist_ok=True)
    Path("assets/gifs").mkdir(parents=True, exist_ok=True)
    Path("assets/videos").mkdir(parents=True, exist_ok=True)
    for figure in Path("results/figures").glob("*.png"):
        shutil.copy2(figure, Path("assets/figures") / figure.name)
    if Path("results/videos/safecrossai_demo.gif").exists():
        shutil.copy2("results/videos/safecrossai_demo.gif", "assets/gifs/demo.gif")
    if Path("results/videos/safecrossai_demo.mp4").exists():
        shutil.copy2("results/videos/safecrossai_demo.mp4", "assets/videos/demo.mp4")
    print(
        "SafeCrossAI complete: Synthetic Demo metrics, figures, demo.gif, demo.mp4, and benchmark report generated from code."
    )


if __name__ == "__main__":
    main()
