# User Session Action Analytics
# TODO: Annotate user_sessions and session_durations.
user_sessions: dict[str, list[str]] = {
    "alice": ["login", "view_page", "logout"],
    "bob": ["login"]
}
session_durations: list[dict[str, int]] = [
    {"session_1": 180, "session_2": 320},
    {"session_1": 45}
]

# Print activity details
for user, events in user_sessions.items():
    print(f"User {user} performed {len(events)} events.")
