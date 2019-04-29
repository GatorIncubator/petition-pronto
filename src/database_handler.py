"""Gets petition info."""

import math
import send_email
import sqlite3

def get_petitions(email):
    """Connects to database and gets list of petitions associated with the
    department of the input email."""
    conn = sqlite3.connect("petitiondb.sqlite3")  # connect to the database

    petition_results = []

    # Get department based on inputted email:
    department_query = "SELECT department FROM User_Table WHERE email = \"{A}\"".format(A = email)
    dept_query_obj = conn.execute(department_query)
    dept_tuple = dept_query_obj.fetchone()  # store results of query - in a tuple
    try:
        dept_result = dept_tuple[0]  # if query returns a result, store it as a string
    except:
        dept_result = ""  # if query returns no results/an error, set value as empty string

    # Find petitions for that department:
    petition_query = "SELECT name, email, department, petitionID FROM Student_Petition WHERE department = \"{A}\"".format(A = dept_result)
    petition_query_obj = conn.execute(petition_query)
    petition_list = petition_query_obj.fetchall()  # store results of query - in a tuple
    try:
        petition_results = petition_list # if query returns a result, store it as a string
    except:
        petition_results = ""  # if query returns no results/an error, set value as empty string

    return(petition_results)
    conn.close()


def get_petition_info(id):
    """Connects to the database and gets info about a specific petition."""
    conn = sqlite3.connect("petitiondb.sqlite3")  # connect to the database

    petition_query = "SELECT * FROM Student_Petition WHERE petitionID = \"{A}\"".format(A = id)
    petition_query_obj = conn.execute(petition_query)
    petition_tuple = petition_query_obj.fetchall()
    try:
        petition_info = petition_tuple[0]
    except:
        petition_info = ""

    return petition_info
    conn.close()


def change_password(email, new_password):
    """Changes the password based on the given email."""
    conn = sqlite3.connect("petitiondb.sqlite3")  # connect to the database

    change_pass_query = "UPDATE User_Table SET password = \"{A}\" WHERE email = \"{B}\"".format(A = new_password, B = email)
    cur = conn.cursor()
    cur.execute(change_pass_query)
    conn.commit()
    conn.close()


id = 0  # set started ID value for users in User_Table
def create_account(email, password, role, department):
    """Creates a user account."""
    conn = sqlite3.connect("petitiondb.sqlite3")  # connect to the database

    max_id_query = "SELECT max(id) FROM User_Table"  # get the most recently created acocunts id
    max_id_obj = conn.execute(max_id_query)
    max_id_tuple = max_id_obj.fetchall()
    try:
        max_id = max_id_tuple[0][0]  # store most recent id
    except:
        max_id = 0

    id = max_id + 1  # create newest id

    create_user_insert = "INSERT INTO User_Table(id, email, password, role, department) VALUES({A}, \"{B}\", \"{C}\", \"{D}\", {E})".format(A = id, B = email, C = password, D = role, E = department)

    cur = conn.cursor()
    cur.execute(create_user_insert)  # execute the creation
    conn.commit()  # commit changes to the database
    conn.close()  # close database connection


def submit_decision(petitionID, approval_decision):
    """Submits faculty's approval or denial decision for petition."""
    conn = sqlite3.connect("petitiondb.sqlite3")  # connect to the database
    cur = conn.cursor()

    find_petition_query = "SELECT * FROM Approval_Responses WHERE petitionID = {A}".format(A = petitionID)
    find_petition_query_obj = conn.execute(find_petition_query)
    petition_tuple = find_petition_query_obj.fetchall()
    try:
        approval_info = petition_tuple[0]
    except:
        create_approval = "INSERT INTO Approval_Responses(petitionID, numOfResponses, numOfApprovals) VALUES({A}, {B}, {C})".format(A = petitionID, B = 0, C = 0)
        cur.execute(create_approval)  # execute the creation
        conn.commit()  # commit changes to the database

    num_query = "SELECT numOfResponses, numOfApprovals FROM Approval_Responses WHERE petitionID = {A}".format(A = petitionID)
    num_query_obj = conn.execute(num_query)
    num_tuple = num_query_obj.fetchall()
    #print(num_tuple)
    try:
        numOfResponses = num_tuple[0][0]
        numOfApprovals = num_tuple[0][1]
    except:
        pass

    numOfResponses += 1
    add_review = "UPDATE Approval_Responses SET numOfResponses = {A} WHERE petitionID = {B}".format(A = numOfResponses, B = petitionID)
    cur.execute(add_review)
    conn.commit()

    if approval_decision is True:
        numOfApprovals += 1
        add_approval = "UPDATE Approval_Responses SET numOfApprovals = {A} WHERE petitionID = {B}".format(A = numOfApprovals, B = petitionID)
        cur.execute(add_approval)
        conn.commit()
    else:
        pass

    get_student_email_query = "SELECT email FROM Student_Petition WHERE petitionID = {A}".format(A = petitionID)
    get_student_email_obj = conn.execute(get_student_email_query)
    student_email_tuple = get_student_email_obj.fetchone()
    try:
        student_email = student_email_tuple[0]
    except:
        student_email = ""

    get_petition_department = "SELECT department FROM Student_Petition WHERE petitionID = {A}".format(A = petitionID)
    get_department_obj = conn.execute(get_petition_department)
    department_tuple = get_department_obj.fetchone()
    try:
        petition_department = department_tuple[0]
    except:
        petition_department = ""

    get_faculty_emails_query = "SELECT email FROM User_Table WHERE department = {A}".format(A = petition_department)
    faculty_emails_obj = conn.execute(get_faculty_emails_query)
    faculty_email_list = faculty_emails_obj.fetchall()
    #print(faculty_email_list)

    if numOfResponses >= len(faculty_email_list):  # num of faculty
        necessaryApprovals = math.ceil(len(faculty_email_list) / 2)
        print(necessaryApprovals)
        if numOfApprovals >= 2:
            student_message = "After votes by the department faculty, it was determined that your petition has been approved."
            teacher_message = "This email is to let you know that the reviewed petition by", student_email, "passed."
            print(teacher_message)
        else:
            student_message = "After votes by department faculty, it was determined that your petition has been denied."
            teacher_message = "This email is to let you know that the reviewed petition by", student_email, "did not pass."
            print(teacher_message)
        student_subject = "Information About Your Petition"
        teacher_subject = "Information About Student Petition"

        send_email.send_email(student_subject, student_message, student_email)  # send email to the student

        for i in range(len(faculty_email_list)):
            current_email = faculty_email_list[i][0]
            print(current_email)
            send_email.send_email(teacher_subject, teacher_message, current_email)  # send email to faculty member

    print("RESPONSES", numOfResponses)
    print("APPROVALS", numOfApprovals)
    conn.close()  # close database connection

submit_decision(0, True)
