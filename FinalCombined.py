import os
from datetime import datetime

Attendance_File = 'attendance_lect.txt'
Courses_File = 'courses_admin.txt'
AdminDetails_File = 'details_admin.txt'
LectDetails_File = 'details_lect.txt'
RegDetails_File = 'details_reg.txt'
StudentDetails_File = 'details_stud.txt'
AccDetails_File = 'details_acc.txt'
Grades_File = 'grades_lect.txt'
LecturerList_File = 'lecturers_admin.txt'
LectModules_File = 'modules_lect.txt'
StudentClasses_File = 'studentlist_lect.txt'
StudentList_File = 'students_reg.txt'
Fees_File = 'fees.txt'
Receipts_File = 'receipts.txt'

# Beginning of Administrator Part---------------------------------------------------------------------------------------

def admin_login():
    try:
        with open(AdminDetails_File, 'r') as file:
            details = {line.split(',')[0]: line.split(',')[1].strip() for line in file}
    except FileNotFoundError:
        print("Admin file not found.")
        return None

    admin_id = input("Please Enter Admin ID: ")
    password = input("Please Enter Password: ")

    if admin_id in details and details[admin_id] == password:
        print("\nLogin successful")
        return admin_id
    else:
        print("Invalid ID or Password.")
        return None

# Utility Functions
def read_file(file):
    """Reads data from a file, returns it as a list of lists."""
    try:
        with open(file, "r") as f:
            return [line.strip().split(",") for line in f.readlines()]
    except FileNotFoundError:
        open(file, "w").close()  # Create the file if it doesn't exist
        return []

def write_file(file, data):
    """Writes a list of lists to a file."""
    with open(file, "w") as f:
        for line in data:
            f.write(",".join(line) + "\n")


def validate_input_a(prompt, validator, error_msg):
    """Prompt for input until valid."""
    while True:
        try:
            value = input(prompt).strip()
            if validator(value):
                return value
            print(f"{error_msg}")
        except OSError:
            return ""

def get_choice():
    """Get menu choice safely, handling non-interactive environments."""
    try:
        return input("Choose: ").strip()
    except OSError:
        return "7"  # Default to exit in non-interactive mode


def add_student():
    """Add a new student."""
    print("\nAdd New Student")

    students = read_file(StudentList_File)
    existing_ids = {student[0] for student in students}  # Create a set of existing IDs for quick lookup

    while True:
        sid = validate_input_a("Student ID: ",lambda x: x,"ID must be numeric.")
        if sid in existing_ids:
            print(f"Student with ID '{sid}' already exists. Please try again.")
        else:
            break

    name = validate_input_a("Student Name: ", lambda x: x.strip() != "", "Name cannot be empty.")
    dept = validate_input_a("Department: ", lambda x: x.strip() != "", "Department cannot be empty.")

    students.append([sid, name, dept])
    write_file(StudentList_File, students)
    print(f"Student '{name}' added successfully.")


def remove_student():
    """Remove a student by ID."""
    print("\nRemove Student")
    students = read_file(StudentList_File)
    if not students:
        print("No students found.")
        return
    sid = validate_input_a("Enter Student ID to remove: ", lambda x: x, "ID must be numeric.")
    updated_students = [s for s in students if s[0] != sid]
    if len(updated_students) == len(students):
        print("Student not found.")
    else:
        write_file(StudentList_File, updated_students)
        print(f"Student ID '{sid}' removed.")


def add_course():
    """Add a new course."""
    print("\nAdd New Course")
    code = validate_input_a("Course Code: ", lambda x: x, "Code cannot be empty.")
    name = validate_input_a("Course Name: ", lambda x: x, "Name cannot be empty.")
    course_credits = validate_input_a("Credits (positive number): ", lambda x: x.isdigit() and int(x) > 0, "Credits must be a positive number.")
    courses = read_file(Courses_File)
    courses.append([code, name, course_credits])
    write_file(Courses_File, courses)
    print(f"Course '{name}' added.")


