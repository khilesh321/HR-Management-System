import datetime

employees = []
attendance_records = []
leave_requests = []

# --- EMPLOYEE FUNCTIONS ---

def add_employee():
    print("\n>> Add Employee")
    
    emp_id = input("Enter Employee ID: ")
    name = input("Enter Name: ")
    designation = input("Enter Designation: ")
    date_joined = str(datetime.date.today())
    
    # Dictionary bana rahe
    employee = {
        "id": emp_id,
        "name": name,
        "designation": designation,
        "date_joined": date_joined
    }

    # Add to list
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


# --- ATTENDANCE FUNCTIONS ---

def mark_attendance():
    print(">> Mark Attendance")
    # Input: employee ID, date = today, status (Present/Absent)
    pass

def view_attendance():
    print(">> View Attendance Records")
    pass

# --- LEAVE MANAGEMENT ---

def apply_leave():
    print(">> Apply for Leave")
    pass

def view_leave_requests():
    print(">> View Leave Requests")
    pass

# --- SALARY CALCULATION ---

def calculate_salary():
    print(">> Calculate Salary")
    pass

# --- MAIN MENU LOOP ---

def main_menu():
    while True:
        print("\n==== HR MANAGEMENT SYSTEM ====")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Remove Employee")
        print("4. Mark Attendance")
        print("5. View Attendance")
        print("6. Apply for Leave")
        print("7. View Leave Requests")
        print("8. Calculate Salary")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_employee()
        elif choice == '2':
            view_employees()
        elif choice == '3':
            remove_employee()
        elif choice == '4':
            mark_attendance()
        elif choice == '5':
            view_attendance()
        elif choice == '6':
            apply_leave()
        elif choice == '7':
            view_leave_requests()
        elif choice == '8':
            calculate_salary()
        elif choice == '9':
            print("Exiting HR Management System...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
