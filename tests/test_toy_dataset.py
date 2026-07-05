from safecrossai.datasets.toy import make_linear_crossing_sample


def test_toy_crossing_sample_shapes() -> None:
    sample = make_linear_crossing_sample(observation_steps=8, prediction_steps=12)

    assert sample.observed.shape == (8, 2)
    assert sample.future.shape == (12, 2)
    assert sample.agent_type == "pedestrian"
