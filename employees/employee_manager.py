import datetime
import re
from data.storage import employees

def add_employee():
    print("\n>> Add Employee")
    emp_id = input("Enter Employee ID: ")
    if any(emp['id'] == emp_id for emp in employees):
        print(">> Employee ID already exists!")
        return
    name = input("Enter Name: ")
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
    employees.append(employee)
    print(f">> Employee '{name}' added successfully!")

def view_employees():
    print("\n>> View All Employees")
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
    for emp in employees:
        if emp['id'] == emp_id:
            confirm = input(f"Are you sure you want to remove {emp['name']}? (y/n): ").strip().lower()
            if confirm == 'y':
                employees.remove(emp)
                print(f">> Employee '{emp['name']}' removed successfully!")
            else:
                print(">> Removal cancelled.")
            return
    print(">> Employee not found.")
