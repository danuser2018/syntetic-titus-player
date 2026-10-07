from pathlib import Path
import subprocess
import time

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

    def focus(self):
        result = subprocess.run(
            ["xdotool", "search", "--name", "DOSBox"],
            capture_output=True,
            text=True,
            check=True,
        )

        windows = result.stdout.strip().splitlines()

        if not windows:
            raise RuntimeError("DOSBox window not found")

        self.window_id = windows[0]

        subprocess.run(
            ["xdotool", "windowactivate", self.window_id],
            check=True,
        )


    def key_down(self, key):
        subprocess.run(
            ["xdotool", "keydown", key],
            check=True,
        )

    def key_up(self, key):
        subprocess.run(
            ["xdotool", "keyup", key],
            check=True,
        )

    def hold(self, key, duration):
        self.focus()
        self.key_down(key)
        time.sleep(duration)
        self.key_up(key)
