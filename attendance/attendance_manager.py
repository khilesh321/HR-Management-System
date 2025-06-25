import datetime
from data.storage import employees, attendance_records

def mark_attendance():
    print("\n>> Mark Attendance")
    emp_id = input("Enter Employee ID: ").strip()
    if not emp_id:
        print(">> Employee ID cannot be empty!")
        return
    emp_exists = any(emp["id"] == emp_id for emp in employees)
    if not emp_exists:
        print(">> Employee not found.")
        return
    date = str(datetime.date.today())
    # Prevent duplicate attendance for the same day
    if any(rec["id"] == emp_id and rec["date"] == date for rec in attendance_records):
        print(f">> Attendance for {emp_id} already marked for today.")
        return
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
    filter_id = input("Filter by Employee ID (leave blank for all): ").strip()
    filter_date = input("Filter by Date (YYYY-MM-DD, leave blank for all): ").strip()
    filtered = attendance_records
    if filter_id:
        filtered = [r for r in filtered if r['id'] == filter_id]
    if filter_date:
        filtered = [r for r in filtered if r['date'] == filter_date]
    if not filtered:
        print(">> No records match the criteria.")
        return
    print(f"\n{'Emp ID':<10}{'Date':<15}{'Status':<10}")
    print("-" * 35)
    for record in filtered:
        print(f"{record['id']:<10}{record['date']:<15}{record['status']:<10}")
    # Show summary if filtered by employee
    if filter_id:
        present = sum(1 for r in filtered if r['status'] == 'Present')
        absent = sum(1 for r in filtered if r['status'] == 'Absent')
        print(f"\nSummary for {filter_id}: Present: {present}, Absent: {absent}")
