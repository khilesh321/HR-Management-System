from pymongo import MongoClient

# MongoDB connection (local, default port)
client = MongoClient('mongodb://localhost:27017/')
db = client['hr_management']

# Collections
employees_col = db['employees']
attendance_col = db['attendance']
leave_col = db['leave']

def get_employees(query=None):
    if query is None:
        query = {}
    return list(employees_col.find(query, {'_id': 0}))

def add_employee_db(employee):
    employees_col.insert_one(employee)

def remove_employee_db(emp_id):
    employees_col.delete_one({'id': emp_id})

def get_attendance(query=None):
    if query is None:
        query = {}
    return list(attendance_col.find(query, {'_id': 0}))

def add_attendance_db(record):
    attendance_col.insert_one(record)

def get_leaves(query=None):
    if query is None:
        query = {}
    return list(leave_col.find(query, {'_id': 0}))

def add_leave_db(leave):
    leave_col.insert_one(leave)

def update_leave_status(emp_id, date, status):
    leave_col.update_one({'id': emp_id, 'date': date}, {'$set': {'status': status}})

def remove_leave_db(emp_id, date):
    leave_col.delete_one({'id': emp_id, 'date': date})
