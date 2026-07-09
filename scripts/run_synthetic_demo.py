#!/usr/bin/env python
"""Run the SafeCrossAI deterministic Synthetic Demo pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from safecrossai.simulation import SyntheticIntersectionSimulator


if __name__ == "__main__":
    summary = SyntheticIntersectionSimulator().run("results")
    print(summary)