def generate_reports():
    """Generate summary of students, courses, and lecturers."""
    print("\nSystem Report")
    students = read_file(StudentList_File)
    courses = read_file(Courses_File)
    lecturers = read_file(LecturerList_File)
    print(f"Students: {len(students)}  Courses: {len(courses)}  Lecturers: {len(lecturers)}")


def view_all_data():
    """Display all data across students, courses, and lecturers."""
    print("\nAll Data")
    print("\nStudents:")
    students = read_file(StudentList_File)
    if students:
        for student in students:
            print(", ".join(student))
    else:
        print("No student data available.")
    print("\nCourses:")
    courses = read_file(Courses_File)
    if courses:
        for course in courses:
            print(", ".join(course))
    else:
        print("No course data available.")
    print("\nLecturers:")
    lecturers = read_file(LecturerList_File)
    if lecturers:
        for lecturer in lecturers:
            print(", ".join(lecturer))
    else:
        print("No lecturer data available.")


def manage_lecturers():
    """Manage lecturers: Add, Remove, and View."""

    def add_lecturer():
        """Add a new lecturer."""
        print("\nAdd New Lecturer")
        lid = validate_input_a("Lecturer ID: ", lambda x: x, "ID must be numeric.")
        name = validate_input_a("Lecturer Name: ", lambda x: x, "Name cannot be empty.")
        department = validate_input_a("Department: ", lambda x: x, "Department cannot be empty.")
        lecturers = read_file(LecturerList_File)
        lecturers.append([lid, name, department])
        write_file(LecturerList_File, lecturers)
        print(f"Lecturer '{name}' added.")

    def remove_lecturer():
        """Remove a lecturer by ID."""
        print("\nRemove Lecturer")
        lecturers = read_file(LecturerList_File)
        if not lecturers:
            print("No lecturers found.")
            return
        lid = validate_input_a("Enter Lecturer ID to remove: ", lambda x: x, "ID must be numeric.")
        updated_lecturers = [l for l in lecturers if l[0] != lid]
        if len(updated_lecturers) == len(lecturers):
            print("Lecturer not found.")
        else:
            write_file(LecturerList_File, updated_lecturers)
            print(f"Lecturer ID '{lid}' removed.")

    def view_lecturers():
        """View all lecturers."""
        print("\nLecturers:")
        lecturers = read_file(LecturerList_File)
        if lecturers:
            for lecturer in lecturers:
                print(", ".join(lecturer))
        else:
            print("No lecturer data available.")

    # Menu for managing lecturers
    try:
        while True:
            print("\nManage Lecturers:")
            print("1. Add Lecturer")
            print("2. Remove Lecturer")
            print("3. View Lecturers")
            print("4. Back to Admin Menu")

            choice = get_choice()
            if choice == "1":
                add_lecturer()
            elif choice == "2":
                remove_lecturer()
            elif choice == "3":
                view_lecturers()
            elif choice == "4":
                print("\nReturning to Admin Menu.")
                break
            else:
                print("Invalid choice.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully.")


def admin_menu(admin_id):
    """Main menu for administrators."""
    try:
        while True:
            print("\nAdmin Menu:")
            print("1. Add Student")
            print("2. Remove Student")
            print("3. Add New Course")
            print("4. Manage Lecturers")
            print("5. Generate Reports")
            print("6. View All Data")
            print("7. Exit")

            choice = get_choice()
            if choice == "1":
                add_student()
            elif choice == "2":
                remove_student()
            elif choice == "3":
                add_course()
            elif choice == "4":
                manage_lecturers()
            elif choice == "5":
                generate_reports()
            elif choice == "6":
                view_all_data()
            elif choice == "7":
                print("\nExiting Admin Menu. Goodbye!")
                break
            else:
                print("Invalid choice.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully.")

# End of the Administrator Part-----------------------------------------------------------------------------------------
# Beginning of Lecturer Part--------------------------------------------------------------------------------------------

