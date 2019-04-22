"""Gets petition info."""

import sqlite3

get_petitions(email):
    """Connects to database and gets list of petitions associated with the
    department of the input email."""
    conn = sqlite3.connect("petitiondb.sqlite3")  # connect to the database

    petition_results = []

    # Get department based on inputted email:
    department_query = "SELECT department FROM User_Table WHERE email = \"{A}\"".format(A = email)
    dept_query_obj = conn.execute(department_query)
    dept_tuple = dept_query_obj.fetchone()  # store results of query - in a tuple
    try:
        dept_result = email_tuple[0]  # if query returns a result, store it as a string
    except:
        dept_result = ""  # if query returns no results/an error, set value as empty string

    # Find petitions for that department:
    petition_query = "SELECT * FROM Student_Petition WHERE department = \"{A}\"".format(A = dept_result)
    petition_query_obj = conn.execute(petition_query)
    petition_tuple = petition_query_obj.fetchall()  # store results of query - in a tuple
    try:
        petition_results.append(petition_tuple[i])  # if query returns a result, store it as a string
    except:
        petition_results = ""  # if query returns no results/an error, set value as empty string

    return petition_results


get_petition_info(id):
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
