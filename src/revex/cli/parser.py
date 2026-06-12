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
        dest="command", required=False, help="Available subcommands"
    )

    # init subcommand
    subparsers.add_parser(
        "init",
        help="Initialize the local learner workspace, creating config files, progress database, and directories.",
    )

    # status subcommand
    subparsers.add_parser(
        "status",
        help="Show current progress status, completion rates, and attempts breakdown by module.",
    )

    # sync subcommand
    subparsers.add_parser(
        "sync",
        help="Synchronize the workspace directory with the latest course content catalog without overwriting existing solutions.",
    )

    # check subcommand
    check_parser = subparsers.add_parser(
        "check",
        help="Validate an exercise solution by performing structural AST checks and strict Pyright type checking.",
    )
    check_parser.add_argument(
        "target",
        nargs="?",
        help="Path to the Python solution file or a 4-digit exercise ID (e.g. 0101).",
    )

    # set subcommand
    set_parser = subparsers.add_parser(
        "set",
        help="View or update settings such as preferred language, static error hints, and terminal markdown formatting.",
    )
    set_parser.add_argument(
        "--language",
        choices=["en", "es"],
        help="Set preferred language code for descriptions and hints ('en' or 'es').",
    )
    set_parser.add_argument(
        "--allow-hints",
        choices=["true", "false"],
        help="Enable or disable localized static hints on validation check failures ('true' or 'false').",
    )
    set_parser.add_argument(
        "--allow-llm",
        choices=["true", "false"],
        help="Enable or disable personalized LLM-powered hints ('true' or 'false'). (Coming soon)",
    )
    set_parser.add_argument(
        "--allow-glow",
        choices=["true", "false"],
        help="Enable or disable glow-decorated markdown rendering in the terminal ('true' or 'false').",
    )

    # view subcommand
    view_parser = subparsers.add_parser(
        "view",
        help="View exercise description, learning objectives, and success criteria in the terminal.",
    )
    view_parser.add_argument(
        "target",
        help="A 4-digit exercise ID (e.g. 0101) or 'next' to view the next unsolved lesson.",
    )

    # help subcommand
    help_parser = subparsers.add_parser(
        "help",
        help="Show help information for a subcommand.",
    )
    help_parser.add_argument(
        "target",
        nargs="?",
        help="Subcommand name to show help for (e.g., init, status, sync, check, set, view).",
    )

    return parser