# Entering LecturerID and Password to Access the Lecturer Menu
def lect_login():
    try:
        with open(LectDetails_File, 'r') as file:
            details = {line.split(',')[0]: line.split(',')[1].strip() for line in file}
    except FileNotFoundError:
        print("Lecturer file not found.")
        return None

    lecturer_id = input("Please Enter Lecturer ID: ")
    password = input("Please Enter Password: ")

    if lecturer_id in details and details[lecturer_id] == password:
        print("\nLogin successful")
        return lecturer_id
    else:
        print("Invalid ID or Password.")
        return None

# Main Menu for lecturers to choose what they want to do (Accessible after login)
# Handles input for lecturer part
def lecturer_menu(lecturer_id):
    while True:
        print("\nLecturer Menu")
        print("1. View Assigned Modules")
        print("2. View Student Grades")
        print("3. Record Grades")
        print("4. View Student List")
        print("5. Track Attendance")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            view_assigned_modules(lecturer_id)
        elif choice == '2':
            module_code = input("Enter module code: ")
            view_student_grades(module_code)
        elif choice == '3':
            module_code = input("Enter module code: ")
            student_id = input("Enter student ID: ")
            if len(student_id) == 8:
                break
            else:
                print("Invalid Student ID. Student ID must start with 'TP' and followed by 6 digits")

            grade = input("Enter grade: ")
            record_grades(module_code, student_id, grade)
        elif choice == '4':
            module_code = input("Enter module code: ")
            view_student_list(module_code)
        elif choice == '5':
            module_code = input("Enter module code: ")

            student_id = input("Enter student ID: ")
            if len(student_id) != 8:
                break
            else:
                print("Invalid Student ID. Student ID must start with 'TP' and followed by 6 digits")

            class_date = input("Enter the date of the class (YYYY-MM-DD): ")

            status = input("Enter attendance status (Present/Absent): ").strip().lower()
            if status not in ['present', 'absent']:
                print("Please enter a valid attendance status (Present/Absent).")
            else:
                status = status.capitalize()
                break

            track_attendance(module_code, student_id, class_date, status)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

# View Assigned Modules Functionality
def view_assigned_modules(lecturer_id):
    try:
        with open(LectModules_File, 'r') as file:
            print("\nYour Assigned Modules:")
            for line in file:
                module_details = line.strip().split(',')
                if module_details[-1] == lecturer_id:
                    print(f"Module Code: {module_details[0]}, Module Name: {module_details[1]}")
    except FileNotFoundError:
        print("Modules file not found.")

# View Student Grades Functionality
def view_student_grades(module_code):
    try:
        with open(Grades_File, 'r') as file:
            print(f"Students Grades for Module {module_code}: ")
            for line in file:
                grade_details = line.strip().split(',')
                if grade_details[0] == module_code:
                    print(f"Student ID: {grade_details[1]}, Grade: {grade_details[2]}")
    except FileNotFoundError:
        print("Grades file not found.")

# Recording Grades Functionality
def record_grades(module_code, student_id, grade):
    grades = []
    updated = False

    try:
        with open(Grades_File, 'r') as file:
            grades = [line.strip().split(',') for line in file]
    except FileNotFoundError:
        pass

    with open(Grades_File, 'w') as file:
        for record in grades:
            if record[0] == module_code and record[1] == student_id:
                file.write(f"{module_code},{student_id},{grade}\n")
                updated = True
            else:
                file.write(','.join(record) + '\n')

        if not updated:
            file.write(f"{module_code},{student_id},{grade}\n")

    print(f"Grade recorded successfully.")

# View Student List Functionality
def view_student_list(module_code):
    try:
        with open(StudentClasses_File, 'r') as file:
            print("Students enrolled in the module: ")
            for line in file:
                students = line.strip().split(',')
                if students[1] == module_code:
                    print(f"Student ID: {students[0]}")
    except FileNotFoundError:
        print("Student list file not found.")

# Track Attendance Functionality
def track_attendance(module_code, student_id, class_date, status):
    attendance_records = []
    updated = False

    try:
        with open(Attendance_File, 'r') as file:
            attendance_records = [line.strip().split(',') for line in file]
    except FileNotFoundError:
        pass

    with open(Attendance_File, 'w') as file:
        for record in attendance_records:
            if record[0] == module_code and record[1] == student_id:
                file.write(f"{module_code},{student_id},{class_date},{status}\n")
                updated = True
            else:
                file.write(','.join(record) + '\n')

        if not updated:
            file.write(f"{module_code},{student_id},{class_date},{status}\n")

    print(f"Attendance recorded successfully.")

