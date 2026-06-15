# HR Department Employee Roster
# TODO: Annotate department_roster as a nested structure.
department_roster: dict[str, list[dict[str, str]]] = {
    "Engineering": [
        {"name": "Alice", "role": "Backend Engineer"},
        {"name": "Bob", "role": "Frontend Engineer"}
    ],
    "Design": [
        {"name": "Charlie", "role": "UI Designer"}
    ]
}

# Print department headcount
for dept, members in department_roster.items():
    print(f"Department {dept} has {len(members)} active team members.")
