#!/usr/bin/env python3

import sqlite3

# use a dictionary to keep track of how many attributes there are per table.
tables_dict = {"User_Table": 5,
"Student_Petition": 4,
"Department": 2
}

def validate_user(email, password):
    """Validates the user identity using information from database."""
    user_email = email
    user_password = password
    conn = sqlite3.connect("petitiondb.sqlite3") # connect to the database

    email_query = "SELECT email FROM User_Table WHERE email = \"{A}\"".format(A = email)
    email_query_obj = conn.execute(email_query)
    email_tuple = email_query_obj.fetchone()
    try:
        email_result = email_tuple[0]
    except:
        email_result = ""


    password_query = "SELECT password FROM User_Table WHERE email = \"{A}\"".format(A = email)
    password_query_obj = conn.execute(password_query)
    password_tuple = password_query_obj.fetchone()
    password_result = password_tuple[0]

    #if email == email_result and password == password_result:
    print("***If", email, "==", email_result, "and", password, "==", password_result)
    if email == email_result and password == password_result:
        return True
    else:
        return False
    conn.close()


def validate_user_old(email, password):
    # This is placeholder implementation. Needs to be implemented with database.
    if email == "email@email.com" and password == "password":
        return True
    else:
        return False
#open my database connection
