#!/usr/bin/env python3

import sqlite3

# use a dictionary to keep track of how many attributes there are per table.
tables_dict = {"User_Table": 5,
"Student_Petition": 4,
"Department": 2
}

def validate_user(email, password):
    """Validates the user identity."""
    # if email == "email@email.com" and password == "password":
    #     return True
    # else:
    #     return False
    #select password from user_table where email2 = email
    email_query = "SELECT email FROM User_Table WHERE email = \"{A}".format(A = email)
    password_query = "SELECT password FROM User_Table WHERE email = \"{A}".format(A = email)
    if email == email_query and password == password_query:
        return True
    else:
        return False

sqlite3Filename = "petitiondb.sqlite3"

#open my database connection
conn = sqlite3.connect(sqlite3Filename) # connect to the database

conn.close()
