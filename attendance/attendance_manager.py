import datetime
from data.storage import employees, attendance_records

def mark_attendance():
    print("\n>> Mark Attendance")
    emp_id = input("Enter Employee ID: ")
    emp_exists = any(emp["id"] == emp_id for emp in employees)
    if not emp_exists:
        print(">> Employee not found.")
        return
    date = str(datetime.date.today())
    status = input("Enter Status (Present/Absent): ").strip().capitalize()
    if status not in ["Present", "Absent"]:
        print(">> Invalid status. Use 'Present' or 'Absent'.")
        return
    record = {
        "id": emp_id,
        "date": date,
        "status": status
    }
    attendance_records.append(record)
    print(f">> Attendance marked for {emp_id} on {date} as {status}.")

def view_attendance():
    print("\n>> View Attendance Records")
    if not attendance_records:
        print(">> No attendance records found.")
        return
    print(f"\n{'Emp ID':<10}{'Date':<15}{'Status':<10}")
    print("-" * 35)
    for record in attendance_records:
        print(f"{record['id']:<10}{record['date']:<15}{record['status']:<10}")
