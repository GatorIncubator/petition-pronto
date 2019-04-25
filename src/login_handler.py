"""Login handler that validates a user's login information."""

import sqlite3

def validate_user(email, password):
    """Validates the user identity using information from database."""
    conn = sqlite3.connect("petitiondb.sqlite3")  # connect to the database

    email_query = "SELECT email FROM User_Table WHERE email = \"{A}\"".format(A = email)
    email_query_obj = conn.execute(email_query)  # execute query that checks for valid email
    email_tuple = email_query_obj.fetchone()  # store results of query - in a tuple
    try:
        email_result = email_tuple[0]  # if query returns a result, store it as a string
    except:
        email_result = ""  # if query returns no results/an error, set value as empty string

    password_query = "SELECT password, role FROM User_Table WHERE email = \"{A}\"".format(A = email)
    password_query_obj = conn.execute(password_query)  # execute query that checks for valid password
    password_tuple = password_query_obj.fetchone()
    try:
        password_result = password_tuple[0] # if query returns a result, store it as a string
    except:
        password_result = ""  # if query returns no results/an error, set value as empty string

    try:
        role = password_tuple[1]
    except:
        role = ""

    admin = role == "Admin"

    if email == email_result and password == password_result:
        return True, admin  # if valid, login
    else:
        return False, admin  # if invalid

    conn.close()  # close database connection