# End of Lecturer Part--------------------------------------------------------------------------------------------------

# Beginning of Student Part---------------------------------------------------------------------------------------------

# Entering StudentID and Password to Access the Student Menu
def student_login():
    try:
        with open(StudentDetails_File, 'r') as file:
            details = {line.split(',')[0]: line.split(',')[1].strip() for line in file}
    except FileNotFoundError:
        print("Student file not found.")
        return None

    student_id = input("Please Enter Student ID: ")
    password = input("Please Enter Password: ")

    if student_id in details and details[student_id] == password:
        print("\nLogin successful")
        return student_id
    else:
        print("Invalid ID or Password.")
        return None

# Main Menu for students to choose what they want to do (Accessible after login)
def student_menu(student_id):
    while True:
        print("\nStudent Menu")
        print("1. View Available Modules")
        print("2. Enroll in Module")
        print("3. View Grades")
        print("4. Access Attendance Record")
        print("5. Unenroll from Module")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            view_available_modules()
        elif choice == '2':
            module_code = input("Enter module code you wish to enroll: ")
            enroll_in_module(student_id, module_code)
        elif choice == '3':
            view_grades(student_id)
        elif choice == '4':
            access_attendance_record(student_id)
        elif choice == '5':
            module_code = input("Enter module code you wish to unenroll: ")
            unenroll_from_module(student_id, module_code)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid input. Please enter a number from 1 to 6.")

# View Available Modules Functionality
def view_available_modules():
    try:
        with open(LectModules_File, 'r') as file:
            print("Currently Available Modules:")
            for line in file:
                module_details = line.strip().split(',')
                print(f"Module Code: {module_details[0]}, Module Name: {module_details[1]}")
    except FileNotFoundError:
        print("Modules file not found.")

# Enroll in Module Functionality
def enroll_in_module(student_id, module_code):
    enrollment = []
    already_enrolled = False

    try:
        with open(StudentClasses_File, 'r') as file:
            enrollment = [line.strip().split(',') for line in file]
    except FileNotFoundError:
        pass

    for record in enrollment:
        if record[0] == student_id and record[1] == module_code:
            already_enrolled = True
            break

    if already_enrolled:
        print("You are already enrolled in this module.")
    else:
        with open(StudentClasses_File, 'a') as file:
            file.write(f"{student_id},{module_code}\n")
        print(f"Successfully enrolled in module {module_code}.")

# View Grades Functionality
def view_grades(student_id):
    try:
        with open(Grades_File, 'r') as file:
            print("Your Grades:")
            for line in file:
                grade_details = line.strip().split(',')
                if grade_details[1] == student_id:
                    print(f"Module Code: {grade_details[0]}, Grade: {grade_details[2]}")
    except FileNotFoundError:
        print("Grades file not found.")

# Access Attendance Record Functionality
def access_attendance_record(student_id):
    try:
        with open(Attendance_File, 'r') as file:
            print("Your Attendance Records:")
            for line in file:
                attendance_record = line.strip().split(',')
                if attendance_record[1] == student_id:
                    print(f"Module Code: {attendance_record[0]}, Date: {attendance_record[2]}, Status: {attendance_record[3]}")
    except FileNotFoundError:
        print("Attendance file not found.")

# Unenroll from Module Functionality
def unenroll_from_module(student_id, module_code):
    enrollment = []
    try:
        with open(StudentClasses_File, 'r') as file:
            enrollment = [line.strip().split(',') for line in file]
    except FileNotFoundError:
        print("Student list file not found.")
        return

    with open(StudentClasses_File, 'w') as file:
        for record in enrollment:
            if not (record[0] == student_id and record[1] == module_code):
                file.write(','.join(record) + '\n')

    print(f"Successfully unenrolled from module {module_code}.")

