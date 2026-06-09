"""
Validation orchestration.

Coordinates all validation steps required
to evaluate an exercise submission.

Responsible for:
    - locating exercise metadata
    - executing validators
    - aggregating validation results
    - reporting validation outcomes

Not responsible for:
    - implementing validation rules
    - content loading internals
"""
# usage: uv run review check <filename.py>
#
#   - Infer exercise Id from path
#   - Runs:
#       - AST validator
#       - Pyright validator
#       - Outputs validation result
#               - On success: triggers save_progress()
#               - On failure: suggests hint/explanation
#
#
