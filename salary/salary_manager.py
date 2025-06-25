from data.storage import employees, attendance_records

def calculate_salary():
    print(">> Calculate Salary")
    emp_id = input("Enter Employee ID: ").strip()
    if not emp_id:
        print(">> Employee ID cannot be empty!")
        return
    # Find employee and allow custom base salary
    emp = next((e for e in employees if e['id'] == emp_id), None)
    if not emp:
        print(">> Employee not found!")
        return
    try:
        base_salary = float(input("Enter Base Salary (default 20000): ") or 20000)
    except ValueError:
        print(">> Invalid salary input!")
        return
    present_days = sum(1 for rec in attendance_records if rec["id"] == emp_id and rec["status"] == "Present")
    absent_days = sum(1 for rec in attendance_records if rec["id"] == emp_id and rec["status"] == "Absent")
    # Deductions: 1 day salary for each absence, bonus for perfect attendance
    per_day = base_salary / 30
    deduction = per_day * absent_days
    bonus = 0
    if absent_days == 0 and present_days > 0:
        bonus = 0.05 * base_salary  # 5% bonus for perfect attendance
    salary = (per_day * present_days) + bonus
    print(f"\nSalary Slip for {emp['name']} ({emp_id})")
    print(f"Base Salary: {base_salary:.2f}")
    print(f"Present Days: {present_days}")
    print(f"Absent Days: {absent_days}")
    print(f"Deduction: {deduction:.2f}")
    print(f"Bonus: {bonus:.2f}")
    print(f"Net Salary: {salary:.2f}")
