import customtkinter as ctk
from gui.employees import show_employees
from gui.attendance import show_attendance
from gui.leave import show_leave
from gui.salary import show_salary

ctk.set_appearance_mode("dark")
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

ctk.CTkButton(sidebar, text="Employees", command=lambda: show_employees(content, root)).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Attendance", command=lambda: show_attendance(content, root)).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Leave", command=lambda: show_leave(content, root)).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Salary", command=lambda: show_salary(content, root)).pack(pady=10, fill="x")

show_employees(content, root)
root.mainloop()
