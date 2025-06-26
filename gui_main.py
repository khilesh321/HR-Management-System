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
    entries = {}
    fields = ["ID", "Name", "Email", "Phone", "Department", "Designation"]
    form_frame = ctk.CTkFrame(win)
    form_frame.pack(pady=10, padx=10, fill="both", expand=True)
    for i, field in enumerate(fields):
        ctk.CTkLabel(form_frame, text=field + ":").pack(pady=(10 if i == 0 else 5, 0))
        entry = ctk.CTkEntry(form_frame)
        entry.pack(fill="x", padx=10)
        entries[field.lower()] = entry
    def submit_gui():
        from data.storage import add_employee_db, get_employees
        import re, datetime
        emp_id = entries['id'].get().strip()
        name = entries['name'].get().strip()
        email = entries['email'].get().strip()
        phone = entries['phone'].get().strip()
        department = entries['department'].get().strip()
        designation = entries['designation'].get().strip()
        # Validation
        if not emp_id:
            mbox.showerror("Error", "Employee ID cannot be empty!")
            return
        if get_employees({'id': emp_id}):
            mbox.showerror("Error", "Employee ID already exists!")
            return
        if not name:
            mbox.showerror("Error", "Name cannot be empty!")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            mbox.showerror("Error", "Invalid email format!")
            return
        if not re.match(r"^\d{10}$", phone):
            mbox.showerror("Error", "Invalid phone number! Must be 10 digits.")
            return
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
        mbox.showinfo("Success", f"Employee '{name}' added!")
        win.destroy()
    submit_button = ctk.CTkButton(form_frame, text="Submit", command=submit_gui)
    submit_button.pack(pady=20)

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
    ctk.CTkLabel(content, text="Attendance Management", font=("Arial", 20, "bold")).pack(pady=10)
    ctk.CTkButton(content, text="Mark Attendance", command=mark_attendance_gui).pack(pady=5)
    ctk.CTkButton(content, text="View Attendance", command=view_attendance_gui).pack(pady=5)

def mark_attendance_gui():
    win = ctk.CTkToplevel(root)
    win.title("Mark Attendance")
    win.geometry("400x300")
    win.attributes("-topmost", True)
    from data.storage import get_employees, add_attendance_db, get_attendance
    import datetime
    # Employee ID dropdown
    ctk.CTkLabel(win, text="Employee ID:").pack(pady=10)
    employees = get_employees()
    emp_ids = [emp['id'] for emp in employees]
    emp_id_var = ctk.StringVar(value=emp_ids[0] if emp_ids else "")
    emp_menu = ctk.CTkOptionMenu(win, variable=emp_id_var, values=emp_ids)
    emp_menu.pack()
    # Status dropdown
    ctk.CTkLabel(win, text="Status:").pack(pady=10)
    status_var = ctk.StringVar(value="Present")
    status_menu = ctk.CTkOptionMenu(win, variable=status_var, values=["Present", "Absent"])
    status_menu.pack()
    def submit_attendance():
        emp_id = emp_id_var.get()
        status = status_var.get()
        date = str(datetime.date.today())
        if not emp_id:
            mbox.showerror("Error", "Please select an Employee ID.")
            return
        if get_attendance({'id': emp_id, 'date': date}):
            mbox.showerror("Error", f"Attendance for {emp_id} already marked for today.")
            return
        record = {"id": emp_id, "date": date, "status": status}
        add_attendance_db(record)
        mbox.showinfo("Success", f"Attendance marked for {emp_id} as {status}.")
        win.destroy()
    ctk.CTkButton(win, text="Submit", command=submit_attendance).pack(pady=20)

def view_attendance_gui():
    win = ctk.CTkToplevel(root)
    win.title("View Attendance")
    win.geometry("900x500")
    win.attributes("-topmost", True)
    from data.storage import get_attendance
    records = get_attendance()
    columns = ["Emp ID", "Date", "Status"]
    table = ctk.CTkFrame(win)
    table.pack(pady=10, padx=10, fill="both", expand=True)
    # Header
    for j, col in enumerate(columns):
        ctk.CTkLabel(table, text=col, font=("Arial", 12, "bold"), width=20).grid(row=0, column=j, padx=2, pady=2)
    # Data rows
    for i, rec in enumerate(records, start=1):
        values = ['id', 'date', 'status']
        for j, value in enumerate(values):
            ctk.CTkLabel(table, text=rec.get(value, ''), width=20).grid(row=i, column=j, padx=2, pady=2)
    if not records:
        ctk.CTkLabel(table, text="No attendance records found.", font=("Arial", 14)).grid(row=1, column=0, columnspan=len(columns), pady=20)

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
