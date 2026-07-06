"""Dataset splitting utilities."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import random
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class SampleSplit(Generic[T]):
    """Train/test split for trajectory samples."""

    train: list[T]
    test: list[T]


def train_test_split_samples(
    samples: list[T],
    test_fraction: float = 0.2,
    seed: int = 42,
) -> SampleSplit[T]:
    """Split samples into deterministic train and test partitions."""
    if not samples:
        raise ValueError("samples must not be empty")
    if not 0.0 < test_fraction < 1.0:
        raise ValueError("test_fraction must be between 0 and 1")
    if len(samples) < 2:
        raise ValueError("at least two samples are required for a split")

    indices = list(range(len(samples)))
    rng = random.Random(seed)
    rng.shuffle(indices)

    test_size = max(1, int(round(len(samples) * test_fraction)))
    test_indices = set(indices[:test_size])

    train = [sample for index, sample in enumerate(samples) if index not in test_indices]
    test = [sample for index, sample in enumerate(samples) if index in test_indices]

    if not train or not test:
        raise ValueError("split produced an empty train or test partition")

    return SampleSplit(train=train, test=test)


def grouped_train_test_split_samples(
    samples: list[T],
    group_fn: Callable[[T], str | None],
    test_fraction: float = 0.2,
    seed: int = 42,
) -> SampleSplit[T]:
    """Split samples by group so each group appears only in train or test."""
    if not samples:
        raise ValueError("samples must not be empty")
    if not 0.0 < test_fraction < 1.0:
        raise ValueError("test_fraction must be between 0 and 1")

    groups: dict[str, list[T]] = {}
    for index, sample in enumerate(samples):
        group = group_fn(sample)
        if group is None:
            group = f"__ungrouped_{index}"
        groups.setdefault(group, []).append(sample)

    if len(groups) < 2:
        raise ValueError("at least two groups are required for a grouped split")

    group_ids = list(groups)
    rng = random.Random(seed)
    rng.shuffle(group_ids)

    test_group_count = max(1, int(round(len(group_ids) * test_fraction)))
    test_groups = set(group_ids[:test_group_count])

    train: list[T] = []
    test: list[T] = []
    for group_id, group_samples in groups.items():
        if group_id in test_groups:
            test.extend(group_samples)
        else:
            train.extend(group_samples)

    if not train or not test:
        raise ValueError("split produced an empty train or test partition")

    return SampleSplit(train=train, test=test)
