# Game Physics: 2D Spawn Telemetry
# TODO: Annotate coordinates as floats, and spawn_delay as a nullable float.
delta_x: float = 12.5
delta_y: float = -4.2
spawn_delay: float | None = None

# Calculate spawn offset
if spawn_delay is not None:
    distance_multiplier = spawn_delay * 2.0
else:
    distance_multiplier = 1.0

offset_x = delta_x * distance_multiplier
print(f"Spawn offsets calculated: x={offset_x:.2f}")
