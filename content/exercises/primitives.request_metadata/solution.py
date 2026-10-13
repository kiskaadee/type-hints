# HTTP Request Metadata
# TODO: Annotate these parameters to show they can be strings, integers, or None.
user_agent: str | None = None
auth_token: str | None = None
content_length: int | None = None


def fetch_header(name: str) -> str | None:
    headers = {"User-Agent": "Mozilla/5.0"}
    return headers.get(name)


# Simulate receiving a partial request
user_agent = fetch_header("User-Agent")
auth_token = fetch_header("Authorization")
content_length = 256 if user_agent else None

# Verify headers before execution
if user_agent is not None:
    print(f"Browser agent: {user_agent}")

if content_length is not None:
    print(f"Payload size: {content_length} bytes")
