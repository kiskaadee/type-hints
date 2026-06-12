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

    # init subcommand
    subparsers.add_parser("init", help="Initialize the local learner workspace.")

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
    set_parser.add_argument(
        "--allow-hints",
        choices=["true", "false"],
        help="Output static hints on errors (true/false).",
    )
    set_parser.add_argument(
        "--allow-llm",
        choices=["true", "false"],
        help="Output LLM-powered interactive hints (true/false).",
    )
    set_parser.add_argument(
        "--allow-glow",
        choices=["true", "false"],
        help="Use glow to render markdown (true/false).",
    )

    # view subcommand
    view_parser = subparsers.add_parser("view", help="View exercise problem details.")
    view_parser.add_argument(
        "target", help="Exercise ID or 'next' to view the next unsolved lesson."
    )

    return parser
