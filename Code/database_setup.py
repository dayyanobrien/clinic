# coding=utf-8
import sqlite3

db = sqlite3.connect('clinic.db')
cursor = db.cursor()
"""
creates the entire database with sutiable columns
"""
cursor.execute('''CREATE TABLE IF NOT EXISTS clients(
               ClientID INTEGER PRIMARY KEY AUTOINCREMENT,
               MedicalRecordID INTEGER unique,
               Prefix TEXT,
               FirstName TEXT,
               Surname TEXT,
               DOB TEXT,
               Telephone TEXT,
               Address TEXT,
               Postcode TEXT,
               FOREIGN KEY(MedicalRecordID) REFERENCES medicalrecords(MedicalRecordID))
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

cursor.execute('''CREATE TABLE IF NOT EXISTS medicalrecords(
                MedicalRecordID INTEGER PRIMARY KEY AUTOINCREMENT,
                ClientID INTEGER unique,
                Sex TEXT,
                Gender TEXT,
                BloodType TEXT,
                Height REAL,
                Mass REAL,
                FOREIGN KEY(ClientID) REFERENCES clients(ClientID))
                ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS appointments(
                AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
                ClientID INTEGER,
                StaffID INTEGER,
                TransactionID INTEGER unique,
                StartDateAndTime TEXT,
                EndDateAndTime TEXT,
                AppointmentStatus TEXT,
                FOREIGN KEY(ClientID) REFERENCES clients(ClientID),
                FOREIGN KEY(StaffID) REFERENCES staff(StaffID),
                FOREIGN KEY(TransactionID) REFERENCES transactions(TransactionID))
                ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions(
                TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
                Difference FLOAT,
                DateAndTime TEXT,
                TransactionStatus TEXT)
                ''')

db.commit()

cursor.execute("""UPDATE staff SET LoggedIn = ?""", ("False",)) #puts loggedin to false

db.commit()
