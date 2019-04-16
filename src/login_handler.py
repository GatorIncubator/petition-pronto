#!/usr/bin/env python3

import sqlite3

# use a dictionary to keep track of how many attributes there are per table.
tables_dict = {"User_Table": 5,
"Student_Petition": 4,
"Department": 2
}

def validate_user(email, password):
    """Validates the user identity using information from database."""
    conn = sqlite3.connect("petitiondb.sqlite3") # connect to the database
    email_query = "SELECT email FROM User_Table WHERE email = \"{A}\"".format(A = email)
    email_result = conn.execute(email_query)
    password_query = "SELECT password FROM User_Table WHERE email = \"{A}\"".format(A = email)
    password_result = conn.execute(password_query)

    #if email == email_result and password == password_result:
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
