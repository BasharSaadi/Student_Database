import psycopg2
from psycopg2 import Error
import sys


# ============================================
# Database Configuration
# ============================================

# Database connection parameters
# Update these values to match your PostgreSQL configuration
DB_CONFIG = {
    'host': 'localhost',        
    'database': 'students_table',  
    'user': 'postgres',         
    'password': 'your_password' # Database password
}


# ============================================
# Database Connection Helper
# ============================================

def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    
    Returns:
        connection: psycopg2 connection object if successful
        None: if connection fails
    
    Raises:
        Error: If unable to connect to the database
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None


# ============================================
# CRUD Operations
# ============================================

def getAllStudents():
    """
    Retrieves and displays all records from the students table.
    
    This function:
    1. Connects to the database
    2. Executes a SELECT query to fetch all student records
    3. Displays the results in a formatted table
    4. Handles any errors that occur during the operation
    
    Returns:
        None
    """
    connection = None
    cursor = None
    
    try:
        # Establish database connection
        connection = get_db_connection()
        if connection is None:
            return
        
        # Create a cursor object to execute queries
        cursor = connection.cursor()
        
        # SQL query to select all students, ordered by student_id
        query = """
            SELECT student_id, first_name, last_name, email, enrollment_date 
            FROM students 
            ORDER BY student_id;
        """
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all results
        students = cursor.fetchall()
        
        # Display results
        if students:
            print("\n" + "="*80)
            print("ALL STUDENTS")
            print("="*80)
            print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30} {'Enrollment Date':<15}")
            print("-"*80)
            
            for student in students:
                student_id, first_name, last_name, email, enrollment_date = student
                enrollment_str = enrollment_date.strftime('%Y-%m-%d') if enrollment_date else 'N/A'
                print(f"{student_id:<5} {first_name:<15} {last_name:<15} {email:<30} {enrollment_str:<15}")
            
            print("="*80)
            print(f"Total students: {len(students)}\n")
        else:
            print("\nNo students found in the database.\n")
    
    except Error as e:
        print(f"Error retrieving students: {e}")
    
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def addStudent(first_name, last_name, email, enrollment_date):
    """
    Inserts a new student record into the students table.
    
    Args:
        first_name (str): Student's first name
        last_name (str): Student's last name
        email (str): Student's email address (must be unique)
        enrollment_date (str): Enrollment date in 'YYYY-MM-DD' format
    
    Returns:
        bool: True if insertion successful, False otherwise
    """
    connection = None
    cursor = None
    
    try:
        # Validate inputs
        if not all([first_name, last_name, email]):
            print("Error: First name, last name, and email are required.")
            return False
        
        # Establish database connection
        connection = get_db_connection()
        if connection is None:
            return False
        
        # Create cursor
        cursor = connection.cursor()
        
        # SQL query to insert a new student
        # Using parameterized query to prevent SQL injection
        query = """
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
            RETURNING student_id;
        """
        
        # Execute the query with parameters
        cursor.execute(query, (first_name, last_name, email, enrollment_date))
        
        # Get the ID of the newly inserted student
        new_student_id = cursor.fetchone()[0]
        
        # Commit the transaction
        connection.commit()
        
        print(f"\n✓ Student added successfully!")
        print(f"  Student ID: {new_student_id}")
        print(f"  Name: {first_name} {last_name}")
        print(f"  Email: {email}")
        print(f"  Enrollment Date: {enrollment_date}\n")
        
        return True
    
    except psycopg2.IntegrityError as e:
        # Handle unique constraint violation (duplicate email)
        if connection:
            connection.rollback()
        print(f"\n✗ Error: Email '{email}' already exists in the database.\n")
        return False
    
    except Error as e:
        # Handle other database errors
        if connection:
            connection.rollback()
        print(f"\n✗ Error adding student: {e}\n")
        return False
    
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def updateStudentEmail(student_id, new_email):
    """
    Updates the email address for a student with the specified student_id.
    
    Args:
        student_id (int): The ID of the student to update
        new_email (str): The new email address
    
    Returns:
        bool: True if update successful, False otherwise
    """
    connection = None
    cursor = None
    
    try:
        # Validate inputs
        if not new_email:
            print("Error: New email is required.")
            return False
        
        # Establish database connection
        connection = get_db_connection()
        if connection is None:
            return False
        
        # Create cursor
        cursor = connection.cursor()
        
        # First, check if the student exists
        check_query = "SELECT first_name, last_name, email FROM students WHERE student_id = %s;"
        cursor.execute(check_query, (student_id,))
        student = cursor.fetchone()
        
        if not student:
            print(f"\n✗ Error: No student found with ID {student_id}.\n")
            return False
        
        old_first_name, old_last_name, old_email = student
        
        # SQL query to update student email
        update_query = """
            UPDATE students 
            SET email = %s 
            WHERE student_id = %s;
        """
        
        # Execute the update
        cursor.execute(update_query, (new_email, student_id))
        
        # Commit the transaction
        connection.commit()
        
        # Check if any rows were affected
        if cursor.rowcount > 0:
            print(f"\n✓ Email updated successfully!")
            print(f"  Student ID: {student_id}")
            print(f"  Name: {old_first_name} {old_last_name}")
            print(f"  Old Email: {old_email}")
            print(f"  New Email: {new_email}\n")
            return True
        else:
            print(f"\n✗ No changes made.\n")
            return False
    
    except psycopg2.IntegrityError as e:
        # Handle unique constraint violation (duplicate email)
        if connection:
            connection.rollback()
        print(f"\n✗ Error: Email '{new_email}' already exists in the database.\n")
        return False
    
    except Error as e:
        if connection:
            connection.rollback()
        print(f"\n✗ Error updating student email: {e}\n")
        return False
    
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def deleteStudent(student_id):
    """
    Deletes the record of the student with the specified student_id.
    
    Args:
        student_id (int): The ID of the student to delete
    
    Returns:
        bool: True if deletion successful, False otherwise
    """
    connection = None
    cursor = None
    
    try:
        # Establish database connection
        connection = get_db_connection()
        if connection is None:
            return False
        
        # Create cursor
        cursor = connection.cursor()
        
        # First, get student details before deletion
        check_query = "SELECT first_name, last_name, email FROM students WHERE student_id = %s;"
        cursor.execute(check_query, (student_id,))
        student = cursor.fetchone()
        
        if not student:
            print(f"\n✗ Error: No student found with ID {student_id}.\n")
            return False
        
        first_name, last_name, email = student
        
        # SQL query to delete the student
        delete_query = "DELETE FROM students WHERE student_id = %s;"
        
        # Execute the deletion
        cursor.execute(delete_query, (student_id,))
        
        # Commit the transaction
        connection.commit()
        
        # Verify deletion
        if cursor.rowcount > 0:
            print(f"\n✓ Student deleted successfully!")
            print(f"  Student ID: {student_id}")
            print(f"  Name: {first_name} {last_name}")
            print(f"  Email: {email}\n")
            return True
        else:
            print(f"\n✗ No student was deleted.\n")
            return False
    
    except Error as e:
        if connection:
            connection.rollback()
        print(f"\n✗ Error deleting student: {e}\n")
        return False
    
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ============================================
# Interactive Menu System
# ============================================

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("STUDENT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. View all students")
    print("2. Add a new student")
    print("3. Update student email")
    print("4. Delete a student")
    print("5. Exit")
    print("="*50)


