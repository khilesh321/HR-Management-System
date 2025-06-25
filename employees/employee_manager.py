import datetime
from data.storage import employees

def add_employee():
    print("\n>> Add Employee")
    emp_id = input("Enter Employee ID: ")
    name = input("Enter Name: ")
    designation = input("Enter Designation: ")
    date_joined = str(datetime.date.today())
    employee = {
        "id": emp_id,
        "name": name,
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
    print(f"\n{'ID':<10}{'Name':<20}{'Designation':<20}{'Date Joined':<15}")
    print("-" * 65)
    for emp in employees:
        print(f"{emp['id']:<10}{emp['name']:<20}{emp['designation']:<20}{emp['date_joined']:<15}")

def remove_employee():
    print("\n>> Remove Employee")
    emp_id = input("Enter Employee ID to remove: ")
    for emp in employees:
        if emp['id'] == emp_id:
            employees.remove(emp)
            print(f">> Employee '{emp['name']}' removed successfully!")
            return
    print(">> Employee not found.")
