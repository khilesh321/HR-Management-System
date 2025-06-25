import datetime
import re
from data.storage import get_employees, add_employee_db, remove_employee_db

def add_employee():
    print("\n>> Add Employee")
    emp_id = input("Enter Employee ID: ").strip()
    if not emp_id:
        print(">> Employee ID cannot be empty!")
        return
    if get_employees({'id': emp_id}):
        print(">> Employee ID already exists!")
        return
    name = input("Enter Name: ").strip()
    if not name:
        print(">> Name cannot be empty!")
        return
    email = input("Enter Email: ")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print(">> Invalid email format!")
        return
    phone = input("Enter Phone: ")
    if not re.match(r"^\d{10}$", phone):
        print(">> Invalid phone number! Must be 10 digits.")
        return
    department = input("Enter Department: ")
    designation = input("Enter Designation: ")
    date_joined = str(datetime.date.today())
    employee = {
        "id": emp_id,
        "name": name,
        "email": email,
        "phone": phone,
        "department": department,
        "designation": designation,
        "date_joined": date_joined
    }
    add_employee_db(employee)
    print(f">> Employee '{name}' added successfully!")

def view_employees():
    print("\n>> View All Employees")
    employees = get_employees()
    if not employees:
        print("No employees found.")
        return
    filter_dept = input("Filter by Department (leave blank for all): ").strip()
    filter_name = input("Search by Name (leave blank for all): ").strip().lower()
    filtered = employees
    if filter_dept:
        filtered = [e for e in filtered if e['department'].lower() == filter_dept.lower()]
    if filter_name:
        filtered = [e for e in filtered if filter_name in e['name'].lower()]
    if not filtered:
        print("No employees match the criteria.")
        return
    print(f"\n{'ID':<8}{'Name':<18}{'Email':<25}{'Phone':<12}{'Dept':<12}{'Designation':<18}{'Date Joined':<12}")
    print("-" * 105)
    for emp in filtered:
        print(f"{emp['id']:<8}{emp['name']:<18}{emp['email']:<25}{emp['phone']:<12}{emp['department']:<12}{emp['designation']:<18}{emp['date_joined']:<12}")

def remove_employee():
    print("\n>> Remove Employee")
    emp_id = input("Enter Employee ID to remove: ")
    employees = get_employees({'id': emp_id})
    if not employees:
        print(">> Employee not found.")
        return
    emp = employees[0]
    confirm = input(f"Are you sure you want to remove {emp['name']}? (y/n): ").strip().lower()
    if confirm == 'y':
        remove_employee_db(emp_id)
        print(f">> Employee '{emp['name']}' removed successfully!")
    else:
        print(">> Removal cancelled.")
