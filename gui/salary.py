import customtkinter as ctk
import tkinter.messagebox as mbox
from data.storage import get_employees, get_attendance

def calculate_salary_gui(root):
    win = ctk.CTkToplevel(root)
    win.title("Calculate Salary")
    win.geometry("400x400")
    win.attributes("-topmost", True)
    employees = get_employees()
    emp_ids = [emp['id'] for emp in employees]
    emp_id_var = ctk.StringVar(value=emp_ids[0] if emp_ids else "")
    ctk.CTkLabel(win, text="Employee ID:").pack(pady=10)
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
        if absent_days <= 5 and present_days > 25:
            bonus = 0.05 * base_salary
        salary = (per_day * present_days) + bonus
        slip = f"\nSalary Slip for {emp['name']} ({emp_id})\n"
        slip += f"Base Salary: {base_salary:.2f}\nPresent Days: {present_days}\nAbsent Days: {absent_days}\nDeduction: {deduction:.2f}\nBonus: {bonus:.2f}\nNet Salary: {salary:.2f}"
        mbox.showinfo("Salary Slip", slip)
        win.destroy()
    ctk.CTkButton(win, text="Calculate", command=submit_salary).pack(pady=20)

def show_salary(content, root):
    for widget in content.winfo_children():
        widget.destroy()
    ctk.CTkLabel(content, text="Salary Calculation", font=("Arial", 20, "bold")).pack(pady=10)
    ctk.CTkButton(content, text="Calculate Salary", command=lambda: calculate_salary_gui(root)).pack(pady=5)
