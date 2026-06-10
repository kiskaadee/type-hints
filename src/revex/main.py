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
import sys
from revex.cli import (
    create_parser,
    execute_setup,
    execute_status,
    execute_sync,
    execute_check,
    execute_set,
    execute_view,
)

def main() -> None:
    """Parses command line arguments and routes execution to command handlers."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "setup":
        execute_setup()
    elif args.command == "status":
        execute_status()
    elif args.command == "sync":
        execute_sync()
    elif args.command == "check":
        execute_check(args.target)
    elif args.command == "set":
        execute_set(args.language)
    elif args.command == "view":
        execute_view(args.target)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
