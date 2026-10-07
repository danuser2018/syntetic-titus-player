from pathlib import Path
import subprocess


class TitusEnvironment:
    def __init__(self, game_path: Path):
        self.game_path = game_path
        self.process: subprocess.Popen | None = None

    def start(self) -> None:
        if self.process is not None:
            raise RuntimeError("Titus is already running")

        command = [
            "dosbox",
            "-c", f"mount c {self.game_path}",
            "-c", "c:",
            "-c", "FOX.COM",
        ]

        self.process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
           stderr=subprocess.DEVNULL,
        )

    def stop(self) -> None:
        if self.process is None:
            return

        self.process.terminate()
        self.process.wait()
        self.process = None