# End of Student Part---------------------------------------------------------------------------------------------------
# Beginning of Registrar Part-------------------------------------------------------------------------------------------

def registrar_login():
    try:
        with open(RegDetails_File, 'r') as file:
            details = {line.split(',')[0]: line.split(',')[1].strip() for line in file}
    except FileNotFoundError:
        print("Registrar file not found.")
        return None

    registrar_id = input("Please Enter Registrar ID: ")
    password = input("Please Enter Password: ")

    if registrar_id in details and details[registrar_id] == password:
        print("\nLogin successful")
        return registrar_id
    else:
        print("Invalid ID or Password.")
        return None

# Helper Functions
def read_file_r(filename):
    """Reads data from a text file and returns it as a list of lines."""
    try:
        with open(filename, "r") as file:
            for line in file:
                return [line.strip()]
    except FileNotFoundError:
        return []

def write_file_r(filename, data):
    """Writes a list of lines to a text file."""
    with open(filename, "a") as file:
        for line in data:
            file.write(line + "\n")

def validate_input(prompt, valid_options=None):
    """
    Prompts the user for input and validates it based on allowed options.
    If valid_options is None, any input is allowed.
    """
    while True:
        user_input = input(prompt)
        if valid_options:
            if user_input in valid_options:
                return user_input
            else:
                print(f"Invalid choice. Please select from {valid_options}.")
        else:
            return user_input

# Registrar Functions
def register_new_student():
    """Registers a new student."""
    student_id = input("Enter student ID: ").strip()
    name = input("Enter student name: ").strip()
    program = input("Enter program: ").strip()

    students = read_file_r(StudentList_File)
    for student in students:
        if student_id == students[0]:
            print("Student ID already exists.")
            return

    students.append(f"{student_id},{name},{program}")
    write_file_r(StudentList_File, students)
    print("Student registered successfully.")


def update_student_records():
    student_id = input("Enter student ID to update: ")
    updated = False

    with open(StudentList_File, 'r') as file:
        lines = file.readlines()  # Read all lines into memory

    with open(StudentList_File, 'w') as file:
        for line in lines:
            details = line.strip().split(',')
            if details[0] == student_id:
                print(f"Current record: {details}")
                new_name = input("Enter new name (or press Enter to skip): ").strip() or details[1]
                new_program = input("Enter new program (or press Enter to skip): ").strip() or details[2]
                file.write(f"{student_id},{new_name},{new_program}\n")
                print("Student record updated.")
                updated = True
            else:
                file.write(line)  # Write the original line back

    if not updated:
        print("Student ID not found.")

def manage_enrolments():
    """Updates module enrolments for a student."""
    student_id = input("Enter student ID: ").strip()
    module = input("Enter module name: ").strip()

    students = read_file_r(StudentList_File)
    if not any(student_id == student.split(",")[0] for student in students):
        print("Student ID not found.")
        return

    enrolments = read_file_r(StudentClasses_File)
    enrolments.append(f"{student_id},{module}")
    write_file_r(StudentClasses_File, enrolments)
    print("Enrolment updated.")

def issue_transcripts():
    student_id = input("Enter student ID: ").strip()
    found = False  # To check if the student ID exists in the list

    with open(StudentList_File, 'r') as file:
        for line in file:
            check_id = line.strip().split(',')
            if student_id == check_id[0]:
                found = True
                print(f"Transcript for {student_id}:")

                # Check enrolled modules
                with open(StudentClasses_File, 'r') as filex:
                    modules = []  # Collect all modules for the student
                    for linex in filex:
                        details = linex.strip().split(',')
                        if student_id == details[0]:
                            modules.append(details[1])
                    if modules:
                        print(f"Enrolled Modules: {', '.join(modules)}")
                    else:
                        print("No modules found for the student.")
                break

    if not found:
        print("Student ID not found.")

def view_student_information():
    """Displays detailed information for a student."""
    student_id = input("Enter student ID: ").strip()

    students = read_file_r(StudentList_File)
    for student in students:
        details = student.split(",")
        if details[0] == student_id:
            print(f"Name: {details[1]}\nStudent ID: {details[0]}\nProgram: {details[2]}")
            return

    print("Student ID not found.")

