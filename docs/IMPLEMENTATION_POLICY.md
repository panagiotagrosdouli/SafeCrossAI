# Implementation Policy

SafeCrossAI follows a research-first implementation policy. The repository must support scientific progress without overstating maturity.

## Scientific Motivation

Safety-critical intelligent-infrastructure software must distinguish between implemented evidence, engineering scaffolds, and future hypotheses. A clean policy prevents accidental overclaiming and makes the project easier to evaluate by supervisors, reviewers, and collaborators.

## Engineering Motivation

Each module should have a narrow responsibility, typed interfaces, unit tests, and documented limitations. Prototype code is acceptable when it is explicitly labelled and when the production path is clear.

## Change Requirements

Every substantial change should document:

1. scientific motivation;
2. engineering motivation;
3. expected benefit;
4. potential drawbacks;
5. implementation complexity;
6. validation strategy.

## Prototype Criteria

A feature must be marked **Prototype** when any of the following is true:

- it has not been validated on a public or documented dataset;
- it has no unit or regression tests;
- it depends on unimplemented data loaders, perception models, or simulators;
- it provides an interface but not a complete algorithm;
- it is meant for demonstration rather than benchmark reporting.

## Reporting Policy

SafeCrossAI must not report benchmark numbers unless they are produced by a reproducible script committed to the repository. Synthetic demos may be used for visualization and smoke testing, but they must not be presented as real-world evidence.

## Current Baseline Status

Implemented baseline modules include constant-velocity prediction, linear least-squares prediction, pairwise geometric interaction utilities, deterministic TTC/CPA analysis, interpretable baseline risk scoring, and basic evaluation metrics. Learning-based prediction, infrastructure perception, calibrated uncertainty, public dataset loaders, and digital-twin simulation remain **Prototype** or **Planned** until implemented and validated.
