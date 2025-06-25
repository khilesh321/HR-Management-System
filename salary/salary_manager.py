from data.storage import employees, attendance_records

def calculate_salary():
    print(">> Calculate Salary")
    emp_id = input("Enter Employee ID: ")
    present_days = sum(1 for rec in attendance_records if rec["id"] == emp_id and rec["status"] == "Present")
    absent_days = sum(1 for rec in attendance_records if rec["id"] == emp_id and rec["status"] == "Absent")
    base_salary = 20000  # Example base salary
    per_day = base_salary / 30
    salary = per_day * present_days
    print(f"Salary for {emp_id}: {salary:.2f} (Present: {present_days}, Absent: {absent_days})")
