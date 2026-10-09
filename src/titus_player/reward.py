import hashlib
from pathlib import Path


class RewardTracker:
    def __init__(self):
        self.seen_hashes: set[str] = set()

    def evaluate(self, screenshot_path: str | Path) -> int:
        image_data = Path(screenshot_path).read_bytes()
        image_hash = hashlib.sha256(image_data).hexdigest()

        if image_hash in self.seen_hashes:
            return 0

        self.seen_hashes.add(image_hash)
        return 1

    def game_over(self) -> int:
        return -500
