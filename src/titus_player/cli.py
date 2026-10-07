import argparse
from pathlib import Path

from titus_player.environment import TitusEnvironment


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["start", "stop"],
    )

    args = parser.parse_args()

    environment = TitusEnvironment(
        Path.home() / "games/fox/fox"
    )

    if args.command == "start":
        environment.start()

    elif args.command == "stop":
        environment.stop()


if __name__ == "__main__":
    main()
