from data.storage import leave_requests

def apply_leave():
    print(">> Apply for Leave")
    emp_id = input("Enter Employee ID: ")
    date = input("Enter Leave Date (YYYY-MM-DD): ")
    reason = input("Enter Reason: ")
    leave = {
        "id": emp_id,
        "date": date,
        "reason": reason,
        "status": "Pending"
    }
    leave_requests.append(leave)
    print(f">> Leave request submitted for {emp_id} on {date}.")

def view_leave_requests():
    print(">> View Leave Requests")
    if not leave_requests:
        print(">> No leave requests found.")
        return
    print(f"\n{'Emp ID':<10}{'Date':<15}{'Reason':<20}{'Status':<10}")
    print("-" * 55)
    for req in leave_requests:
        print(f"{req['id']:<10}{req['date']:<15}{req['reason']:<20}{req['status']:<10}")
