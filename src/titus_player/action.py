from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    keys: tuple[str, ...]
    duration: float

