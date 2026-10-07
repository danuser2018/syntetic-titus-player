import argparse
from pathlib import Path

from titus_player.environment import TitusEnvironment


GAME_PATH = Path.home() / "games/fox/fox"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="titus-player",
        description="Synthetic Titus Player",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # start
    subparsers.add_parser(
        "start",
        help="Launch Titus",
    )

    # press-right
    press_right = subparsers.add_parser(
        "press-right",
        help="Hold RIGHT for a given duration",
    )
    press_right.add_argument(
        "duration",
        type=float,
        help="Duration in seconds",
    )

    # jump
    jump = subparsers.add_parser(
        "jump",
        help="Hold UP for a given duration",
    )
    jump.add_argument(
        "duration",
        type=float,
        help="Duration in seconds",
    )

    args = parser.parse_args()

    environment = TitusEnvironment(GAME_PATH)

    if args.command == "start":
        environment.start()

    elif args.command == "press-right":
        environment.hold("Right", args.duration)

    elif args.command == "jump":
        environment.hold("Up", args.duration)


if __name__ == "__main__":
    main()
