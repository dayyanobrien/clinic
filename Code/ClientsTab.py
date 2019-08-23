# coding=utf-8

import sqlite3
import tkinter as Tkinter
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
import ast


class ClientsFrame(tk.Frame):
    """
    the frame for the clients tab
    """

    def __init__(self, parent, *args, **kwargs):
        """
        intially run function, sets up design of the entire page
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)

        clients_frame = tk.LabelFrame(self, text="Clients", padx=5, pady=5, width=1275, height=750) #creates the client frame
        clients_frame.grid(row=0, column=0)

        OPTIONS = [
            "ClientID               ",
            "MedicalRecordID",
            "Prefix                   ",
            "First Name           ",
            "Surname              ",
            "DOB                      ",
            "Telephone           ",
            "Address                ",
            "Postcode              ",
        ] #creates the options for the dropdown menu on serach

        variable = StringVar(clients_frame)
        variable.set(OPTIONS[0]) #starts the dropdown menu on ClientID

        # Set the treeview
        clients_frame.tree = ttk.Treeview(clients_frame, height="33", selectmode='browse',
                                          columns=(
                                              'MedicalRecordID', 'Prefix', 'First Name', 'Surname', 'DOB', 'Telephone', 'Address',
                                              'Postcode')) #creates the treeview
        ClientsFrame.tree = clients_frame.tree
        clients_frame.tree.heading('#0', text='ClientID')
        clients_frame.tree.heading('#1', text='MedicalRecordID')
        clients_frame.tree.heading('#2', text='Prefix')
        clients_frame.tree.heading('#3', text='First Name')
        clients_frame.tree.heading('#4', text='Surname')
        clients_frame.tree.heading('#5', text='DOB')
        clients_frame.tree.heading('#6', text='Telephone')
        clients_frame.tree.heading('#7', text='Address')
        clients_frame.tree.heading('#8', text='Postcode')
        clients_frame.tree.column('#0', stretch=Tkinter.YES, width="75", minwidth="50")
        clients_frame.tree.column('#1', stretch=Tkinter.YES, width="100", minwidth="100")
        clients_frame.tree.column('#2', stretch=Tkinter.YES, width="75", minwidth="50")
        clients_frame.tree.column('#3', stretch=Tkinter.YES, width="110", minwidth="85")
        clients_frame.tree.column('#4', stretch=Tkinter.YES, width="110", minwidth="85")
        clients_frame.tree.column('#5', stretch=Tkinter.YES, width="75", minwidth="75")
        clients_frame.tree.column('#6', stretch=Tkinter.YES, width="100", minwidth="100")
        clients_frame.tree.column('#7', stretch=Tkinter.YES, width="155", minwidth='100')
        clients_frame.tree.column('#8', stretch=Tkinter.YES, width="75", minwidth="75")
        clients_frame.tree.grid(row=5, columnspan=50, rowspan=50, sticky='nsew')
        clients_frame.treeview = clients_frame.tree

        search = tk.Label(clients_frame, text="Search: ")
        search.grid(row=10, column=50)
        search_box = clients_frame.search_entry = tk.Entry(clients_frame)
        search_box.grid(row=10, column=51)
        dropdownsearch = OptionMenu(clients_frame, variable, *OPTIONS)
        dropdownsearch.grid(row=10, column=52)

        tk.Button(clients_frame, text="Search", command=self.search_table).grid(row=11, column=51)

        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()
        
        self.cursor.execute("""SELECT Position FROM staff WHERE LoggedIn = ?""",(True,))
        pos = self.cursor.fetchone()[0]
        if pos == 'Owner               ' or pos == 'Nurse               ' or pos == 'Physiotherapist' or pos == 'Receptionist     ': #a view - only allows certain members to view it
            tk.Button(clients_frame, text="Add a client", command=CreateClientFrame).grid(row=13, column=51)

            tk.Button(clients_frame, text="Edit a client", command=EditClientFrame).grid(row=15, column=51)

            tk.Button(clients_frame, text="Delete selected client", command=self.delete_client).grid(row=17, column=51)

        pad = tk.Label(clients_frame, text="")
        pad.grid(row=10, column=55, padx=(0, 30))

        self.tree = clients_frame.tree
        self.variable = variable
        self.search_box = search_box
        self.update_table()

    def delete_client(self):
        """
        deletes highlighted client
        """
        iid_selected = self.tree.focus() #finds the iid of the highlighted box
        client_id = self.tree.item(iid_selected, 'text') #gets the client id from the iid of the highlighted box

        self.cursor.execute("""DELETE from clients WHERE ClientID = ? """, (client_id,))
        self.cursor.execute("""DELETE from medicalrecords WHERE ClientID = ? """, (client_id,))
        self.cursor.execute("""DELETE from appointments WHERE ClientID = ? """, (client_id,))
        self.db.commit()
        self.update_table()

    def search_table(self):
        """
        searches for a keyword from a selected column and shows in treeview
        """
        drop_down = self.variable.get()
        search = self.search_box.get()
        if drop_down == "ClientID               ":
            self.cursor.execute("""SELECT * FROM clients WHERE ClientID LIKE ?""", ('%' + search + '%',))
            drop_down = "ClientID"
        elif drop_down == "MedicalRecordID":
            self.cursor.execute("""SELECT * FROM clients WHERE MedicalRecordID LIKE ?""", ('%' + search + '%',))
        elif drop_down == "Prefix                   ":
            self.cursor.execute("""SELECT * FROM clients WHERE Prefix LIKE ?""", ('%' + search + '%',))
            drop_down = "Prefix"
        elif drop_down == "First Name           ":
            self.cursor.execute("""SELECT * FROM clients WHERE FirstName LIKE ?""", ('%' + search + '%',))
            drop_down = "First Name"
        elif drop_down == "Surname              ":
            self.cursor.execute("""SELECT * FROM clients WHERE Surname LIKE ?""", ('%' + search + '%',))
            drop_down = "Surname"
        elif drop_down == "DOB                      ":
            self.cursor.execute("""SELECT * FROM clients WHERE DOB LIKE ?""", ('%' + search + '%',))
            drop_down = "DOB"
        elif drop_down == "Telephone           ":
            self.cursor.execute("""SELECT * FROM clients WHERE Telephone LIKE ?""", ('%' + search + '%',))
            drop_down = "Telephone"
        elif drop_down == "Address                ":
            self.cursor.execute("""SELECT * FROM clients WHERE Address LIKE ?""", ('%' + search + '%',))
            drop_down = "Address"
        elif drop_down == "Postcode              ":
            self.cursor.execute("""SELECT * FROM clients WHERE Postcode LIKE ?""", ('%' + search + '%',))
            drop_down = "Postcode"
        self.tree.delete(*self.tree.get_children()) #clears treeview table
        rows = self.cursor.fetchall()
        f = open('clients.txt','w')
        f.write("--------------------------------------- Searched for '" + search + "' by " + drop_down + "---------------------------------------" + '\n')
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=row[1:])
            f.write('\n' + "ClientID: " + str(row[0]))
            f.write('\n' + "MedicalRecordID: "  + str(row[1]))
            f.write('\n' + "Prefix: " + str(row[2]))
            f.write('\n' + "First Name: " + str(row[3]))
            f.write('\n' + "Surname: " + str(row[4]))
            f.write('\n' + "DOB: " + str(row[5]))
            f.write('\n' + "Telephone: " + str(row[6]))
            f.write('\n' + "Address: " + str(row[7]))
            f.write('\n' + "Postcode: " + str(row[8]))
            f.write('\n')
        messagebox.showinfo("Alert", "Clients saved (clients.txt)")
        f.close()

    def update_table(self):
        """
        updates the treeview and fills it with all records
        in the ClientID table
        """
        self.cursor.execute("""SELECT * FROM clients""")
        result = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children()) #clears table
        for item in result:
           self.tree.insert('', 'end', text=item[0], values=item[1:]) #updates table


class CreateClientFrame(tk.Frame):
    """
    creates a new window and allows the user to create a new client,
    when completed it will update the treeview in ClientTab
    """

    def __init__(self):
        tk.Frame.__init__(self)
        self.tree = ClientsFrame.tree
        create_client_window = tk.Toplevel(self) 
        create_client_window.geometry("280x230") #creates the new window with geomtery so you can create a client

        PREFIXOPTIONS = [
            "Dr",
            "Mr",
            "Mrs",
            "Ms",
            "Mx",
            "Prof",
            "Rev"
        ]

        variable = StringVar(create_client_window)
        variable.set(PREFIXOPTIONS[0])

        prefix = tk.Label(create_client_window, text="Prefix: ")
        prefix.grid(row=0, column=0)
        dropdownsearch = OptionMenu(create_client_window, variable, *PREFIXOPTIONS)
        dropdownsearch.grid(row=0, column=1)

        first_name = tk.Label(create_client_window, text="First Name: ")
        first_name.grid(row=1, column=0)
        first_name_box = create_client_window.search_entry = tk.Entry(create_client_window)
        first_name_box.grid(row=1, column=1)

        surname = tk.Label(create_client_window, text="Surname: ")
        surname.grid(row=2, column=0)
        surname_box = create_client_window.search_entry = tk.Entry(create_client_window)
        surname_box.grid(row=2, column=1)

        dob = tk.Label(create_client_window, text="DOB: ")
        dob.grid(row=3, column=0)
        dob_box = create_client_window.search_entry = tk.Entry(create_client_window)
        dob_box.grid(row=3, column=1)

        telephone = tk.Label(create_client_window, text="Telephone: ")
        telephone.grid(row=4, column=0)
        telephone_box = create_client_window.search_entry = tk.Entry(create_client_window)
        telephone_box.grid(row=4, column=1)

        address = tk.Label(create_client_window, text="Address: ")
        address.grid(row=5, column=0)
        address_box = create_client_window.search_entry = tk.Entry(create_client_window)
        address_box.grid(row=5, column=1)

        postcode = tk.Label(create_client_window, text="Postcode: ")
        postcode.grid(row=6, column=0)
        postcode_box = create_client_window.search_entry = tk.Entry(create_client_window)
        postcode_box.grid(row=6, column=1)

        search_button = tk.Button(create_client_window, text="Add client", command=self.add_client)
        search_button.grid(row=7, column=1)

        self.variable = variable
        self.first_name_box = first_name_box
        self.surname_box = surname_box
        self.dob_box = dob_box
        self.telephone_box = telephone_box
        self.address_box = address_box
        self.postcode_box = postcode_box
        self.create_client_window = create_client_window
        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()

    def add_client(self):
        """
        checks if add client results are valid and then updates tables
        """
        if self.first_name_box.get().isalpha():
            if 20 > len(self.first_name_box.get()) > 2:
                if self.surname_box.get().isalpha():
                    if 20 > len(self.surname_box.get()) > 2:
                        pattern = r'(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])'
                        match = re.search(pattern, self.dob_box.get())
                        if match:
                            if 10 < len(self.telephone_box.get()) < 12:
                                if self.telephone_box.get().isdigit():
                                    if 50 > len(self.address_box.get()) > 5:
                                        pattern = r'(GIR|([A-Z-[QVX][0-9][0-9]?)|(([A-Z-[QVX][A-Z-[IJZ][0-9][0-9]?)|(([A-Z-[QVX][0-9][A-HJKSTUW])|([A-Z-[QVX][A-Z-[IJZ][0-9][ABEHMNPRVWXY]))))(?=( )?[0-9][A-Z-[CIKMOV]{2})'
                                        match = re.search(pattern, self.postcode_box.get())
                                        if match:
                                            self.cursor.execute(
                                                """INSERT INTO clients(Prefix, FirstName, Surname, DOB, Telephone, Address, Postcode) VALUES (?,?,?,?,?,?,?)""",
                                                (self.variable.get(), self.first_name_box.get(), self.surname_box.get(),
                                                 self.dob_box.get(), self.telephone_box.get(), self.address_box.get(),
                                                 self.postcode_box.get(),))
                                            self.cursor.execute(
                                                """SELECT ClientID FROM clients ORDER BY ClientID DESC LIMIT 1"""
                                            )
                                            clientid = self.cursor.fetchone()
                                            clientid = clientid[0]
                                            self.cursor.execute(
                                                """INSERT INTO medicalrecords(ClientID) VALUES (?)""", (clientid,))
                                            self.cursor.execute(
                                                """SELECT MedicalRecordID FROM medicalrecords ORDER BY MedicalRecordID DESC LIMIT 1"""
                                            )
                                            medicalrecordid = self.cursor.fetchone()
                                            medicalrecordid = medicalrecordid[0]
                                            self.cursor.execute(
                                                """UPDATE clients SET MedicalRecordID = ? WHERE ClientID = ?""",
                                                (medicalrecordid, clientid,))
                                            self.db.commit()
                                            self.create_client_window.destroy()
                                            ClientsFrame.update_table(self)
                                        else:
                                            messagebox.showinfo("Error", "Postcode incorrect format")
                                    else:
                                        messagebox.showinfo("Error", "Address is an invalid length")
                                else:
                                    messagebox.showinfo("Error", "Telephone number contains non numeric characters")
                            else:
                                messagebox.showinfo("Error", "Telephone number is an invalid length. Must be 11 digits")
                        else:
                            messagebox.showinfo("Error", "DOB incorrect format (YYYY-MM-DD)")
                    else:
                        messagebox.showinfo("Error", "Surname is an invalid length")
                else:
                    messagebox.showinfo("Error", "Surname contains non alphabetical characters")
            else:
                messagebox.showinfo("Error", "First name is an invalid length")
        else:
            messagebox.showinfo("Error", "First name contains non alphabetical characters")


class EditClientFrame(tk.Frame):
    """
    creates a new window and allows the user to edit a current client,
    when completed it will update the treeview in ClientTab
    """

    def __init__(self):
        tk.Frame.__init__(self)
        self.tree = ClientsFrame.tree
        edit_client_window = tk.Toplevel(self)
        edit_client_window.geometry("280x230")
        self.edit_client_window = edit_client_window

        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()

        PREFIXOPTIONS = [
            "",
            "Dr",
            "Mr",
            "Mrs",
            "Ms",
            "Mx",
            "Prof",
            "Rev"
        ]

        variable = StringVar(edit_client_window)
        variable.set(PREFIXOPTIONS[0])

        self.cursor.execute("""SELECT ClientID FROM clients""")

        CLIENTOPTIONS = []
        result = self.cursor.fetchall()
        for item in result:
            CLIENTOPTIONS.append(item)

        clientvariable = StringVar(edit_client_window)

        try:
            clientvariable.set(CLIENTOPTIONS[0]) #checks if there are any clients already
        except IndexError:
            messagebox.showinfo("Error", "No clients available")
            self.edit_client_window.destroy()

        psa = tk.Label(edit_client_window, text="Leave blank to keep column the same ")
        psa.grid(row=0, column=0, columnspan=2)

        clientid = tk.Label(edit_client_window, text="ClientID: ")
        clientid.grid(row=1, column=0)
        clientidsearch = OptionMenu(edit_client_window, clientvariable, *CLIENTOPTIONS)
        clientidsearch.grid(row=1, column=1)

        prefix = tk.Label(edit_client_window, text="Prefix: ")
        prefix.grid(row=2, column=0)
        dropdownsearch = OptionMenu(edit_client_window, variable, *PREFIXOPTIONS)
        dropdownsearch.grid(row=2, column=1)

        first_name = tk.Label(edit_client_window, text="First Name: ")
        first_name.grid(row=3, column=0)
        first_name_box = edit_client_window.search_entry = tk.Entry(edit_client_window)
        first_name_box.grid(row=3, column=1)

        surname = tk.Label(edit_client_window, text="Surname: ")
        surname.grid(row=4, column=0)
        surname_box = edit_client_window.search_entry = tk.Entry(edit_client_window)
        surname_box.grid(row=4, column=1)

        dob = tk.Label(edit_client_window, text="DOB (YYYY-MM-DD): ")
        dob.grid(row=5, column=0)
        dob_box = edit_client_window.search_entry = tk.Entry(edit_client_window)
        dob_box.grid(row=5, column=1)

        telephone = tk.Label(edit_client_window, text="Telephone: ")
        telephone.grid(row=6, column=0)
        telephone_box = edit_client_window.search_entry = tk.Entry(edit_client_window)
        telephone_box.grid(row=6, column=1)

        address = tk.Label(edit_client_window, text="Address: ")
        address.grid(row=7, column=0)
        address_box = edit_client_window.search_entry = tk.Entry(edit_client_window)
        address_box.grid(row=7, column=1)

        postcode = tk.Label(edit_client_window, text="Postcode: ")
        postcode.grid(row=8, column=0)
        postcode_box = edit_client_window.search_entry = tk.Entry(edit_client_window)
        postcode_box.grid(row=8, column=1)

        search_button = tk.Button(edit_client_window, text="Edit client", command=self.add_client)
        search_button.grid(row=9, column=1)

        self.variable = variable
        self.clientvariable = clientvariable
        self.first_name_box = first_name_box
        self.surname_box = surname_box
        self.dob_box = dob_box
        self.telephone_box = telephone_box
        self.address_box = address_box
        self.postcode_box = postcode_box

        self.postcode_box.bind("<Return>", self.add_client)

    def add_client(self):
        """
        checks if add client results are valid and then updates tables
        """
        
        clientvariable = self.clientvariable.get()
        clientvariable = (ast.literal_eval(clientvariable)[0])  # converts to tuple

        if self.variable.get() == "":
            pass
        else:
            self.cursor.execute("""UPDATE clients SET Prefix = ? WHERE ClientID = ?""",
                                (self.variable.get(), clientvariable,))

        if self.first_name_box.get() == "":
            pass
        elif self.first_name_box.get().isalpha():
            if 20 > len(self.first_name_box.get()) > 2:
                self.cursor.execute("""UPDATE clients SET FirstName = ? WHERE ClientID = ?""",
                                    (self.first_name_box.get(), clientvariable,))
            else:
                messagebox.showinfo("Error", "First name is an invalid length")
        else:
            messagebox.showinfo("Error", "First name contains non alphabetical characters")

        if self.surname_box.get() == "":
            pass
        elif self.surname_box.get().isalpha():
            if 20 > len(self.surname_box.get()) > 2:
                self.cursor.execute("""UPDATE clients SET Surname = ? WHERE ClientID = ?""",
                                    (self.surname_box.get(), clientvariable,))
            else:
                messagebox.showinfo("Error", "Surname is an invalid length")
        else:
            messagebox.showinfo("Error", "Surname contains non alphabetical characters")

        if self.dob_box.get() == "":
            pass
        else:
            pattern = r'(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])'
            match = re.search(pattern, self.dob_box.get())
            if match:
                self.cursor.execute("""UPDATE clients SET DOB = ? WHERE ClientID = ?""",
                                    (self.dob_box.get(), clientvariable,))
            else:
                messagebox.showinfo("Error", "DOB incorrect format")

        if self.telephone_box.get() == "":
            pass
        elif 10 < len(self.telephone_box.get()) < 12:
            if self.telephone_box.get().isdigit():
                self.cursor.execute("""UPDATE clients SET Telephone = ? WHERE ClientID = ?""",
                                    (self.telephone_box.get(), clientvariable,))
            else:
                messagebox.showinfo("Error", "Telephone number contains non numeric characters")
        else:
            messagebox.showinfo("Error", "Telephone number is an invalid length. Must be 11 digits")

        if self.address_box.get() == "":
            pass
        elif 50 > len(self.address_box.get()) > 5:
            self.cursor.execute("""UPDATE clients SET Address = ? WHERE ClientID = ?""",
                                (self.address_box.get(), clientvariable,))
        else:
            messagebox.showinfo("Error", "Address is an invalid length")

        if self.postcode_box.get() == "":
            pass
        else:
            pattern = r'(GIR|([A-Z-[QVX][0-9][0-9]?)|(([A-Z-[QVX][A-Z-[IJZ][0-9][0-9]?)|(([A-Z-[QVX][0-9][A-HJKSTUW])|([A-Z-[QVX][A-Z-[IJZ][0-9][ABEHMNPRVWXY]))))(?=( )?[0-9][A-Z-[CIKMOV]{2})'
            match = re.search(pattern, self.postcode_box.get())
            if match:
                self.cursor.execute("""UPDATE clients SET Postcode = ? WHERE ClientID = ?""",
                                    (self.postcode_box.get(), clientvariable,))
            else:
                messagebox.showinfo("Error", "Postcode incorrect format")

        self.db.commit()
        self.edit_client_window.destroy()
        ClientsFrame.update_table(self)
