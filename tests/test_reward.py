from titus_player.reward import RewardTracker


def test_new_hash_gets_reward(tmp_path):
    image = tmp_path / "screen.png"
    image.write_bytes(b"screen A")

    tracker = RewardTracker()

    assert tracker.evaluate(image) == 1


def test_repeated_hash_gets_no_reward(tmp_path):
    image = tmp_path / "screen.png"
    image.write_bytes(b"screen A")

    tracker = RewardTracker()

    assert tracker.evaluate(image) == 1
    assert tracker.evaluate(image) == 0


def test_different_hash_gets_reward(tmp_path):
    first = tmp_path / "first.png"
    second = tmp_path / "second.png"

    first.write_bytes(b"screen A")
    second.write_bytes(b"screen B")

    tracker = RewardTracker()

    assert tracker.evaluate(first) == 1
    assert tracker.evaluate(second) == 1


def test_hash_memory_survives_episodes(tmp_path):
    image = tmp_path / "screen.png"
    image.write_bytes(b"screen A")

    tracker = RewardTracker()

    assert tracker.evaluate(image) == 1

    # Simulate the start of another episode.
    # The tracker is deliberately not recreated.
    assert tracker.evaluate(image) == 0


def test_game_over_penalty():
    tracker = RewardTracker()

    assert tracker.game_over() == -500

