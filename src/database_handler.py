"""Gets petition info."""

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
    try:
        numOfResponses = num_tuple[0][0]
        print("RESPONSES", numOfResponses)
        numOfApprovals = num_tuple[0][1]
        print("APPROVALS", numOfApprovals)
    except:
        print("no")

    numOfResponses += 1
    add_review = "UPDATE Approval_Responses SET numOfResponses = {A} WHERE petitionID = {B}".format(A = numOfResponses, B = petitionID)
    cur.execute(add_review)
    conn.commit()

    if approval_decision:
        numOfApprovals += 1
        print(numOfApprovals)
        add_approval = "UPDATE Approval_Responses SET numOfApprovals = {A} WHERE petitionID = {B}".format(A = numOfApprovals, B = petitionID)
    else:
        pass

    if numOfResponses >= 4:  # num of faculty
        if numOfApprovals >= 2:
            student_message = "Your petition has passed."
            teacher_message = "This email is to let you know that the reviewed petition passed."
        else:
            student_message = "Your petition did not pass."
            teacher_message = "This email is to let you know that the reviewed petition did not pass."
        student_subject = "Information About Your Petition"
        teacher_subject = "Information About Student Petition"

        #send_email.send_email(student_subject, student_message, "lussierc@allegheny.edu")

    conn.close()  # close database connection

dec = True
submit_decision(0, dec)
