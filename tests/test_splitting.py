from safecrossai.datasets.splitting import train_test_split_samples


def test_train_test_split_samples_is_deterministic() -> None:
    samples = list(range(10))

    first = train_test_split_samples(samples, test_fraction=0.3, seed=7)
    second = train_test_split_samples(samples, test_fraction=0.3, seed=7)

    assert first == second
    assert len(first.train) == 7
    assert len(first.test) == 3
    assert set(first.train).isdisjoint(first.test)
