# HTTP Request Metadata
# TODO: Annotate these parameters to show they can be strings, integers, or None.
user_agent: str | None = None
auth_token: str | None = None
content_length: int | None = None

# Simulate receiving a partial request
user_agent = "Mozilla/5.0"
content_length = 256

# Verify headers before execution
if user_agent is not None:
    print(f"Browser agent: {user_agent}")

if content_length is not None:
    print(f"Payload size: {content_length} bytes")
