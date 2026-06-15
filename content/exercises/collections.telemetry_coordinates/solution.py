# GPS Tracker Coordinates
# TODO: Annotate coordinate tuple and path list of coordinate tuples.
current_position: tuple[float, float] = (40.7128, -74.0060)
waypoint_coordinates: list[tuple[float, float]] = [
    (40.7128, -74.0060),
    (34.0522, -118.2437)
]

# Calculate route step count
step_count = len(waypoint_coordinates)
print(f"Calculating route through {step_count} checkpoints starting at {current_position}")
