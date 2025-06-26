import customtkinter as ctk
import tkinter.messagebox as mbox
from data.storage import get_employees, add_attendance_db, get_attendance
import datetime

def mark_attendance_gui(root):
    win = ctk.CTkToplevel(root)
    win.title("Mark Attendance")
    win.geometry("400x300")
    win.attributes("-topmost", True)
    employees = get_employees()
    emp_ids = [emp['id'] for emp in employees]
    emp_id_var = ctk.StringVar(value=emp_ids[0] if emp_ids else "")
    ctk.CTkLabel(win, text="Employee ID:").pack(pady=10)
    emp_menu = ctk.CTkOptionMenu(win, variable=emp_id_var, values=emp_ids)
    emp_menu.pack()
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

def view_attendance_gui(root):
    win = ctk.CTkToplevel(root)
    win.title("View Attendance")
    win.geometry("900x500")
    win.attributes("-topmost", True)
    records = get_attendance()
    columns = ["Emp ID", "Date", "Status"]
    table = ctk.CTkFrame(win)
    table.pack(pady=10, padx=10, fill="both", expand=True)
    for j, col in enumerate(columns):
        ctk.CTkLabel(table, text=col, font=("Arial", 12, "bold"), width=20).grid(row=0, column=j, padx=2, pady=2)
    for i, rec in enumerate(records, start=1):
        values = ['id', 'date', 'status']
        for j, value in enumerate(values):
            ctk.CTkLabel(table, text=rec.get(value, ''), width=20).grid(row=i, column=j, padx=2, pady=2)
    if not records:
        ctk.CTkLabel(table, text="No attendance records found.", font=("Arial", 14)).grid(row=1, column=0, columnspan=len(columns), pady=20)

def show_attendance(content, root):
    for widget in content.winfo_children():
        widget.destroy()
    ctk.CTkLabel(content, text="Attendance Management", font=("Arial", 20, "bold")).pack(pady=10)
    ctk.CTkButton(content, text="Mark Attendance", command=lambda: mark_attendance_gui(root)).pack(pady=5)
    ctk.CTkButton(content, text="View Attendance", command=lambda: view_attendance_gui(root)).pack(pady=5)
