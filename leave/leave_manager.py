from data.storage import leave_requests
import datetime

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_overlapping(emp_id, date):
    for req in leave_requests:
        if req['id'] == emp_id and req['date'] == date:
            return True
    return False

def apply_leave():
    print(">> Apply for Leave")
    emp_id = input("Enter Employee ID: ").strip()
    if not emp_id:
        print(">> Employee ID cannot be empty!")
        return
    date = input("Enter Leave Date (YYYY-MM-DD): ").strip()
    if not is_valid_date(date):
        print(">> Invalid date format!")
        return
    if is_overlapping(emp_id, date):
        print(">> Leave request for this date already exists!")
        return
    reason = input("Enter Reason: ").strip()
    if not reason:
        print(">> Reason cannot be empty!")
        return
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
    filter_id = input("Filter by Employee ID (leave blank for all): ").strip()
    filter_status = input("Filter by Status (Pending/Approved/Rejected, leave blank for all): ").strip().capitalize()
    filtered = leave_requests
    if filter_id:
        filtered = [r for r in filtered if r['id'] == filter_id]
    if filter_status:
        filtered = [r for r in filtered if r['status'] == filter_status]
    if not filtered:
        print(">> No leave requests match the criteria.")
        return
    print(f"\n{'Emp ID':<10}{'Date':<15}{'Reason':<20}{'Status':<10}")
    print("-" * 55)
    for req in filtered:
        print(f"{req['id']:<10}{req['date']:<15}{req['reason']:<20}{req['status']:<10}")
    # Approve/Reject pending requests
    for req in filtered:
        if req['status'] == 'Pending':
            action = input(f"Approve/Reject leave for {req['id']} on {req['date']}? (a/r/skip): ").strip().lower()
            if action == 'a':
                req['status'] = 'Approved'
                print(f"Leave approved for {req['id']} on {req['date']}.")
            elif action == 'r':
                req['status'] = 'Rejected'
                print(f"Leave rejected for {req['id']} on {req['date']}.")
            else:
                print("Skipped.")
