"""
CLI Argument Parser.

Defines options, flags, subcommands, and help text.
"""

import argparse


def create_parser() -> argparse.ArgumentParser:
    """Creates and configures the ArgumentParser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="revex",
        description="CLI tool for learning Python type hints through guided exercises.",
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available subcommands"
    )

    # setup subcommand
    subparsers.add_parser("setup", help="Initialize the local learner workspace.")

    # status subcommand
    subparsers.add_parser(
        "status", help="Show current module-by-module completion status."
    )

    # sync subcommand
    subparsers.add_parser(
        "sync", help="Synchronize workspace exercises with latest catalog."
    )

    # check subcommand
    check_parser = subparsers.add_parser("check", help="Validate an exercise solution.")
    check_parser.add_argument(
        "target", nargs="?", help="Path to exercise file or exercise ID."
    )

    # set subcommand
    set_parser = subparsers.add_parser("set", help="View or update preferences.")
    set_parser.add_argument(
        "--language", choices=["en", "es"], help="Set preferred language (en/es)."
    )

    # view subcommand
    view_parser = subparsers.add_parser("view", help="View exercise problem details.")
    view_parser.add_argument(
        "target", help="Exercise ID or 'next' to view the next unsolved lesson."
    )

    return parser
