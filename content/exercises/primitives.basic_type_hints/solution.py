"""
Exercise 0101 - Basic Type Hints (Solution)

Goal:
    Learn how to annotate variables using Python's
    four most common built-in types.
"""

# Employee information

employee_name: str = "Alex Rivera"
employee_id: int = 49201
job_title: str = "Data Analyst"

# Compensation

hourly_rate: float = 35.50
hours_per_week: float = 37.5

# Personal information

age: int = 28

# Employment status

is_full_time: bool = True
completed_orientation: bool = False


if __name__ == "__main__":
    print("EMPLOYEE PROFILE")
    print(f"Name: {employee_name}")
    print(f"ID: {employee_id}")
    print(f"Role: {job_title}")
    print(f"Age: {age}")
    print(f"Hourly Rate: ${hourly_rate}")
    print(f"Hours Per Week: {hours_per_week}")
    print(f"Full Time: {is_full_time}")
    print(f"Orientation Complete: {completed_orientation}")
