"""
Workspace initialization.

Creates the local learner environment required
to use the application.

Responsible for:
    - creating workspace/
    - creating .review/
    - generating default config
    - generating initial progress state

Not responsible for:
    - content updates
    - exercise validation
    - progress reporting
"""

# usage: uv run review setup
#   Creates:
#       workspace/
#           <populates version-specific exercises>
#       .review/
#           - config.toml
#           - progress.json
#           - cache/
