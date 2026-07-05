"""Tensor conversion utilities for trajectory samples."""

from __future__ import annotations

import numpy as np
import torch

from safecrossai.datasets.toy import TrajectorySample


def samples_to_tensors(samples: list[TrajectorySample]) -> tuple[torch.Tensor, torch.Tensor]:
    """Convert trajectory samples to float32 tensors.

    Returns observed and future tensors with shapes:
    - observed: batch x observation_steps x 2
    - future: batch x prediction_steps x 2
    """
    if not samples:
        raise ValueError("samples must not be empty")

    observed = np.stack([sample.observed for sample in samples]).astype(np.float32)
    future = np.stack([sample.future for sample in samples]).astype(np.float32)

    return torch.from_numpy(observed), torch.from_numpy(future)
