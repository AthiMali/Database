import sqlite3
import json
import xml.etree.ElementTree as ET


# Connecting the database
try:
    conn = sqlite3.connect("HyperionDev.db")
except sqlite3.Error:
    print("Please store your database as HyperionDev.db")
    quit()

cur = conn.cursor()
with open('create_database.sql','r') as file:
    sql_commands = file.read()
    
cur.executescript(sql_commands)
conn.commit()

def execute_query_and_print_results(query, column_names):
    cur.execute(query)
    results = cur.fetchall()
    
    for row in results:

        # Print only specified columns

        print(', '.join([str(row[column_names.index(col)]) for col in column_names]))


def usage_is_incorrect(input, num_args):
    if len(input) != num_args + 1:
        print(f"The {input[0]} command requires {num_args} arguments.")
        return True
    return False

def store_data_as_json(data, filename):
    pass

def store_data_as_xml(data, filename):
    pass

def offer_to_store(data):
    while True:
        print("Would you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()

        if choice == "y":
            filename = input("Specify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1]
            if ext == 'xml':
                store_data_as_xml(data, filename)
            elif ext == 'json':
                store_data_as_json(data, filename)
            else:
                print("Invalid file extension. Please use .xml or .json")

        elif choice == 'n':
            break

        else:
            print("Invalid choice")

usage = '''
What would you like to do?

d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")

while True:
    print()
    # Get input from user
    user_input = input(usage).split(" ")
    print()

    # Parse user input into command and args
    command = user_input[0]
    if len(user_input) > 1:
        args = user_input[1:]

    if command == 'd': # demo - a nice bit of code from me to you - this prints all student names and surnames :)
        data = cur.execute("SELECT * FROM Student")
        data = cur.fetchall()
        for _, firstname, surname, _, _ in data:
            print(f"{firstname} {surname}")
        
    elif command == 'vs': # view subjects by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        data = None

        # Run SQL query and store in data
        # . . 

        data = cur.fetchall()

        # student_id = input("Enter the student's ID: ")
        
        query = f"""  SELECT B.Course_Name FROM 'StudentCourse' AS 
            A  JOIN 'Course' AS B ON A.course_code = B.course_code
            WHERE student_id = '{student_id}'"""
        column_names = ["course_name"]
        execute_query_and_print_results(query, column_names)
        

        offer_to_store(data)
        pass

    elif command == 'la':# list address by name and surname
        if usage_is_incorrect(user_input, 2):
            continue
        firstname, surname = args[0], args[1]
        data = None

        # Run SQL query and store in data
        # . . .
        
        query = f"SELECT street, city FROM Address INNER JOIN Student ON Address.address_id = Student.address_id WHERE first_name = '{firstname}' AND last_name = '{surname}'"
        column_names = ["street", "city"]
        execute_query_and_print_results(query, column_names)

        data = cur.fetchall()

        offer_to_store(data)
        pass
    
    elif command == 'lr':# list reviews by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        data = None

        # Run SQL query and store in data
        # . . .

        query = f"SELECT completeness, efficiency, style, documentation, review_text FROM Review WHERE student_id = '{student_id}'"
        column_names = ["completeness", "efficiency", "style", "documentation", "review_text"]
        execute_query_and_print_results(query, column_names)

        offer_to_store(data)
        pass

    elif command == 'lc':# list all courses taken by teacher_id
        if usage_is_incorrect(user_input, 1):
            continue
        teacher_id = args[0]
        data = None
        
        query = f"SELECT course_name FROM Course WHERE teacher_id = '{teacher_id}'"
        column_names = ["course_name"]
        execute_query_and_print_results(query, column_names)

        offer_to_store(data)
    
    elif command == 'lnc':# list all students who haven't completed their course
        
        data = None

        # Run SQL query and store in data
        # . . . 
        query = """SELECT  A.student_id, A.first_name, A.last_name,A.email,C.course_name
                FROM 'Student' AS A 
                JOIN 'StudentCourse' AS B ON A.student_id = B.student_id 
                JOIN 'Course' AS C ON C.course_code = B.course_code
                WHERE B.is_complete = false"""
        column_names = ["student_id", "first_name", "last_name", "email", "course_name"]
        execute_query_and_print_results(query, column_names)

        offer_to_store(data)
        pass
    
    elif command == 'lf':# list all students who have completed their course and got a mark <= 30
        data = None

        # Run SQL query and store in data
        # . . . 
       
        query = """SELECT  A.student_id, A.first_name, A.last_name,A.email,C.course_name
                    FROM 'Student' AS A 
                    JOIN 'StudentCourse' AS B ON A.student_id = B.student_id 
                    JOIN 'Course' AS C ON C.course_code = B.course_code
                    WHERE B.mark <= 30"""
        
        column_names = ["student_id", "first_name", "last_name", "email", "course_name"]
        execute_query_and_print_results(query, column_names)

        offer_to_store(data)
        pass
    
    elif command == 'e':# list address by name and surname
        print("Programme exited successfully!")
        break
    
    else:
        print(f"Incorrect command: '{command}'")

# Close the database connection
conn.close()
    

    
