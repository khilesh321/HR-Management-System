import customtkinter as ctk
import tkinter.messagebox as mbox
from data.storage import add_employee_db, get_employees
import re, datetime

def add_employee_gui(root):
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
        emp_id = entries['id'].get().strip()
        name = entries['name'].get().strip()
        email = entries['email'].get().strip()
        phone = entries['phone'].get().strip()
        department = entries['department'].get().strip()
        designation = entries['designation'].get().strip()
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

def view_employees_gui(root):
    win = ctk.CTkToplevel(root)
    win.title("View Employees")
    win.geometry("950x500")
    win.attributes("-topmost", True)
    employees = get_employees()
    columns = ["ID", "Name", "Email", "Phone", "Department", "Designation", "Date Joined"]
    canvas = ctk.CTkCanvas(win, width=900, height=400, highlightthickness=0, bg='gray16')
    scrollbar = ctk.CTkScrollbar(win, orientation="vertical", command=canvas.yview)
    scroll_frame = ctk.CTkFrame(canvas)
    scroll_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    for j, col in enumerate(columns):
        ctk.CTkLabel(scroll_frame, text=col, font=("Arial", 12, "bold"), width=15).grid(row=0, column=j, padx=2, pady=2)
    for i, emp in enumerate(employees, start=1):
        for j, key in enumerate(['id', 'name', 'email', 'phone', 'department', 'designation', 'date_joined']):
            ctk.CTkLabel(scroll_frame, text=emp.get(key, ''), width=15).grid(row=i, column=j, padx=2, pady=2)
    if not employees:
        ctk.CTkLabel(scroll_frame, text="No employees found.", font=("Arial", 14)).grid(row=1, column=0, columnspan=len(columns), pady=20)
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

def remove_employee_gui(root):
    import tkinter.messagebox as mbox
    from data.storage import get_employees, remove_employee_db
    win = ctk.CTkToplevel(root)
    win.title("Remove Employee")
    win.geometry("400x200")
    win.attributes("-topmost", True)
    ctk.CTkLabel(win, text="Enter Employee ID to remove:").pack(pady=10)
    emp_id_entry = ctk.CTkEntry(win)
    emp_id_entry.pack(pady=5)
    def submit_remove():
        emp_id = emp_id_entry.get().strip()
        employees = get_employees({'id': emp_id})
        if not employees:
            mbox.showerror("Error", "Employee not found.")
            return
        emp = employees[0]
        confirm = mbox.askyesno("Confirm", f"Are you sure you want to remove {emp['name']}?")
        if confirm:
            remove_employee_db(emp_id)
            mbox.showinfo("Success", f"Employee '{emp['name']}' removed successfully!")
            win.destroy()
    ctk.CTkButton(win, text="Remove", command=submit_remove).pack(pady=15)

def update_employee_gui(root):
    import tkinter.messagebox as mbox
    from data.storage import get_employees, employees_col
    import re
    win = ctk.CTkToplevel(root)
    win.title("Update Employee")
    win.geometry("400x570")
    win.attributes("-topmost", True)
    ctk.CTkLabel(win, text="Enter Employee ID to update:").pack(pady=10)
    emp_id_entry = ctk.CTkEntry(win)
    emp_id_entry.pack(pady=5)
    form_frame = ctk.CTkFrame(win)
    def load_employee():
        emp_id = emp_id_entry.get().strip()
        employees = get_employees({'id': emp_id})
        if not employees:
            mbox.showerror("Error", "Employee not found.")
            return
        emp = employees[0]
        for widget in form_frame.winfo_children():
            widget.destroy()
        fields = ["Name", "Email", "Phone", "Department", "Designation"]
        entries = {}
        for i, field in enumerate(fields):
            ctk.CTkLabel(form_frame, text=field + ":").pack(pady=(10 if i == 0 else 5, 0))
            entry = ctk.CTkEntry(form_frame)
            entry.insert(0, emp[field.lower()])
            entry.pack(fill="x", padx=10)
            entries[field.lower()] = entry
        def submit_update():
            name = entries['name'].get().strip()
            email = entries['email'].get().strip()
            phone = entries['phone'].get().strip()
            department = entries['department'].get().strip()
            designation = entries['designation'].get().strip()
            if not name:
                mbox.showerror("Error", "Name cannot be empty!")
                return
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                mbox.showerror("Error", "Invalid email format!")
                return
            if not re.match(r"^\d{10}$", phone):
                mbox.showerror("Error", "Invalid phone number! Must be 10 digits.")
                return
            employees_col.update_one({'id': emp_id}, {'$set': {
                'name': name,
                'email': email,
                'phone': phone,
                'department': department,
                'designation': designation
            }})
            mbox.showinfo("Success", f"Employee '{emp_id}' updated successfully!")
            win.destroy()
        ctk.CTkButton(form_frame, text="Update", command=submit_update).pack(pady=15)
        form_frame.pack(pady=10, padx=10, fill="both", expand=True)
    ctk.CTkButton(win, text="Load", command=load_employee).pack(pady=10)

def show_employees(content, root):
    for widget in content.winfo_children():
        widget.destroy()
    ctk.CTkLabel(content, text="Employee Management", font=("Arial", 20, "bold")).pack(pady=10)
    ctk.CTkButton(content, text="Add Employee", command=lambda: add_employee_gui(root)).pack(pady=5)
    ctk.CTkButton(content, text="View Employees", command=lambda: view_employees_gui(root)).pack(pady=5)
    ctk.CTkButton(content, text="Remove Employee", command=lambda: remove_employee_gui(root)).pack(pady=5)
    ctk.CTkButton(content, text="Update Employee", command=lambda: update_employee_gui(root)).pack(pady=5)

