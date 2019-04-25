"""Gets petition info."""

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
        peitition_info = ""

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


id = 0
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
    conn.commit()
    conn.close()
