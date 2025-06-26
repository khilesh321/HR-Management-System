import customtkinter as ctk
import tkinter.messagebox as mbox
from employees.employee_manager import add_employee, view_employees, update_employee, remove_employee
from attendance.attendance_manager import mark_attendance, view_attendance
from leave.leave_manager import apply_leave, view_leave_requests
from salary.salary_manager import calculate_salary

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("HR Management System")
root.geometry("900x600")
root.resizable(False, False)

sidebar = ctk.CTkFrame(root, width=180)
sidebar.pack(side="left", fill="y")
ctk.CTkLabel(sidebar, text="HR Menu", font=("Arial", 18, "bold")).pack(pady=20)

content = ctk.CTkFrame(root)
content.pack(side="right", fill="both", expand=True)

def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

def show_employees():
    clear_content()
    ctk.CTkLabel(content, text="Employee Management", font=("Arial", 20, "bold")).pack(pady=10)
    ctk.CTkButton(content, text="Add Employee", command=add_employee_gui).pack(pady=5)
    ctk.CTkButton(content, text="View Employees", command=view_employees_gui).pack(pady=5)

def add_employee_gui():
    win = ctk.CTkToplevel(root)
    win.title("Add Employee")
    win.geometry("400x500")
    win.attributes("-topmost", True)
    # win.grab_set()  # Focus ko forcefully le leta hai

    entries = {}
    fields = ["ID", "Name", "Email", "Phone", "Department", "Designation"]
    
    # Frame ke andar form daal rahe
    form_frame = ctk.CTkFrame(win)
    form_frame.pack(pady=10, padx=10, fill="both", expand=True)

    for i, field in enumerate(fields):
        ctk.CTkLabel(form_frame, text=field + ":").pack(pady=(10 if i == 0 else 5, 0))
        entry = ctk.CTkEntry(form_frame)
        entry.pack(fill="x", padx=10)
        entries[field.lower()] = entry

    # Submit Button fix
    submit_button = ctk.CTkButton(form_frame, text="Submit", command=lambda: submit(entries, win))
    submit_button.pack(pady=20)

def submit(entries, win):
    import builtins
    old_input = builtins.input

    def fake_input(prompt=""):
        key = prompt.lower().split(" ")[2].replace(":", "") if "id" in prompt.lower() else prompt.lower().split(" ")[1].replace(":", "")
        entry_widget = entries.get(key)
        if entry_widget:
            return entry_widget.get()
        else:
            return ""

    builtins.input = fake_input
    try:
        add_employee()
        mbox.showinfo("Success", "Employee added!")
        win.destroy()
    except Exception as e:
        mbox.showerror("Error", str(e))
    finally:
        builtins.input = old_input

def view_employees_gui():
    win = ctk.CTkToplevel(root)
    win.title("View Employees")
    win.geometry("900x500")
    win.attributes("-topmost", True)
    from data.storage import get_employees
    employees = get_employees()
    columns = ["ID", "Name", "Email", "Phone", "Department", "Designation", "Date Joined"]
    table = ctk.CTkFrame(win)
    table.pack(pady=10, padx=10, fill="both", expand=True)
    for j, col in enumerate(columns):
        ctk.CTkLabel(table, text=col, font=("Arial", 12, "bold"), width=15).grid(row=0, column=j, padx=2, pady=2)
    for i, emp in enumerate(employees, start=1):
        ctk.CTkLabel(table, text=emp.get('id', ''), width=15).grid(row=i, column=0, padx=2, pady=2)
        ctk.CTkLabel(table, text=emp.get('name', ''), width=15).grid(row=i, column=1, padx=2, pady=2)
        ctk.CTkLabel(table, text=emp.get('email', ''), width=20).grid(row=i, column=2, padx=2, pady=2)
        ctk.CTkLabel(table, text=emp.get('phone', ''), width=12).grid(row=i, column=3, padx=2, pady=2)
        ctk.CTkLabel(table, text=emp.get('department', ''), width=12).grid(row=i, column=4, padx=2, pady=2)
        ctk.CTkLabel(table, text=emp.get('designation', ''), width=15).grid(row=i, column=5, padx=2, pady=2)
        ctk.CTkLabel(table, text=emp.get('date_joined', ''), width=12).grid(row=i, column=6, padx=2, pady=2)
    if not employees:
        ctk.CTkLabel(table, text="No employees found.", font=("Arial", 14)).grid(row=1, column=0, columnspan=len(columns), pady=20)

def show_attendance():
    clear_content()
    ctk.CTkLabel(content, text="Attendance Management (Coming Soon)", font=("Arial", 20, "bold")).pack(pady=10)

def show_leave():
    clear_content()
    ctk.CTkLabel(content, text="Leave Management (Coming Soon)", font=("Arial", 20, "bold")).pack(pady=10)

def show_salary():
    clear_content()
    ctk.CTkLabel(content, text="Salary Calculation (Coming Soon)", font=("Arial", 20, "bold")).pack(pady=10)

ctk.CTkButton(sidebar, text="Employees", command=show_employees).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Attendance", command=show_attendance).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Leave", command=show_leave).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Salary", command=show_salary).pack(pady=10, fill="x")

show_employees()
root.mainloop()
