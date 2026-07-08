# Evaluation Protocol

This document defines how SafeCrossAI experiments should be evaluated. It prevents overclaiming by requiring each result to state dataset, split, horizon, baseline, seed, and metric definitions.

## Reporting Rules

Every reported result must include:

- dataset name and version;
- whether the data are synthetic or real;
- train/validation/test split;
- observation horizon;
- prediction horizon;
- sampling frequency;
- number of scenes and agents;
- random seeds;
- baseline model;
- metric definitions;
- commit hash or release tag.

Synthetic demos must be labelled as synthetic demos and must not be presented as real benchmark evidence.

## Trajectory Prediction Metrics

### Average Displacement Error

For predicted trajectory \(\hat{y}_{1:T}\) and ground truth \(y_{1:T}\):

\[
ADE = \frac{1}{T}\sum_{t=1}^{T}\lVert \hat{y}_t - y_t \rVert_2
\]

### Final Displacement Error

\[
FDE = \lVert \hat{y}_T - y_T \rVert_2
\]

### Miss Rate

A prediction is a miss if its final displacement error exceeds a threshold \(\tau\):

\[
MR = \frac{1}{N}\sum_i \mathbb{1}[FDE_i > \tau]
\]

The threshold must be reported.

## Interaction-Risk Metrics

For binary conflict labels, report:

- precision;
- recall;
- F1;
- confusion matrix;
- ROC curve;
- precision-recall curve;
- expected calibration error when probabilities are used.

## Uncertainty-Aware Risk Evaluation

SafeCrossAI now includes a **Prototype** uncertainty interface based on 2D covariance matrices. This is not a calibrated uncertainty model. It is an engineering scaffold for future probabilistic predictors.

Future uncertainty experiments must report:

- the source of uncertainty estimates;
- whether covariances are predicted, fitted, or assumed;
- calibration metrics such as reliability diagrams and expected calibration error;
- negative log-likelihood when probabilistic ground truth evaluation is appropriate;
- risk-score changes under uncertainty inflation;
- sensitivity to the chosen sigma scale.

A risk score must not be interpreted as a probability unless calibration is demonstrated on held-out labelled data.

## Calibration

Risk scores should not be interpreted as probabilities unless calibration is evaluated. Calibration experiments should report reliability diagrams and expected calibration error.

## Baselines

Minimum baselines:

1. constant-position baseline;
2. constant-velocity baseline;
3. linear model baseline;
4. interaction-aware baseline;
5. learning-based model only after the baseline protocol is stable.

## Dataset Protocol

Until public dataset loaders are implemented, only synthetic smoke tests are supported. Future public-dataset experiments should use official splits when available.

Candidate datasets:

- inD;
- rounD;
- highD;
- INTERACTION;
- Argoverse 2 Motion Forecasting;
- Waymo Open Motion Dataset;
- nuScenes prediction-related data;
- V2X and infrastructure-perception datasets.

No benchmark table should be committed until reproducible scripts produce it.
