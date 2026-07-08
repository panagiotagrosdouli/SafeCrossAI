from dataclasses import dataclass

from safecrossai.datasets.splitting import grouped_train_test_split_samples, train_test_split_samples


@dataclass(frozen=True)
class Item:
    value: int
    group: str


def test_train_test_split_samples_is_deterministic() -> None:
    samples = list(range(10))

    first = train_test_split_samples(samples, test_fraction=0.3, seed=7)
    second = train_test_split_samples(samples, test_fraction=0.3, seed=7)

    assert first == second
    assert len(first.train) == 7
    assert len(first.test) == 3
    assert set(first.train).isdisjoint(first.test)


def test_grouped_train_test_split_keeps_groups_separate() -> None:
    samples = [
        Item(value=1, group="a"),
        Item(value=2, group="a"),
        Item(value=3, group="b"),
        Item(value=4, group="b"),
        Item(value=5, group="c"),
        Item(value=6, group="c"),
    ]

    split = grouped_train_test_split_samples(
        samples,
        group_fn=lambda item: item.group,
        seed=1,
    )

    train_groups = {item.group for item in split.train}
    test_groups = {item.group for item in split.test}
    assert train_groups.isdisjoint(test_groups)
    assert len(split.train) + len(split.test) == len(samples)
