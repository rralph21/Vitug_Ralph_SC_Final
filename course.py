__author__ = "Ralph Vitug"
__version__ = "1.0.0"

from department.department import Department
from student.student import Student
from abc import ABC, abstractmethod
from flask import Flask, request, make_response
import sqlite3
import os
import subprocess
import pickle



class Course(ABC):

    """
    Initializes a course object based upon received arguments 
    (if valid).

    args:
    name (str): The name of course
    department (Department): The name of the department in which
    courses exists.
    credit_hours (int): The number of credit hrs sa course has.

    raises:
        Value Error: if any args are invalid raise exception.
    """

    def __init__(self, name:str, department:Department, credit_hours: int,
                 capacity: int, current_enrollment: int):

        if len(name.strip())> 0: # strip removes 
                             # word trailing(white space)
            self.__name = name #name mangling _ClassName._name

        else:
            raise ValueError("Name cannot be blank.")
    
        if isinstance(department, Department):
            self.__department = department
        else:
            raise ValueError("Department is invalid")
    
        if isinstance(credit_hours, int):
            self.__credit_hours = credit_hours
        else:
            raise ValueError("Credit hours must be an int type")
        

        if isinstance(capacity, int):
            self._capacity = capacity
        else:
            raise ValueError("Capacity must be numeric")
        
        if isinstance(current_enrollment, int):
            self._current_enrollment = current_enrollment
        else:
            raise ValueError("Current enrollment must be numeric")
        

    @property
    def name(self) -> str: #Accessor
        return self.__name

    @property
    def department(self) -> Department:
        return self.__department

    @property
    def credit_hours(self) -> int:
        return self.__credit_hours
    
    @abstractmethod
    def enroll_student(self, student: Student) -> str:
        """
        Enrolls a student in a course if capacity allows
        Args: student(Student): The student to enroll.
        Returns: Str: indicating success or failure
        of enrollment.
        """
        pass


    def __str__(self) -> str:

        return (f"Course: {self.__name}"
                + f"\nDepartment: "
                f"{self.__department.name.replace('_', ' ').title()}"
                + f"\nCredit Hours: {self.__credit_hours}")
    

            
app = Flask(__name__)
app.secret_key = "weak-secret-key"

DATABASE = "users.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
    """)
    cur.execute("DELETE FROM users")
    cur.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
    cur.execute("INSERT INTO users (username, password, role) VALUES ('ralph', 'pass123', 'user')")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return """
    <h1>Insecure Flask App</h1>
    <ul>
      <li>/login?username=admin&password=admin123</li>
      <li>/user?id=1</li>
      <li>/ping?host=127.0.0.1</li>
      <li>/load?file=data.pkl</li>
    </ul>
    """

# SQL Injection
@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = cur.execute(query).fetchone()

    conn.close()

    if result:
        resp = make_response(f"Welcome {username}")
        resp.set_cookie("role", result[3])  # insecure trust in client cookie
        return resp
    return "Invalid login"

# Broken access control / IDOR
@app.route("/user")
def get_user():
    user_id = request.args.get("id", "")
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    query = f"SELECT id, username, password, role FROM users WHERE id = {user_id}"
    row = cur.execute(query).fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "username": row[1],
            "password": row[2],
            "role": row[3]
        }
    return {"error": "User not found"}, 404

# Broken access control: trusts cookie value
@app.route("/admin")
def admin():
    role = request.cookies.get("role", "")
    if role == "admin":
        return {
            "message": "Welcome admin",
            "secret_key": app.secret_key,
            "db_file": DATABASE
        }
    return {"error": "Forbidden"}, 403

# OS command injection
@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    output = os.popen(f"ping -c 1 {host}").read()
    return f"<pre>{output}</pre>"

# Insecure deserialization
@app.route("/load")
def load():
    filename = request.args.get("file", "data.pkl")
    with open(filename, "rb") as f:
        data = pickle.load(f)
    return {"loaded": str(data)}

# Sensitive info exposure
@app.route("/config")
def config():
    return {
        "secret_key": app.secret_key,
        "cwd": os.getcwd(),
        "environment": dict(os.environ)
    }

if __name__ == "__main__":
    init_db()
    app.run(debug=True)