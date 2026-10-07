import argparse
from pathlib import Path

from titus_player.action import Action
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

    # combo-right
    combo_right = subparsers.add_parser(
        "combo-right",
        help="Hold UP + RIGHT for a given duration",
    )
    combo_right.add_argument(
        "duration",
        type=float,
        help="Duration in seconds",
    )

    # combo-left
    combo_left = subparsers.add_parser(
        "combo-left",
        help="Hold UP + LEFT for a given duration",
    )
    combo_left.add_argument(
        "duration",
        type=float,
        help="Duration in seconds",
    )

    # generic action
    action_parser = subparsers.add_parser(
        "action",
        help="Execute an action",
    )

    action_parser.add_argument(
        "duration",
        type=float,
        help="Duration in seconds",
    )

    action_parser.add_argument(
        "keys",
        nargs="+",
        help="Keys to hold",
    )

    args = parser.parse_args()

    environment = TitusEnvironment(GAME_PATH)

    if args.command == "start":
        environment.start()

    elif args.command == "press-right":
        environment.hold("Right", args.duration)

    elif args.command == "jump":
        environment.hold("Up", args.duration)

    elif args.command == "combo-right":
        environment.hold_combo(["Up", "Right"], args.duration)

    elif args.command == "combo-left":
        environment.hold_combo(["Up", "Left"], args.duration)

    elif args.command == "action":
        action = Action(
            keys=tuple(args.keys),
            duration=args.duration,
        )
        print(f"Executing action: {action}")
        environment.execute(action)

if __name__ == "__main__":
    main()
