from data.storage import get_employees, get_attendance

def calculate_salary():
    print(">> Calculate Salary")
    emp_id = input("Enter Employee ID: ").strip()
    if not emp_id:
        print(">> Employee ID cannot be empty!")
        return
    employees = get_employees({'id': emp_id})
    if not employees:
        print(">> Employee not found!")
        return
    emp = employees[0]
    try:
        base_salary = float(input("Enter Base Salary (default 20000): ") or 20000)
    except ValueError:
        print(">> Invalid salary input!")
        return
    attendance_records = get_attendance({'id': emp_id})
    present_days = sum(1 for rec in attendance_records if rec["status"] == "Present")
    absent_days = sum(1 for rec in attendance_records if rec["status"] == "Absent")
    per_day = base_salary / 30
    deduction = per_day * absent_days
    bonus = 0
    if absent_days == 0 and present_days >= 28:
        bonus = 0.05 * base_salary  # 5% bonus for perfect attendance
    salary = (per_day * present_days) + bonus
    print(f"\nSalary Slip for {emp['name']} ({emp_id})")
    print(f"Base Salary: {base_salary:.2f}")
    print(f"Present Days: {present_days}")
    print(f"Absent Days: {absent_days}")
    print(f"Deduction: {deduction:.2f}")
    print(f"Bonus: {bonus:.2f}")
    print(f"Net Salary: {salary:.2f}")
