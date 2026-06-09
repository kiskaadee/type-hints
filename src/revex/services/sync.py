"""
Workspace synchronization.

Keeps the learner workspace aligned with
the bundled course content.

Responsible for:
    - detecting missing exercises
    - copying new exercises into workspace
    - updating workspace metadata

Guarantees:
    - learner work is never overwritten

Not responsible for:
    - validation
    - progress tracking
    - content discovery
"""
#
# uv run revex sync
#   - Syncs workspace with manifest.
#   - Adds new exercises.
#   - Never overwrites learner work.
#


# for exercise in manifest:
#     if not workspace_contains(exercise):
#         copy_exercise(exercise)
