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
    win.geometry("950x500")
    win.attributes("-topmost", True)
    from data.storage import get_employees
    employees = get_employees()
    columns = ["ID", "Name", "Email", "Phone", "Department", "Designation", "Date Joined"]
    # Add a scrollable frame
    canvas = ctk.CTkCanvas(win, width=900, height=400)
    scrollbar = ctk.CTkScrollbar(win, orientation="vertical", command=canvas.yview)
    scroll_frame = ctk.CTkFrame(canvas)
    scroll_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    # Header
    for j, col in enumerate(columns):
        ctk.CTkLabel(scroll_frame, text=col, font=("Arial", 12, "bold"), width=15).grid(row=0, column=j, padx=2, pady=2)
    # Data rows
    for i, emp in enumerate(employees, start=1):
        for j, key in enumerate(['id', 'name', 'email', 'phone', 'department', 'designation', 'date_joined']):
            ctk.CTkLabel(scroll_frame, text=emp.get(key, ''), width=15).grid(row=i, column=j, padx=2, pady=2)
    if not employees:
        ctk.CTkLabel(scroll_frame, text="No employees found.", font=("Arial", 14)).grid(row=1, column=0, columnspan=len(columns), pady=20)
    # Search bar
    def search_employees():
        query = search_entry.get().strip().lower()
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        for j, col in enumerate(columns):
            ctk.CTkLabel(scroll_frame, text=col, font=("Arial", 12, "bold"), width=15).grid(row=0, column=j, padx=2, pady=2)
        filtered = [emp for emp in employees if query in emp.get('name', '').lower() or query in emp.get('id', '').lower()]
        for i, emp in enumerate(filtered, start=1):
            for j, key in enumerate(['id', 'name', 'email', 'phone', 'department', 'designation', 'date_joined']):
                ctk.CTkLabel(scroll_frame, text=emp.get(key, ''), width=15).grid(row=i, column=j, padx=2, pady=2)
        if not filtered:
            ctk.CTkLabel(scroll_frame, text="No employees found.", font=("Arial", 14)).grid(row=1, column=0, columnspan=len(columns), pady=20)
    search_entry = ctk.CTkEntry(win, width=30)
    search_entry.pack(side="top", pady=5)
    ctk.CTkButton(win, text="Search", command=search_employees).pack(side="top")

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
    ctk.CTkLabel(content, text="Leave Management", font=("Arial", 20, "bold")).pack(pady=10)
    ctk.CTkButton(content, text="Apply for Leave", command=apply_leave_gui).pack(pady=5)
    ctk.CTkButton(content, text="View Leave Requests", command=view_leave_requests_gui).pack(pady=5)

def apply_leave_gui():
    win = ctk.CTkToplevel(root)
    win.title("Apply for Leave")
    win.geometry("400x400")
    win.attributes("-topmost", True)
    from data.storage import get_employees, add_leave_db, get_leaves
    import datetime
    # Employee ID dropdown
    ctk.CTkLabel(win, text="Employee ID:").pack(pady=10)
    employees = get_employees()
    emp_ids = [emp['id'] for emp in employees]
    emp_id_var = ctk.StringVar(value=emp_ids[0] if emp_ids else "")
    emp_menu = ctk.CTkOptionMenu(win, variable=emp_id_var, values=emp_ids)
    emp_menu.pack()
    # Date
    ctk.CTkLabel(win, text="Leave Date (YYYY-MM-DD):").pack(pady=10)
    date_entry = ctk.CTkEntry(win)
    date_entry.pack()
    # Reason
    ctk.CTkLabel(win, text="Reason:").pack(pady=10)
    reason_entry = ctk.CTkEntry(win)
    reason_entry.pack()
    def submit_leave():
        emp_id = emp_id_var.get()
        date = date_entry.get().strip()
        reason = reason_entry.get().strip()
        if not emp_id:
            mbox.showerror("Error", "Please select an Employee ID.")
            return
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            mbox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
            return
        from data.storage import get_leaves
        if get_leaves({'id': emp_id, 'date': date}):
            mbox.showerror("Error", "Leave request for this date already exists!")
            return
        if not reason:
            mbox.showerror("Error", "Reason cannot be empty!")
            return
        leave = {"id": emp_id, "date": date, "reason": reason, "status": "Pending"}
        add_leave_db(leave)
        mbox.showinfo("Success", f"Leave request submitted for {emp_id} on {date}.")
        win.destroy()
    ctk.CTkButton(win, text="Submit", command=submit_leave).pack(pady=20)

