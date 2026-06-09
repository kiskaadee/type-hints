"""
Workspace initialization.

Creates the local learner environment required
to use the application.

Responsible for:
    - creating workspace/
    - creating .user_data/
    - generating default config
    - generating initial progress state

Not responsible for:
    - content updates
    - exercise validation
    - progress reporting
"""

# usage: uv run revex setup
#   Creates:
#       workspace/
#           <populates exercises>
#       .user_data/
#           - config.toml
#           - progress.json
#           - cache/
