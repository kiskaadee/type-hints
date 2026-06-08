"""
Exercise 0101 - Basic Type Hints

Goal:
    Learn how to annotate variables using Python's
    four most common built-in types.

Instructions:
    Replace every ??? with the correct type hint.
"""

# Employee information

employee_name: ??? = "Alex Rivera"
employee_id: ??? = 49201
job_title: ??? = "Data Analyst"

# Compensation

hourly_rate: ??? = 35.50
hours_per_week: ??? = 37.5

# Personal information

age: ??? = 28

# Employment status

is_full_time: ??? = True
completed_orientation: ??? = False


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
