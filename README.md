# Student Database System

A Python app that performs CRUD operations on a PostgreSQL database with an interactive menu interface at terminal.

## Author

- Bashar Saadi
- YouTube Link: [coming soon]

## Requirements

- Python 3.7+
- PostgreSQL
- psycopg2

## Setup Instructions

### 1. Install PostgreSQL

Download and install from [postgresql.org](https://www.postgresql.org/download/)

### 2. Install Python Dependencies

```bash
pip install psycopg2-binary
```

### 3. Run Database on pgAdmin 

Edit [student_crud.py](student_crud.py) lines 12-17:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'students_table',  
    'user': 'postgres',            
    'password': 'password'   # enter yours here 
}
```

## 4. Run the Python Script

Navigate to the project directory and run:

```bash
python student_crud.py
```

or

```bash
python3 student_crud.py
```

### Interactive Menu Interface at Terminal

The application provides a menu-driven interface:

```
==================================================
STUDENT MANAGEMENT SYSTEM
==================================================
1. View all students
2. Add a new student
3. Update student email
4. Delete a student
5. Exit
==================================================
```

## Application Functions

### 1. getAllStudents()
Retrieves and displays all student records in a formatted table.

### 2. addStudent(first_name, last_name, email, enrollment_date)
Inserts a new student record into the database.

### 3. updateStudentEmail(student_id, new_email)
Updates the email address for a student.

### 4. deleteStudent(student_id)
Deletes a student record from the database.