def main():
    """
    Main function that runs the interactive menu system.
    Allows users to perform CRUD operations through a command-line interface.
    """
    print("\nWelcome to the Student Databse Management System!")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            # View all students
            getAllStudents()
        
        elif choice == '2':
            # Add a new student
            print("\n--- Add New Student ---")
            first_name = input("Enter first name: ").strip()
            last_name = input("Enter last name: ").strip()
            email = input("Enter email: ").strip()
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ").strip()
            
            addStudent(first_name, last_name, email, enrollment_date)
        
        elif choice == '3':
            # Update student email
            print("\n--- Update Student Email ---")
            try:
                student_id = int(input("Enter student ID: ").strip())
                new_email = input("Enter new email: ").strip()
                updateStudentEmail(student_id, new_email)
            except ValueError:
                print("\n✗ Error: Student ID must be a number.\n")
        
        elif choice == '4':
            # Delete a student
            print("\n--- Delete Student ---")
            try:
                student_id = int(input("Enter student ID to delete: ").strip())
                confirm = input(f"Are you sure you want to delete student {student_id}? (yes/no): ").strip().lower()
                
                if confirm == 'yes':
                    deleteStudent(student_id)
                else:
                    print("\nDeletion cancelled.\n")
            except ValueError:
                print("\n✗ Error: Student ID must be a number.\n")
        
        elif choice == '5':
            # Exit
            print("\nThank you for using the Student Management System. Goodbye!\n")
            sys.exit(0)
        
        else:
            print("\n✗ Invalid choice. Please enter a number between 1 and 5.\n")


# ============================================
# Entry Point
# ============================================

if __name__ == "__main__":
    main()
    deleteStudent(3)
