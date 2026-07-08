# Visualization

SafeCrossAI visualizations are designed for scientific communication, not decorative graphics.

## Goals

Visualization should help explain:

- observed road-user motion;
- predicted future trajectories;
- interaction graph structure;
- time-to-interaction and closest-approach reasoning;
- interpretable risk overlays;
- evaluation results such as confusion matrices and calibration curves.

## Current Capabilities

Implemented / prototype:

- trajectory prediction plots;
- scene rendering;
- agent markers by type;
- velocity arrows;
- interaction edges;
- risk-weighted edge overlays;
- PNG frame export;
- GIF assembly.

## Demo GIF

Generate the demo with:

```bash
python scripts/make_demo_gif.py --output assets/demo.gif --mp4 assets/demo.mp4
```

The GIF is generated from a deterministic synthetic scenario. It should be labelled as a synthetic demo wherever it is shown.

## Figure Policy

Figures intended for papers should:

- state whether data are synthetic or real;
- avoid unexplained colors or legends;
- include units on axes;
- be reproducible from scripts;
- be saved under `assets/` or `results/figures/`;
- never imply benchmark performance without evaluation protocol.

## Future Extensions

- predicted trajectory fan plots;
- uncertainty ellipses;
- interaction graph overlay on map geometry;
- risk timeline plots;
- calibration and reliability diagrams;
- publication-ready figure templates.
