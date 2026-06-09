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
