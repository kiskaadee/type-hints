# Configuration Manager
# TODO: Annotate the variables with their appropriate primitive/optional type hints.
port: int = 8000
host: str = "0.0.0.0"
ssl_cert: str | None = None
debug_mode: bool = False

# Print status configuration
ssl_status = "enabled" if ssl_cert is not None else "disabled"
print(f"Server configured at {host}:{port} with SSL {ssl_status} (debug: {debug_mode})")
