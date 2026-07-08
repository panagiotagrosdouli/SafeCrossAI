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
- GIF assembly;
- deterministic generation of architecture, pipeline, dependency, prediction, interaction, risk, ROC, precision-recall, confusion-matrix, and calibration figures.

## Demo GIF

Generate the demo with:

```bash
python scripts/make_demo_gif.py --output assets/demo.gif --mp4 assets/demo.mp4
```

The GIF is generated from a deterministic synthetic scenario. It should be labelled as a synthetic demo wherever it is shown.

## Scientific Figures

Generate the explanatory figure set with:

```bash
python scripts/generate_figures.py --output-dir assets
```

The script writes:

```text
assets/architecture_diagram.png
assets/pipeline_diagram.png
assets/module_dependency_graph.png
assets/trajectory_prediction.png
assets/interaction_graph.png
assets/risk_overlay.png
assets/confusion_matrix.png
assets/roc_curve.png
assets/precision_recall_curve.png
assets/calibration_curve.png
```

These figures are deterministic communication artifacts. The evaluation curves use synthetic labels and scores for visualization only; they are not benchmark evidence.

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
- calibration and reliability diagrams from real validation data;
- publication-ready figure templates.
