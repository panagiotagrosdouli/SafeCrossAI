"""Deterministic Synthetic Demo intelligent-intersection simulator.

The module produces synthetic CSV/JSON artefacts for software validation and
research communication. Outputs are labelled Synthetic Demo and must not be
reported as real-world benchmark evidence.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path

import numpy as np
import pandas as pd


class AgentType(str, Enum):
    """Supported road-user classes."""

    PEDESTRIAN = "PEDESTRIAN"
    CYCLIST = "CYCLIST"
    VEHICLE = "VEHICLE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class AgentState:
    """Timestamped 2D kinematic state."""

    agent_id: str
    agent_type: AgentType
    t: float
    x: float
    y: float
    vx: float
    vy: float
    observed: bool
    synthetic_demo: bool = True

    def row(self) -> dict[str, object]:
        data = asdict(self)
        data["agent_type"] = self.agent_type.value
        return data


@dataclass(frozen=True)
class LinearAgent:
    """Constant-velocity synthetic road user."""

    agent_id: str
    agent_type: AgentType
    x0: float
    y0: float
    vx: float
    vy: float

    def state_at(self, t: float, observed: bool) -> AgentState:
        return AgentState(
            self.agent_id,
            self.agent_type,
            t,
            self.x0 + self.vx * t,
            self.y0 + self.vy * t,
            self.vx,
            self.vy,
            observed,
        )


def _ttc(p1: np.ndarray, v1: np.ndarray, p2: np.ndarray, v2: np.ndarray, radius: float = 1.5) -> float:
    rel_p = p2 - p1
    rel_v = v2 - v1
    a = float(rel_v @ rel_v)
    b = 2.0 * float(rel_p @ rel_v)
    c = float(rel_p @ rel_p) - radius**2
    if a < 1e-9:
        return math.inf
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        return math.inf
    roots = [(-b - math.sqrt(disc)) / (2.0 * a), (-b + math.sqrt(disc)) / (2.0 * a)]
    positive = [root for root in roots if root >= 0.0]
    return min(positive) if positive else math.inf


def _cpa(p1: np.ndarray, v1: np.ndarray, p2: np.ndarray, v2: np.ndarray) -> tuple[float, float]:
    rel_p = p2 - p1
    rel_v = v2 - v1
    denom = float(rel_v @ rel_v)
    t_star = 0.0 if denom < 1e-9 else max(0.0, -float(rel_p @ rel_v) / denom)
    return t_star, float(np.linalg.norm(rel_p + rel_v * t_star))


def _predict(observed: pd.DataFrame, future_steps: int, dt: float) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for agent_id, group in observed.sort_values("t").groupby("agent_id"):
        last = group.iloc[-1]
        t0 = float(last.t)
        for step in range(1, future_steps + 1):
            rows.append(
                {
                    "agent_id": agent_id,
                    "agent_type": last.agent_type,
                    "t": t0 + step * dt,
                    "step": step,
                    "x": float(last.x + last.vx * step * dt),
                    "y": float(last.y + last.vy * step * dt),
                    "method": "constant_velocity",
                    "synthetic_demo": True,
                }
            )
    return pd.DataFrame(rows)


def _edges(observed: pd.DataFrame) -> pd.DataFrame:
    latest = observed.sort_values("t").groupby("agent_id").tail(1)
    records = latest.to_dict("records")
    rows: list[dict[str, object]] = []
    for source in records:
        for target in records:
            if source["agent_id"] == target["agent_id"]:
                continue
            p1 = np.array([source["x"], source["y"]], dtype=float)
            p2 = np.array([target["x"], target["y"]], dtype=float)
            v1 = np.array([source["vx"], source["vy"]], dtype=float)
            v2 = np.array([target["vx"], target["vy"]], dtype=float)
            distance = float(np.linalg.norm(p2 - p1))
            if distance > 30.0:
                continue
            ttc = _ttc(p1, v1, p2, v2)
            time_to_cpa, cpa_distance = _cpa(p1, v1, p2, v2)
            relative_speed = float(np.linalg.norm(v2 - v1))
            ttc_term = 0.0 if math.isinf(ttc) else max(0.0, 1.0 - ttc / 6.0)
            score = min(
                1.0,
                0.30 * max(0.0, 1.0 - distance / 25.0)
                + 0.20 * min(1.0, relative_speed / 10.0)
                + 0.30 * ttc_term
                + 0.20 * max(0.0, 1.0 - cpa_distance / 8.0),
            )
            level = "CRITICAL" if score >= 0.75 else "HIGH" if score >= 0.55 else "MEDIUM" if score >= 0.30 else "LOW"
            rows.append(
                {
                    "source_agent": source["agent_id"],
                    "target_agent": target["agent_id"],
                    "distance": distance,
                    "relative_speed": relative_speed,
                    "ttc": ttc,
                    "time_to_cpa": time_to_cpa,
                    "closest_approach_distance": cpa_distance,
                    "risk_score": score,
                    "risk_level": level,
                    "edge_status": "ACTIVE" if score >= 0.30 else "WEAK",
                    "recommended_warning_flag": level in {"HIGH", "CRITICAL"},
                    "explanation": f"{level}: Synthetic Demo TTC/CPA risk estimate.",
                    "synthetic_demo": True,
                }
            )
    return pd.DataFrame(rows)


def _metrics(predicted: pd.DataFrame, ground_truth: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for agent_id, pred in predicted.groupby("agent_id"):
        gt = ground_truth[ground_truth.agent_id == agent_id].sort_values("step")
        pred = pred.sort_values("step")
        diff = pred[["x", "y"]].to_numpy() - gt[["x", "y"]].to_numpy()
        distances = np.linalg.norm(diff, axis=1)
        rows.append(
            {
                "agent_id": agent_id,
                "ADE": float(distances.mean()),
                "FDE": float(distances[-1]),
                "miss_rate_at_2m": float(distances[-1] > 2.0),
                "synthetic_demo": True,
            }
        )
    return pd.DataFrame(rows)


class SyntheticIntersectionSimulator:
    """Run a deterministic synthetic intelligent-intersection scenario."""

    def __init__(self, seed: int = 7, dt: float = 0.5, observed_steps: int = 8, future_steps: int = 12):
        self.seed = seed
        self.dt = dt
        self.observed_steps = observed_steps
        self.future_steps = future_steps

    def agents(self) -> list[LinearAgent]:
        return [
            LinearAgent("ped_1", AgentType.PEDESTRIAN, -1.5, -9.0, 0.0, 1.35),
            LinearAgent("cyc_1", AgentType.CYCLIST, 11.0, -11.0, -1.25, 1.25),
            LinearAgent("veh_1", AgentType.VEHICLE, -20.0, 0.0, 4.0, 0.0),
            LinearAgent("veh_2", AgentType.VEHICLE, 19.0, 3.0, -2.5, 0.0),
        ]

    def trajectories(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        observed: list[dict[str, object]] = []
        future: list[dict[str, object]] = []
        for agent in self.agents():
            for idx in range(self.observed_steps):
                observed.append(agent.state_at(idx * self.dt, True).row())
            t0 = (self.observed_steps - 1) * self.dt
            for step in range(1, self.future_steps + 1):
                row = agent.state_at(t0 + step * self.dt, False).row()
                row["step"] = step
                future.append(row)
        return pd.DataFrame(observed), pd.DataFrame(future)

    def run(self, output_dir: str | Path = "results") -> dict[str, object]:
        output = Path(output_dir)
        (output / "metrics").mkdir(parents=True, exist_ok=True)
        (output / "reports").mkdir(parents=True, exist_ok=True)
        observed, ground_truth = self.trajectories()
        predicted = _predict(observed, self.future_steps, self.dt)
        edges = _edges(observed)
        conflicts = edges[edges.risk_score >= 0.55].copy()
        conflicts["event_type"] = "SAFETY_CRITICAL_INTERACTION"
        metrics = _metrics(predicted, ground_truth)
        summary = {
            "label": "Synthetic Demo",
            "seed": self.seed,
            "agents": int(observed.agent_id.nunique()),
            "conflicts_detected": int(len(conflicts)),
            "mean_ADE": float(metrics.ADE.mean()),
            "mean_FDE": float(metrics.FDE.mean()),
            "implemented": "synthetic simulation, prediction, interaction edges, TTC/CPA risk, metrics",
            "prototype": "dataset loaders and uncertainty calibration",
            "planned": "learning-based trajectory prediction and GNN social modelling",
        }
        outputs = {
            "observed_trajectories.csv": observed,
            "ground_truth_future.csv": ground_truth,
            "predicted_trajectories.csv": predicted,
            "agent_states.csv": pd.concat([observed, ground_truth], ignore_index=True),
            "interaction_edges.csv": edges,
            "risk_scores.csv": edges,
            "conflict_events.csv": conflicts,
        }
        for name, frame in outputs.items():
            frame.to_csv(output / name, index=False)
        metrics.to_csv(output / "metrics" / "metrics.csv", index=False)
        (output / "metrics" / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        (output / "scene_metadata.json").write_text(
            json.dumps(
                {
                    "label": "Synthetic Demo",
                    "geometry": "2D four-way intersection with crosswalks, lanes, and central conflict zone",
                    "occlusion": "placeholder",
                    "sensor_noise": "placeholder",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        (output / "simulation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        (output / "reports" / "synthetic_demo_report.md").write_text(
            "# Synthetic Demo Report\n\nAll reported numbers are produced from deterministic synthetic trajectories.\n",
            encoding="utf-8",
        )
        return summary
