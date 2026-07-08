# SafeCrossAI Pipeline

This document describes the intended end-to-end processing pipeline.

## 1. Perception and Tracking

Status: **Prototype / Planned**

In a deployed intelligent-intersection system, infrastructure sensors would detect and track road users. SafeCrossAI does not currently implement perception models. Future modules should define a common track format independent of the detector.

## 2. Scene Representation

Status: **Implemented scaffold**

A scene contains timestamped agents with positions, velocities, and optional type labels. The current scene representation is intentionally lightweight so it can support toy scenarios, public datasets, and future simulation outputs.

## 3. Trajectory Prediction

Status: **Constant-velocity baseline implemented**

The current baseline extrapolates the last observed displacement vector. This is a minimal reference model and should be included in all future benchmark comparisons.

## 4. Interaction Modelling

Status: **Implemented**

The social-interaction layer computes distances, relative velocities, neighbors, time-to-interaction, closest approach, and radius-based directed interaction graphs.

## 5. Risk Estimation

Status: **Baseline implemented**

The risk module computes deterministic pairwise risk reports from distance, time-to-interaction, and closest-approach features. These scores are interpretable but not calibrated probabilities.

## 6. Evaluation

Status: **Partially implemented**

Trajectory metrics include ADE and FDE. Additional classification, curve, and calibration helpers are available for future labelled risk datasets.

## 7. Visualization

Status: **Prototype implemented**

Visualization utilities render synthetic scenes with agents, velocity arrows, interaction edges, and risk-weighted overlays. The GIF pipeline is intended for reproducible demonstration, not benchmark reporting.
