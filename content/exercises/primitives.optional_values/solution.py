# Customer Support Ticket System

# These fields are required
ticket_id: int = 1045
customer_name: str = "Alice Smith"

# These fields may not be populated when the ticket is first created.
# TODO: Annotate them to indicate they can be a string OR None.
assigned_agent: str | None = None
resolution_notes: str | None = None


def close_ticket(agent: str) -> None:
    """Closes the ticket and records the agent who handled it."""
    print(f"Ticket closed by {agent}")


# TODO: strict type checkers will flag the line below as an error.
# Why? Because 'assigned_agent' might be None, but 'close_ticket' strictly requires a 'str'.
# Wrap the function call in an 'if' statement (a type guard) to check that 
# 'assigned_agent' is not None before calling the function.

if assigned_agent is not None:
    close_ticket(assigned_agent)
