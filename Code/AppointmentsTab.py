# coding=utf-8

import tkinter as Tkinter
import tkinter.ttk as ttk
import re
import sqlite3
from tkinter import *
import tkinter as tk
import datetime
from datetime import datetime
from tkinter import messagebox
import ast


class AppointmentsFrame(tk.Frame):
    """
    the frame for the appointments tab
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        appointments_frame = tk.LabelFrame(self, text="Appointments", padx=5, pady=5, width=1250, height=750)
        appointments_frame.grid(row=0, column=0)

        OPTIONS = [
            "AppointmentID          ",
            "ClientID                       ",
            "StaffID                         ",
            "TransactionID            ",
            "Start Date And Time ",
            "End Date And Time   ",
            "Appointment Status  "
        ]

        variable = StringVar(appointments_frame)
        variable.set(OPTIONS[0])

        # Set the treeview
        appointments_frame.tree = ttk.Treeview(appointments_frame, height="33", selectmode='browse',
                                               columns=(
                                                   'ClientID', 'StaffID', 'TransactionID', 'Start Date And Time',
                                                   'End Date And Time', 'Appointment Status'
                                               ))
        AppointmentsFrame.tree = appointments_frame.tree
        appointments_frame.tree.heading('#0', text='AppointmentID')
        appointments_frame.tree.heading('#1', text='ClientID')
        appointments_frame.tree.heading('#2', text='StaffID')
        appointments_frame.tree.heading('#3', text='TransactionID')
        appointments_frame.tree.heading('#4', text='Start Date And Time')
        appointments_frame.tree.heading('#5', text='End Date And Time')
        appointments_frame.tree.heading('#6', text='Appointment Status')
        appointments_frame.tree.column('#0', stretch=Tkinter.YES, width="100", minwidth="50")
        appointments_frame.tree.column('#1', stretch=Tkinter.YES, width="100", minwidth="100")
        appointments_frame.tree.column('#2', stretch=Tkinter.YES, width="75", minwidth="50")
        appointments_frame.tree.column('#3', stretch=Tkinter.YES, width="110", minwidth="85")
        appointments_frame.tree.column('#4', stretch=Tkinter.YES, width="150", minwidth="85")
        appointments_frame.tree.column('#5', stretch=Tkinter.YES, width="150", minwidth="75")
        appointments_frame.tree.column('#6', stretch=Tkinter.YES, width="150", minwidth="100")
        appointments_frame.tree.grid(row=5, columnspan=50, rowspan=50, sticky='nsew')
        appointments_frame.treeview = appointments_frame.tree

        search = tk.Label(appointments_frame, text="Search: ")
        search.grid(row=10, column=50)
        search_box = appointments_frame.search_entry = tk.Entry(appointments_frame)
        search_box.grid(row=10, column=51)
        dropdownsearch = OptionMenu(appointments_frame, variable, *OPTIONS)
        dropdownsearch.grid(row=10, column=52)

        tk.Button(appointments_frame, text="Search", command=self.search_table).grid(row=11, column=51)

        tk.Button(appointments_frame, text="Add an appointment", command=CreateAppointmentFrame).grid(row=13, column=51)

        tk.Button(appointments_frame, text="Cancel an appointment", command=self.cancel_appointment).grid(row=15,
                                                                                                          column=51)


        pad = tk.Label(appointments_frame, text="")
        pad.grid(row=10, column=55, padx=(0, 30))

        self.tree = appointments_frame.tree
        self.variable = variable
        self.search_box = search_box
        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()
        self.update_table()

    def cancel_appointment(self):
        """
        cancels highlighted appointment
        """
        iid_selected = self.tree.focus()
        appointment_id = self.tree.item(iid_selected, 'text')
        self.cursor.execute("""UPDATE appointments SET AppointmentStatus = ? WHERE AppointmentID = ?""",
                            ('Cancelled', appointment_id,))
        self.db.commit()
        self.update_table()

    def search_table(self):
        """
        searches for a keyword from a selected column and shows in treeview
        """
        drop_down = self.variable.get()
        search = self.search_box.get()
        if drop_down == "AppointmentID          ":
            self.cursor.execute("""SELECT * FROM appointments WHERE AppointmentID LIKE ?""", ('%' + search + '%',))
            drop_down = "AppointmentID"
        elif drop_down == "ClientID                       ":
            self.cursor.execute("""SELECT * FROM appointments WHERE ClientID LIKE ?""", ('%' + search + '%',))
            drop_down = "ClientID"
        elif drop_down == "StaffID                         ":
            self.cursor.execute("""SELECT * FROM appointments WHERE StaffID LIKE ?""", ('%' + search + '%',))
            drop_down = "StaffID"
        elif drop_down == "TransactionID            ":
            self.cursor.execute("""SELECT * FROM appointments WHERE TransactionID LIKE ?""", ('%' + search + '%',))
            drop_down = "TransactionID"
        elif drop_down == "Start Date And Time ":
            self.cursor.execute("""SELECT * FROM appointments WHERE StartDateAndTime LIKE ?""", ('%' + search + '%',))
            drop_down = "Start Date And Time"
        elif drop_down == "End Date And Time   ":
            self.cursor.execute("""SELECT * FROM appointments WHERE EndDateAndTime LIKE ?""", ('%' + search + '%',))
            drop_down = "End Date And Time"
        elif drop_down == "Appointment Status  ":
            self.cursor.execute("""SELECT * FROM appointments WHERE AppointmentStatus LIKE ?""", ('%' + search + '%',))
            drop_down = "Appointment Status"
        self.tree.delete(*self.tree.get_children())
        rows = self.cursor.fetchall()
        f = open('appointments.txt','w')
        f.write("------------------------ Searched for '" + search + "' by " + drop_down + "------------------------" + '\n')
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=row[1:])
            f.write('\n' + "AppointmentID: " + str(row[0]))
            f.write('\n' + "ClientID: "  + str(row[1]))
            f.write('\n' + "StaffID: " + str(row[2]))
            f.write('\n' + "TransactionID: " + str(row[3]))
            f.write('\n' + "Start Date And Time: " + str(row[4]))
            f.write('\n' + "End Date And Time: " + str(row[5]))
            f.write('\n' + "Appointment Status: " + str(row[6]))
            f.write('\n')
        messagebox.showinfo("Alert", "Appointments saved (appointments.txt)")
        f.close()

    def update_table(self):
        """
        updates the treeview and fills it with all records
        in the AppointmentID table
        """
        self.cursor.execute("""SELECT * FROM appointments""")
        result = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for item in result:
            self.tree.insert('', 'end', text=item[0], values=item[1:])


class CreateAppointmentFrame(tk.Frame):
    """
    creates a new window and allows the user to create a new client,
    when completed it will update the treeview in ClientTab
    """

    def __init__(self):
        tk.Frame.__init__(self)
        self.tree = AppointmentsFrame.tree
        create_appointment_window = tk.Toplevel(self)
        create_appointment_window.geometry("280x230")
        self.create_appointment_window = create_appointment_window
        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()

        self.cursor.execute("""SELECT ClientID FROM clients""")

        CLIENTOPTIONS = []
        result = self.cursor.fetchall()
        for item in result:
            CLIENTOPTIONS.append(item)

        clientvariable = StringVar(create_appointment_window)

        try:
            clientvariable.set(CLIENTOPTIONS[0])
        except IndexError:
            messagebox.showinfo("Error", "No clients available")
            self.create_appointment_window.destroy()

        self.cursor.execute("""SELECT StaffID FROM staff""")

        STAFFOPTIONS = []
        result = self.cursor.fetchall()
        for item in result:
            STAFFOPTIONS.append(item)

        staffvariable = StringVar(create_appointment_window)

        try:
            staffvariable.set(STAFFOPTIONS[0])
        except IndexError:
            messagebox.showinfo("Error", "No staff available")
            self.create_appointment_window.destroy()

        client = tk.Label(create_appointment_window, text="ClientID: ")
        client.grid(row=0, column=0)
        clientsearch = OptionMenu(create_appointment_window, clientvariable, *CLIENTOPTIONS)
        clientsearch.grid(row=0, column=1)

        staff = tk.Label(create_appointment_window, text="StaffID: ")
        staff.grid(row=1, column=0)
        staffsearch = OptionMenu(create_appointment_window, staffvariable, *STAFFOPTIONS)
        staffsearch.grid(row=1, column=1)

        startdateandtime = tk.Label(create_appointment_window, text="Start Date And Time: ")
        startdateandtime.grid(row=2, column=0)
        startdateandtime_box = create_appointment_window.search_entry = tk.Entry(create_appointment_window)
        startdateandtime_box.grid(row=2, column=1)

        enddateandtime = tk.Label(create_appointment_window, text="End Date And Time: ")
        enddateandtime.grid(row=3, column=0)
        enddateandtime_box = create_appointment_window.search_entry = tk.Entry(create_appointment_window)
        enddateandtime_box.grid(row=3, column=1)

        search_button = tk.Button(create_appointment_window, text="Add client", command=self.add_appointment)
        search_button.grid(row=4, column=1)

        self.clientvariable = clientvariable
        self.staffvariable = staffvariable
        self.startdateandtime_box = startdateandtime_box
        self.enddateandtime_box = enddateandtime_box

        self.enddateandtime_box.bind("<Return>", self.add_appointment)

    def add_appointment(self):
        """
        checks if all appointment results are valid and then updates tables
        """
        clientvariable = self.clientvariable.get()
        clientvariable = (ast.literal_eval(clientvariable)[0])
        staffvariable = self.staffvariable.get()
        staffvariable = (ast.literal_eval(staffvariable)[0])
        try:
            datetime.strptime(self.startdateandtime_box.get(), '%Y-%m-%d %H:%M:%S')
            try:
                datetime.strptime(self.enddateandtime_box.get(), '%Y-%m-%d %H:%M:%S')
                self.cursor.execute(
                    """INSERT INTO appointments(ClientID, StaffID, StartDateAndTime, EndDateAndTime, AppointmentStatus) VALUES (?,?,?,?,?)""",
                    (clientvariable, staffvariable, self.startdateandtime_box.get(),
                     self.enddateandtime_box.get(), 'Active'))
                self.cursor.execute("""SELECT AppointmentID FROM appointments ORDER BY AppointmentID DESC LIMIT 1""")
                appointmentid = self.cursor.fetchone()
                appointmentid = appointmentid[0]       
                now = datetime.now()
                now = now.strftime('%Y-%m-%d %H:%M:%S')
                self.cursor.execute("""INSERT INTO transactions(DateAndTime, TransactionStatus) VALUES (?,?)""", (now, "Successful"))
                self.cursor.execute(
                    """SELECT TransactionID FROM transactions ORDER BY TransactionID DESC LIMIT 1""")
                transactionid = self.cursor.fetchone()
                transactionid = transactionid[0]
                self.cursor.execute("""UPDATE appointments SET TransactionID = ? WHERE AppointmentID = ?""",
                                    (transactionid, appointmentid,))
                self.db.commit()
                self.create_appointment_window.destroy()
                AppointmentsFrame.update_table(self)
            except ValueError:
                messagebox.showinfo("Error", "End date and time incorrect format (YYYY-MM-DD HH:MM:SS)")
        except ValueError:
            messagebox.showinfo("Error", "Start date and time incorrect format (YYYY-MM-DD HH:MM:SS)")
