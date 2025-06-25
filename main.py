from employees.employee_manager import add_employee, view_employees, remove_employee
from attendance.attendance_manager import mark_attendance, view_attendance
from leave.leave_manager import apply_leave, view_leave_requests
from salary.salary_manager import calculate_salary

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