# Menu Function
def registrar_menu(registrar_id):
    """Displays the main menu and handles user choices."""
    while True:
        print("\nRegistrar System")
        print("1. Register New Student")
        print("2. Update Student Records")
        print("3. Manage Enrolments")
        print("4. Issue Transcripts")
        print("5. View Student Information")
        print("6. Exit")

        choice = validate_input("Choose an option (1-6): ", valid_options=["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            register_new_student()
        elif choice == "2":
            update_student_records()
        elif choice == "3":
            manage_enrolments()
        elif choice == "4":
            issue_transcripts()
        elif choice == "5":
            view_student_information()
        elif choice == "6":
            print("Exiting Registrar System. Goodbye!")
            break

# End of Registrar Part-------------------------------------------------------------------------------------------------

# Beginning of Accountant Part------------------------------------------------------------------------------------------

def acc_login():
    try:
        with open(AccDetails_File, 'r') as file:
            details = {line.split(',')[0]: line.split(',')[1].strip() for line in file}
    except FileNotFoundError:
        print("Accountant file not found.")
        return None

    acc_id = input("Please Enter Accountant ID: ")
    password = input("Please Enter Password: ")

    if acc_id in details and details[acc_id] == password:
        print("\nLogin successful")
        return acc_id
    else:
        print("Invalid ID or Password.")
        return None

# Function to record tuition fees
def record_tuition_fees():
    student_id = input("Enter student ID: ")
    amount_paid = input("Enter fee amount: ")

    try:
        with open(StudentList_File, 'r') as file:
            for line in file:
                details = line.strip().split(',')
                if details[0] == student_id:
                    with open(Fees_File, 'a') as f:
                        f.write(f"{student_id},{amount_paid}\n")
                    print("Tuition fee recorded successfully.")
                    break
            else:
                print("Student ID is not registered.")
    except FileNotFoundError:
        print("Student File was not found")


# Function to view outstanding fees
def view_outstanding_fees():
    try:
        students = {}
        payments = {}
        full_fees = float(75000.00)

        with open(StudentList_File, 'r') as students_file:
            for line in students_file:
                student_id, name, program = line.strip().split(',')
                students[student_id] = f"{name} ({program})"

        with open(Fees_File, 'r') as fees_file:
            for line in fees_file:
                student_id, amount_paid = line.strip().split(',')
                payments[student_id] = payments.get(student_id, 0) + int(amount_paid)

        print("\nOutstanding Fees:")
        for student_id, name in students.items():
            if student_id not in payments:
                print(f"Student ID: {student_id}, Name: {name} has not paid any fees yet.")
            else:
                outstanding = full_fees - payments[student_id]
                print(f"Student ID: {student_id}, Name: {name} has {outstanding} fees remaining to be paid.")

    except Exception as e:
        print(f"Error viewing outstanding fees: {e}")


# Function to update payment records
def update_payment_records():
    student_id = input("Enter student ID to update: ")
    amount_paid = input("Enter new fee amount: ")

    try:
        lines = []
        updated = False  # Flag to check if an update has occurred
        with open(Fees_File, 'r') as f:
            lines = f.readlines()

        with open(Fees_File, 'w') as f:
            for line in lines:
                if line.startswith(student_id):
                    f.write(f"{student_id},{amount_paid}\n")
                    updated = True  # Set the flag to True if an update occurs
                else:
                    f.write(line)

        if updated:
            print("Payment record updated successfully.")
        else:
            print("No record found for the given student ID.")
    except FileNotFoundError:
        print("Fees file not found.")
    except Exception as e:
        print(f"Error updating payment records: {e}")


# Function to issue fee receipts
def issue_fee_receipts():
    student_id = input("Enter student ID: ")

    try:
        with open(Fees_File, 'r') as f:
            fees = f.readlines()

        # Check if the student ID exists in the fees file
        for line in fees:
            if line.startswith(student_id):
                amount = line.split(',')[1].strip()

                # Get student name from students file
                with open(StudentList_File, 'r') as students_file:
                    students = {line.split(',')[0]: line.strip() for line in students_file}
                    student_name = students.get(student_id, "Unknown Student")

                # Generate a unique receipt number (uses datetime to print receipt according to current timestamp)
                receipt_number = f"REC-{int(datetime.now().timestamp())}"

                # Get the current date
                transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Create the receipt content
                receipt = (
                    f"===============================\n"
                    f"          Fee Receipt          \n"
                    f"===============================\n"
                    f"Receipt Number: {receipt_number}\n"
                    f"Student ID: {student_id}\n"
                    f"Student Info: {student_name}\n"
                    f"Amount Paid: ${amount}\n"
                    f"Transaction Date: {transaction_date}\n"
                    f"===============================\n"
                )

                # Save the receipt to the receipts file
                with open(Receipts_File, 'a') as receipt_file:
                    receipt_file.write(receipt)

                print("Fee receipt issued successfully.")
                print(receipt)  # Print the receipt to the console
                return

        print("No fee record found for this student ID.")
    except FileNotFoundError:
        print("Fees file not found.")
    except Exception as e:
        print(f"Error issuing fee receipt: {e}")


# Function to view financial summary
def view_financial_summary():
    try:
        total_collected = 0
        total_outstanding = 0
        full_fees = 75000.00

        # Read fees and calculate total collected
        with open(Fees_File, 'r') as f:
            fees = f.readlines()
            total_collected = sum(float(line.split(',')[1]) for line in fees)

        # Calculate total outstanding fees
        total_students = 0
        with open(StudentList_File, 'r') as f:
            total_students = len(f.readlines())

        total_outstanding = total_students * full_fees - total_collected  # Assuming each student has a fee of 75000

        # Calculate average fee per student
        average_fee = total_collected / total_students if total_students > 0 else 0

        # Display the financial summary
        print("\n===============================")
        print("        Financial Summary      ")
        print("===============================")
        print(f"Total Fees Collected: ${total_collected:.2f}")
        print(f"Total Outstanding Fees: ${total_outstanding:.2f}")
        print(f"Average Fee per Student: ${average_fee:.2f}")
        print("===============================")
    except FileNotFoundError:
        print("One of the required files is missing.")
    except Exception as e:
        print(f"Error viewing financial summary: {e}")


# Main menu function
def accountant_menu(acc_id):

    while True:
        print("\n===============================")
        print("         Accountant Menu       ")
        print("===============================")
        print("1. Record Tuition Fees")
        print("2. View Outstanding Fees")
        print("3. Update Payment Records")
        print("4. Issue Fee Receipts")
        print("5. View Financial Summary")
        print("6. Exit")
        print("===============================")

        choice = input("Select an option (1-6): ")

        if choice == '1':
            record_tuition_fees()
        elif choice == '2':
            view_outstanding_fees()
        elif choice == '3':
            update_payment_records()
        elif choice == '4':
            issue_fee_receipts()
        elif choice == '5':
            view_financial_summary()
        elif choice == '6':
            print("Exiting the system. Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")

# End of Accountant Part------------------------------------------------------------------------------------------------

# Main Menu to Select Role and Access Relevant Functionality------------------------------------------------------------
def main_menu():
    while True:
        print("\nUniversity Management System")
        print("1. Administrator Login")
        print("2. Lecturer Login")
        print("3. Student Login")
        print("4. Registrar Login")
        print("5. Accountant Menu")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            admin_id = admin_login()
            if admin_id:
                admin_menu(admin_id)
        elif choice == '2':
            lecturer_id = lect_login()
            if lecturer_id:
                lecturer_menu(lecturer_id)
        elif choice == '3':
            student_id = student_login()
            if student_id:
                student_menu(student_id)
        elif choice == '4':
            registrar_id = registrar_login()
            if registrar_id:
                registrar_menu(registrar_id)
        elif choice == '5':
            acc_id = acc_login()
            if acc_id:
                accountant_menu(acc_id)
        elif choice == '6':
            print("Exiting the system...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 3.")

# End of Main Menu------------------------------------------------------------------------------------------------------

# Run the Main Menu
main_menu()