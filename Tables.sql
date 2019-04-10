CREATE TABLE User_Table (
  id INTEGER PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  role TEXT NOT NULL,
  department INTEGER REFERENCES Department(ID)
);

CREATE TABLE Student_Petition (
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  petition TEXT NOT NULL,
  department INTEGER REFERENCES Department(ID)
);

CREATE TABLE Department (
  name TEXT NOT NULL UNIQUE,
  ID INTEGER PRIMARY KEY
);