def view_leave_requests_gui():
    win = ctk.CTkToplevel(root)
    win.title("View Leave Requests")
    win.geometry("950x500")
    win.attributes("-topmost", True)
    from data.storage import get_leaves, update_leave_status, remove_leave_db
    leave_requests = get_leaves()
    columns = ["Emp ID", "Date", "Reason", "Status"]
    # Add a scrollable frame
    canvas = ctk.CTkCanvas(win, width=900, height=400)
    scrollbar = ctk.CTkScrollbar(win, orientation="vertical", command=canvas.yview)
    scroll_frame = ctk.CTkFrame(canvas)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    # Header
    for j, col in enumerate(columns):
        ctk.CTkLabel(scroll_frame, text=col, font=("Arial", 12, "bold"), width=20).grid(row=0, column=j, padx=2, pady=2)
    for i, req in enumerate(leave_requests, start=1):
        values = ['id', 'date', 'reason', 'status']
        for j, value in enumerate(values):
            ctk.CTkLabel(scroll_frame, text=req.get(value, ''), width=20).grid(row=i, column=j, padx=2, pady=2)
        # Approve/Reject buttons for pending requests
        if req.get('status') == 'Pending':
            def make_action(emp_id=req['id'], date=req['date'], win=win):
                def approve():
                    update_leave_status(emp_id, date, 'Approved')
                    mbox.showinfo("Success", f"Leave approved for {emp_id} on {date}.")
                    win.destroy(); view_leave_requests_gui()
                def reject():
                    update_leave_status(emp_id, date, 'Rejected')
                    mbox.showinfo("Success", f"Leave rejected for {emp_id} on {date}.")
                    win.destroy(); view_leave_requests_gui()
                return approve, reject
            approve, reject = make_action()
            ctk.CTkButton(scroll_frame, text="Approve", command=approve, fg_color="green").grid(row=i, column=len(columns), padx=2, pady=2)
            ctk.CTkButton(scroll_frame, text="Reject", command=reject, fg_color="red").grid(row=i, column=len(columns)+1, padx=2, pady=2)
        # Delete button for all requests
        def make_delete(emp_id=req['id'], date=req['date'], win=win):
            def delete():
                # Hide the main window before showing the messagebox
                win.attributes('-topmost', False)
                result = mbox.askyesno("Confirm", f"Delete leave request for {emp_id} on {date}?")
                win.attributes('-topmost', True)
                if result:
                    remove_leave_db(emp_id, date)
                    mbox.showinfo("Deleted", "Leave request deleted.")
                    win.destroy(); view_leave_requests_gui()
            return delete
        ctk.CTkButton(scroll_frame, text="Delete", command=make_delete(), fg_color="gray").grid(row=i, column=len(columns)+2, padx=2, pady=2)
    if not leave_requests:
        ctk.CTkLabel(scroll_frame, text="No leave requests found.", font=("Arial", 14)).grid(row=1, column=0, columnspan=len(columns), pady=20)

def show_salary():
    clear_content()
    ctk.CTkLabel(content, text="Salary Calculation", font=("Arial", 20, "bold")).pack(pady=10)
    ctk.CTkButton(content, text="Calculate Salary", command=calculate_salary_gui).pack(pady=5)

def calculate_salary_gui():
    win = ctk.CTkToplevel(root)
    win.title("Calculate Salary")
    win.geometry("400x400")
    win.attributes("-topmost", True)
    from data.storage import get_employees, get_attendance
    ctk.CTkLabel(win, text="Employee ID:").pack(pady=10)
    employees = get_employees()
    emp_ids = [emp['id'] for emp in employees]
    emp_id_var = ctk.StringVar(value=emp_ids[0] if emp_ids else "")
    emp_menu = ctk.CTkOptionMenu(win, variable=emp_id_var, values=emp_ids)
    emp_menu.pack()
    ctk.CTkLabel(win, text="Base Salary (default 20000):").pack(pady=10)
    base_salary_entry = ctk.CTkEntry(win)
    base_salary_entry.pack()
    def submit_salary():
        emp_id = emp_id_var.get()
        try:
            base_salary = float(base_salary_entry.get() or 20000)
        except ValueError:
            mbox.showerror("Error", "Invalid salary input!")
            return
        employees = get_employees({'id': emp_id})
        if not employees:
            mbox.showerror("Error", "Employee not found!")
            return
        emp = employees[0]
        attendance_records = get_attendance({'id': emp_id})
        present_days = sum(1 for rec in attendance_records if rec["status"] == "Present")
        absent_days = sum(1 for rec in attendance_records if rec["status"] == "Absent")
        per_day = base_salary / 30
        deduction = per_day * absent_days
        bonus = 0
        if absent_days == 0 and present_days > 0:
            bonus = 0.05 * base_salary
        salary = (per_day * present_days) + bonus
        slip = f"\nSalary Slip for {emp['name']} ({emp_id})\n"
        slip += f"Base Salary: {base_salary:.2f}\nPresent Days: {present_days}\nAbsent Days: {absent_days}\nDeduction: {deduction:.2f}\nBonus: {bonus:.2f}\nNet Salary: {salary:.2f}"
        mbox.showinfo("Salary Slip", slip)
        win.destroy()
    ctk.CTkButton(win, text="Calculate", command=submit_salary).pack(pady=20)

ctk.CTkButton(sidebar, text="Employees", command=show_employees).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Attendance", command=show_attendance).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Leave", command=show_leave).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Salary", command=show_salary).pack(pady=10, fill="x")

show_employees()
root.mainloop()
