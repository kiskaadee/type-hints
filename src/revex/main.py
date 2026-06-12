"""
CLI entrypoint.

Responsible for:
    - parsing command line arguments
    - routing commands to application services
    - displaying user-facing output

Not responsible for:
    - content loading
    - validation logic
    - progress persistence
    - synchronization logic
"""

import argparse
import sys
from typing import cast

from revex.cli import (
    create_parser,
    execute_check,
    execute_init,
    execute_set,
    execute_status,
    execute_sync,
    execute_view,
)


class CLIArgs(argparse.Namespace):
    """Command line arguments namespace type-hint helper."""

    def __init__(self) -> None:
        super().__init__()
        self.command: str = ""
        self.target: str | None = None
        self.language: str | None = None
        self.allow_hints: str | None = None
        self.allow_llm: str | None = None
        self.allow_glow: str | None = None


def main() -> None:
    """Parses command line arguments and routes execution to command handlers."""
    parser = create_parser()
    args = cast(CLIArgs, parser.parse_args())

    if args.command == "init":
        execute_init()
    elif args.command == "status":
        execute_status()
    elif args.command == "sync":
        execute_sync()
    elif args.command == "check":
        execute_check(args.target)
    elif args.command == "set":
        execute_set(
            language=args.language,
            allow_hints=args.allow_hints,
            allow_llm=args.allow_llm,
            allow_glow=args.allow_glow,
        )
    elif args.command == "view" and args.target is not None:
        execute_view(args.target)
    elif args.command == "help":
        subparser_choices = {}
        for action in parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                subparser_choices = action.choices
                break
        if args.target and args.target in subparser_choices:
            subparser_choices[args.target].print_help()
        else:
            parser.print_help()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
