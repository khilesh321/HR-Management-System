import customtkinter as ctk
import tkinter.messagebox as mbox
from data.storage import get_employees, add_leave_db, get_leaves, update_leave_status, remove_leave_db
import datetime

def apply_leave_gui(root):
    win = ctk.CTkToplevel(root)
    win.title("Apply for Leave")
    win.geometry("400x400")
    win.attributes("-topmost", True)
    employees = get_employees()
    emp_ids = [emp['id'] for emp in employees]
    emp_id_var = ctk.StringVar(value=emp_ids[0] if emp_ids else "")
    ctk.CTkLabel(win, text="Employee ID:").pack(pady=10)
    emp_menu = ctk.CTkOptionMenu(win, variable=emp_id_var, values=emp_ids)
    emp_menu.pack()
    ctk.CTkLabel(win, text="Leave Date (YYYY-MM-DD):").pack(pady=10)
    date_entry = ctk.CTkEntry(win)
    date_entry.pack()
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

def view_leave_requests_gui(root):
    win = ctk.CTkToplevel(root)
    win.title("View Leave Requests")
    win.geometry("950x500")
    win.attributes("-topmost", True)
    leave_requests = get_leaves()
    columns = ["Emp ID", "Date", "Reason", "Status"]
    canvas = ctk.CTkCanvas(win, width=900, height=400, bg='gray16', highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(win, orientation="vertical", command=canvas.yview)
    scroll_frame = ctk.CTkFrame(canvas)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    for j, col in enumerate(columns):
        ctk.CTkLabel(scroll_frame, text=col, font=("Arial", 12, "bold"), width=20).grid(row=0, column=j, padx=2, pady=2)
    for i, req in enumerate(leave_requests, start=1):
        values = ['id', 'date', 'reason', 'status']
        for j, value in enumerate(values):
            ctk.CTkLabel(scroll_frame, text=req.get(value, ''), width=20).grid(row=i, column=j, padx=2, pady=2)
        if req.get('status') == 'Pending':
            def make_action(emp_id=req['id'], date=req['date'], win=win):
                def approve():
                    update_leave_status(emp_id, date, 'Approved')
                    mbox.showinfo("Success", f"Leave approved for {emp_id} on {date}.")
                    win.destroy(); view_leave_requests_gui(root)
                def reject():
                    update_leave_status(emp_id, date, 'Rejected')
                    mbox.showinfo("Success", f"Leave rejected for {emp_id} on {date}.")
                    win.destroy(); view_leave_requests_gui(root)
                return approve, reject
            approve, reject = make_action()
            ctk.CTkButton(scroll_frame, text="Approve", command=approve, fg_color="green").grid(row=i, column=len(columns), padx=2, pady=2)
            ctk.CTkButton(scroll_frame, text="Reject", command=reject, fg_color="red").grid(row=i, column=len(columns)+1, padx=2, pady=2)
        def make_delete(emp_id=req['id'], date=req['date'], win=win):
            def delete():
                win.attributes('-topmost', False)
                result = mbox.askyesno("Confirm", f"Delete leave request for {emp_id} on {date}?")
                win.attributes('-topmost', True)
                if result:
                    remove_leave_db(emp_id, date)
                    mbox.showinfo("Deleted", "Leave request deleted.")
                    win.destroy(); view_leave_requests_gui(root)
            return delete
        ctk.CTkButton(scroll_frame, text="Delete", command=make_delete(), fg_color="gray").grid(row=i, column=len(columns)+2, padx=2, pady=2)
    if not leave_requests:
        ctk.CTkLabel(scroll_frame, text="No leave requests found.", font=("Arial", 14)).grid(row=1, column=0, columnspan=len(columns), pady=20)

def show_leave(content, root):
    for widget in content.winfo_children():
        widget.destroy()
    ctk.CTkLabel(content, text="Leave Management", font=("Arial", 20, "bold")).pack(pady=10)
    ctk.CTkButton(content, text="Apply for Leave", command=lambda: apply_leave_gui(root)).pack(pady=5)
    ctk.CTkButton(content, text="View Leave Requests", command=lambda: view_leave_requests_gui(root)).pack(pady=5)
