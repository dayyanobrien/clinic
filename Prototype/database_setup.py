# coding=utf-8
import sqlite3

db = sqlite3.connect('clinic.db')
cursor = db.cursor()
"""
creates the entire database with sutiable columns
"""
cursor.execute('''CREATE TABLE IF NOT EXISTS clients(
               ClientID INTEGER PRIMARY KEY AUTOINCREMENT,
               Prefix TEXT,
               FirstName TEXT,
               Surname TEXT,
               DOB TEXT,
               Telephone TEXT,
               Address TEXT,
               Postcode TEXT)
               ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS staff(
               StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
               Prefix TEXT, 
               FirstName TEXT,
               Surname TEXT,
               DOB TEXT,
               Telephone TEXT,
               Address TEXT,
               Postcode TEXT,
               Username TEXT unique,
               Position TEXT,
               LoggedIn BOOLEAN,
               Password TEXT)
               ''')

db.commit()

cursor.execute("""UPDATE staff SET LoggedIn = ?""", ("False",))  # puts loggedin to false

db.commit()
