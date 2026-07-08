"""Scenario rendering utilities for SafeCrossAI demos."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from safecrossai.risk import RiskConfig, assess_pairwise_risk
from safecrossai.social import Scene


def _agent_marker(agent_type: str) -> str:
    if agent_type == "pedestrian":
        return "o"
    if agent_type == "cyclist":
        return "s"
    if agent_type == "vehicle":
        return "^"
    return "x"


def render_scene(scene: Scene, ax: plt.Axes, risk_radius: float = 8.0) -> None:
    """Render one scene snapshot with agents and interaction edges."""
    ax.set_title(f"SafeCrossAI synthetic demo · t={scene.timestamp:.1f}s")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_xlim(-6.0, 8.0)
    ax.set_ylim(-4.0, 4.5)
    ax.grid(True, linewidth=0.4, alpha=0.35)
    ax.axhline(0.0, linewidth=1.0, alpha=0.25)
    ax.axvline(0.0, linewidth=1.0, alpha=0.25)

    for agent in scene.agents:
        velocity = (
            np.zeros(2) if agent.velocity is None else np.asarray(agent.velocity, dtype=float)
        )
        ax.scatter(
            agent.position[0],
            agent.position[1],
            marker=_agent_marker(agent.agent_type),
            s=70,
            label=f"{agent.agent_id} ({agent.agent_type})",
        )
        ax.arrow(
            agent.position[0],
            agent.position[1],
            velocity[0] * 0.6,
            velocity[1] * 0.6,
            head_width=0.08,
            length_includes_head=True,
            alpha=0.75,
        )
        ax.text(
            agent.position[0] + 0.12,
            agent.position[1] + 0.12,
            agent.agent_id,
            fontsize=8,
        )

    graph = scene.build_interaction_graph(radius=risk_radius)
    config = RiskConfig()
    agent_by_id = {agent.agent_id: agent for agent in scene.agents}
    for edge in graph.edges:
        source = agent_by_id[edge.source_id]
        target = agent_by_id[edge.target_id]
        report = assess_pairwise_risk(source, target, config=config)
        alpha = 0.15 + 0.75 * report.score
        ax.plot(
            [source.position[0], target.position[0]],
            [source.position[1], target.position[1]],
            linestyle="--",
            linewidth=1.0 + 2.0 * report.score,
            alpha=alpha,
        )

    ax.legend(loc="upper right", fontsize=7, frameon=True)


def render_scenario_frame(scene: Scene, output_path: Path | str) -> Path:
    """Render one scene frame to a PNG file."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 4.5), dpi=150)
    render_scene(scene, ax=ax)
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)
    return output


def save_scenario_gif(
    frame_paths: list[Path],
    output_path: Path | str,
    duration_ms: int = 120,
) -> Path:
    """Assemble PNG frames into a GIF using imageio.

    The function imports imageio lazily so baseline users do not need the GIF
    dependency unless they call this function.
    """
    if not frame_paths:
        raise ValueError("frame_paths must not be empty")
    import imageio.v2 as imageio  # noqa: PLC0415

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    frames = [imageio.imread(path) for path in frame_paths]
    imageio.mimsave(output, frames, duration=duration_ms / 1000.0)
    return output
