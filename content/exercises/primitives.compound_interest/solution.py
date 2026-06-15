# Compound Interest Calculator
# TODO: Annotate these inputs as basic primitives (float, int, bool)
principal: float = 5000.0
rate: float = 0.045
years: int = 8
is_compound: bool = True

# Calculation logic
if is_compound:
    final_amount = principal * ((1 + rate) ** years)
else:
    final_amount = principal * (1 + (rate * years))

print(f"Final investment amount: {final_amount:.2f}")
