# coding=utf-8

import tkinter as Tkinter
import tkinter.ttk as ttk
import re
import sqlite3
from tkinter import *
import tkinter as tk
import ast
from tkinter import messagebox


class StaffFrame(tk.Frame):
    """
    the frame for the finances tab
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        staff_frame = tk.LabelFrame(self, text="Staff", padx=5, pady=5, width=1275, height=750)
        staff_frame.grid(row=0, column=0)

        OPTIONS = [
            "StaffID      ",
            "Prefix          ",
            "First Name",
            "Surname    ",
            "DOB            ",
            "Telephone",
            "Address      ",
            "Postcode    ",
            "Username  ",
            "Position   "
        ]

        variable = StringVar(staff_frame)
        variable.set(OPTIONS[0])

        # Set the treeview
        staff_frame.tree = ttk.Treeview(staff_frame, height="33", selectmode='browse',
                                        columns=(
                                            'Prefix', 'First Name', 'Surname', 'DOB', 'Telephone', 'Address',
                                            'Postcode', 'Username', 'Position'))
        StaffFrame.tree = staff_frame.tree
        staff_frame.tree.heading('#0', text='StaffID')
        staff_frame.tree.heading('#1', text='Prefix')
        staff_frame.tree.heading('#2', text='First Name')
        staff_frame.tree.heading('#3', text='Surname')
        staff_frame.tree.heading('#4', text='DOB')
        staff_frame.tree.heading('#5', text='Telephone')
        staff_frame.tree.heading('#6', text='Address')
        staff_frame.tree.heading('#7', text='Postcode')
        staff_frame.tree.heading('#8', text='Username')
        staff_frame.tree.heading('#9', text='Position')
        staff_frame.tree.column('#0', stretch=Tkinter.YES, width="75", minwidth="50")
        staff_frame.tree.column('#1', stretch=Tkinter.YES, width="75", minwidth="50")
        staff_frame.tree.column('#2', stretch=Tkinter.YES, width="75", minwidth="50")
        staff_frame.tree.column('#3', stretch=Tkinter.YES, width="85", minwidth="50")
        staff_frame.tree.column('#4', stretch=Tkinter.YES, width="75", minwidth="75")
        staff_frame.tree.column('#5', stretch=Tkinter.YES, width="110", minwidth="100")
        staff_frame.tree.column('#6', stretch=Tkinter.YES, width="145", minwidth='100')
        staff_frame.tree.column('#7', stretch=Tkinter.YES, width="75", minwidth="75")
        staff_frame.tree.column('#8', stretch=Tkinter.YES, width="100", minwidth='100')
        staff_frame.tree.column('#9', stretch=Tkinter.YES, width="95", minwidth="50")
        staff_frame.tree.grid(row=5, columnspan=50, rowspan=50, sticky='nsew')
        staff_frame.treeview = staff_frame.tree

        search = tk.Label(staff_frame, text="Search: ")
        search.grid(row=10, column=50)
        search_box = staff_frame.search_entry = tk.Entry(staff_frame)
        search_box.grid(row=10, column=51)
        dropdownsearch = OptionMenu(staff_frame, variable, *OPTIONS)
        dropdownsearch.grid(row=10, column=52)

        tk.Button(staff_frame, text="Search", command=self.search_table).grid(row=11, column=51)

        tk.Button(staff_frame, text="Add staff", command=CreateStaffFrame).grid(row=13, column=51)

        tk.Button(staff_frame, text="Edit staff", command=EditStaffFrame).grid(row=15, column=51)

        tk.Button(staff_frame, text="Delete selected staff", command=self.delete_staff).grid(row=17, column=51)

        pad = tk.Label(staff_frame, text="")
        pad.grid(row=10, column=55, padx=(0, 30))

        self.tree = staff_frame.tree
        self.variable = variable
        self.search_box = search_box
        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()
        self.update_table()

    def delete_staff(self):
        """
        deletes highlighted staff
        """
        iid_selected = self.tree.focus()
        staff_id = self.tree.item(iid_selected, 'text')

        self.cursor.execute("""DELETE from staff WHERE StaffID = ? """, (staff_id,))
        self.db.commit()
        self.update_table()

    def search_table(self):
        """
        searches for a keyword from a selected column and shows in treeview
        """
        drop_down = self.variable.get()
        search = self.search_box.get()
        if drop_down == "StaffID      ":
            self.cursor.execute("""SELECT * FROM staff WHERE StaffID LIKE ?""", ('%' + search + '%',))
            drop_down = "StaffID"
        elif drop_down == "Prefix          ":
            self.cursor.execute("""SELECT * FROM staff WHERE Prefix LIKE ?""", ('%' + search + '%',))
            drop_down = "Prefix"
        elif drop_down == "First Name":
            self.cursor.execute("""SELECT * FROM staff WHERE FirstName LIKE ?""", ('%' + search + '%',))
        elif drop_down == "Surname    ":
            self.cursor.execute("""SELECT * FROM staff WHERE Surname LIKE ?""", ('%' + search + '%',))
            drop_down = "Surname"
        elif drop_down == "DOB            ":
            self.cursor.execute("""SELECT * FROM staff WHERE DOB LIKE ?""", ('%' + search + '%',))
            drop_down = "DOB"
        elif drop_down == "Telephone":
            self.cursor.execute("""SELECT * FROM staff WHERE Telephone LIKE ?""", ('%' + search + '%',))
        elif drop_down == "Address      ":
            self.cursor.execute("""SELECT * FROM staff WHERE Address LIKE ?""", ('%' + search + '%',))
            drop_down = "Address"
        elif drop_down == "Postcode   ":
            self.cursor.execute("""SELECT * FROM staff WHERE Postcode LIKE ?""", ('%' + search + '%',))
            drop_down = "Postcode"
        elif drop_down == "Username  ":
            self.cursor.execute("""SELECT * FROM staff WHERE Username LIKE ?""", ('%' + search + '%',))
            drop_down = "Username"
        elif drop_down == "Position   ":
            self.cursor.execute("""SELECT * FROM staff WHERE Position LIKE ?""", ('%' + search + '%',))
            drop_down = "Position"
        self.tree.delete(*self.tree.get_children())
        rows = self.cursor.fetchall()
        f = open('staff.txt','w')
        f.write("--------------------------------------- Searched for '" + search + "' by " + drop_down + "---------------------------------------" + '\n')
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=row[1:])
            f.write('\n' + "StaffID: " + str(row[0]))
            f.write('\n' + "Prefix: " + str(row[1]))
            f.write('\n' + "First Name: " + str(row[2]))
            f.write('\n' + "Surname: " + str(row[3]))
            f.write('\n' + "DOB: " + str(row[4]))
            f.write('\n' + "Telephone: " + str(row[5]))
            f.write('\n' + "Address: " + str(row[6]))
            f.write('\n' + "Postcode: " + str(row[7]))
            f.write('\n' + "Username: " + str(row[8]))
            f.write('\n' + "Position: " + str(row[9]))
            f.write('\n')
        messagebox.showinfo("Alert", "Staff saved (staff.txt)")
        f.close()

    def update_table(self):
        """
        updates the treeview and fills it with all records
        in the staffid table
        """
        self.cursor.execute("""SELECT * FROM staff""")
        result = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for item in result:
            self.tree.insert('', 'end', text=item[0], values=item[1:10])


# noinspection PyCallByClass
class CreateStaffFrame(tk.Frame):
    """
    creates a new window and allows the user to create a new staff,
    when completed it will update the treeview in staffTab
    """

    def __init__(self):
        tk.Frame.__init__(self)
        self.tree = StaffFrame.tree
        create_staff_window = tk.Toplevel(self)
        create_staff_window.geometry("280x270")

        PREFIXOPTIONS = [
            "Dr",
            "Mr",
            "Mrs",
            "Ms",
            "Mx",
            "Prof",
            "Rev"
        ]

        variable = StringVar(create_staff_window)
        variable.set(PREFIXOPTIONS[0])

        POSITIONOPTIONS = [
            "Owner               ",
            "IT                    ",
            "Nurse               ",
            "Physiotherapist",
            "Receptionist     "
        ]

        positionvariable = StringVar(create_staff_window)
        positionvariable.set(POSITIONOPTIONS[0])

        position = tk.Label(create_staff_window, text="Position: ")
        position.grid(row=0, column=0)
        positiondropdownsearch = OptionMenu(create_staff_window, positionvariable, *POSITIONOPTIONS)
        positiondropdownsearch.grid(row=0, column=1)

        prefix = tk.Label(create_staff_window, text="Prefix: ")
        prefix.grid(row=1, column=0)
        dropdownsearch = OptionMenu(create_staff_window, variable, *PREFIXOPTIONS)
        dropdownsearch.grid(row=1, column=1)

        first_name = tk.Label(create_staff_window, text="First Name: ")
        first_name.grid(row=2, column=0)
        first_name_box = create_staff_window.search_entry = tk.Entry(create_staff_window)
        first_name_box.grid(row=2, column=1)

        surname = tk.Label(create_staff_window, text="Surname: ")
        surname.grid(row=3, column=0)
        surname_box = create_staff_window.search_entry = tk.Entry(create_staff_window)
        surname_box.grid(row=3, column=1)

        dob = tk.Label(create_staff_window, text="DOB (YYYY-MM-DD): ")
        dob.grid(row=4, column=0)
        dob_box = create_staff_window.search_entry = tk.Entry(create_staff_window)
        dob_box.grid(row=4, column=1)

        telephone = tk.Label(create_staff_window, text="Telephone: ")
        telephone.grid(row=5, column=0)
        telephone_box = create_staff_window.search_entry = tk.Entry(create_staff_window)
        telephone_box.grid(row=5, column=1)

        address = tk.Label(create_staff_window, text="Address: ")
        address.grid(row=6, column=0)
        address_box = create_staff_window.search_entry = tk.Entry(create_staff_window)
        address_box.grid(row=6, column=1)

        postcode = tk.Label(create_staff_window, text="Postcode: ")
        postcode.grid(row=7, column=0)
        postcode_box = create_staff_window.search_entry = tk.Entry(create_staff_window)
        postcode_box.grid(row=7, column=1)

        username = tk.Label(create_staff_window, text="Username: ")
        username.grid(row=8, column=0)
        username_box = create_staff_window.search_entry = tk.Entry(create_staff_window)
        username_box.grid(row=8, column=1)

        password = tk.Label(create_staff_window, text="Password: ")
        password.grid(row=9, column=0)
        password_box = create_staff_window.search_entry = tk.Entry(create_staff_window)
        password_box.grid(row=9, column=1)

        search_button = tk.Button(create_staff_window, text="Add staff", command=self.add_staff)
        search_button.grid(row=10, column=1)

        self.variable = variable
        self.first_name_box = first_name_box
        self.surname_box = surname_box
        self.dob_box = dob_box
        self.telephone_box = telephone_box
        self.address_box = address_box
        self.postcode_box = postcode_box
        self.positionvariable = positionvariable
        self.username_box = username_box
        self.password_box = password_box
        self.create_staff_window = create_staff_window
        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()

    def add_staff(self):
        """
        checks if add staff results are valid and then updates tables
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
                                            if len(self.username_box.get()) > 6:
                                                if len(self.password_box.get()) > 6:
                                                    try:
                                                        self.cursor.execute(
                                                            """INSERT INTO staff(Prefix, FirstName, Surname, DOB, Telephone, Address, 
                                                                Postcode, Username, Position, LoggedIn, Password) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                                                            (self.variable.get(), self.first_name_box.get(),
                                                             self.surname_box.get(),
                                                             self.dob_box.get(), self.telephone_box.get(),
                                                             self.address_box.get(),
                                                             self.postcode_box.get(), self.username_box.get(),
                                                             self.positionvariable.get(), False,
                                                             self.password_box.get()))
                                                        self.db.commit()
                                                        self.create_staff_window.destroy()
                                                        StaffFrame.update_table(self)
                                                    except sqlite3.IntegrityError:
                                                        messagebox.showinfo("Error", "Username not unique")
                                                else:
                                                    messagebox.showinfo("Error", "Password too short")
                                            else:
                                                messagebox.showinfo("Error", "Username too short")
                                        else:
                                            messagebox.showinfo("Error", "Postcode incorrect format")
                                    else:
                                        messagebox.showinfo("Error", "Address is an invalid length")
                                else:
                                    messagebox.showinfo("Error", "Telephone number contains non numeric characters")
                            else:
                                messagebox.showinfo("Error", "Telephone number is an invalid length. Must be 11 digits")
                        else:
                            messagebox.showinfo("Error", "DOB incorrect format")
                    else:
                        messagebox.showinfo("Error", "Surname is an invalid length")
                else:
                    messagebox.showinfo("Error", "Surname contains non alphabetical characters")
            else:
                messagebox.showinfo("Error", "First name is an invalid length")
        else:
            messagebox.showinfo("Error", "First name contains non alphabetical characters")


class EditStaffFrame(tk.Frame):
    """
    creates a new window and allows the user to edit a current staff,
    when completed it will update the treeview in staffTab
    """

    def __init__(self):
        tk.Frame.__init__(self)
        self.tree = StaffFrame.tree
        edit_staff_window = tk.Toplevel(self)
        edit_staff_window.geometry("280x310")
        self.edit_staff_window = edit_staff_window

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

        variable = StringVar(edit_staff_window)
        variable.set(PREFIXOPTIONS[0])

        self.cursor.execute("""SELECT StaffID FROM staff""")

        STAFFOPTIONS = []
        result = self.cursor.fetchall()
        for item in result:
            STAFFOPTIONS.append(item)

        staffvariable = StringVar(edit_staff_window)

        try:
            staffvariable.set(STAFFOPTIONS[0])
        except IndexError:
            messagebox.showinfo("Error", "No staff available")
            self.edit_staff_window.destroy()

        POSITIONOPTIONS = [
            "                        ",
            "Owner               ",
            "IT                    ",
            "Nurse               ",
            "Physiotherapist",
            "Receptionist    "
        ]

        positionvariable = StringVar(edit_staff_window)
        positionvariable.set(POSITIONOPTIONS[0])

        psa = tk.Label(edit_staff_window, text="Leave blank to keep column the same ")
        psa.grid(row=0, column=0, columnspan=2)

        staffid = tk.Label(edit_staff_window, text="StaffID: ")
        staffid.grid(row=1, column=0)
        staffidsearch = OptionMenu(edit_staff_window, staffvariable, *STAFFOPTIONS)
        staffidsearch.grid(row=1, column=1)

        position = tk.Label(edit_staff_window, text="Position: ")
        position.grid(row=2, column=0)
        positiondropdownsearch = OptionMenu(edit_staff_window, positionvariable, *POSITIONOPTIONS)
        positiondropdownsearch.grid(row=2, column=1)

        prefix = tk.Label(edit_staff_window, text="Prefix: ")
        prefix.grid(row=3, column=0)
        dropdownsearch = OptionMenu(edit_staff_window, variable, *PREFIXOPTIONS)
        dropdownsearch.grid(row=3, column=1)

        first_name = tk.Label(edit_staff_window, text="First Name: ")
        first_name.grid(row=4, column=0)
        first_name_box = edit_staff_window.search_entry = tk.Entry(edit_staff_window)
        first_name_box.grid(row=4, column=1)

        surname = tk.Label(edit_staff_window, text="Surname: ")
        surname.grid(row=5, column=0)
        surname_box = edit_staff_window.search_entry = tk.Entry(edit_staff_window)
        surname_box.grid(row=5, column=1)

        dob = tk.Label(edit_staff_window, text="DOB (YYYY-MM-DD): ")
        dob.grid(row=6, column=0)
        dob_box = edit_staff_window.search_entry = tk.Entry(edit_staff_window)
        dob_box.grid(row=6, column=1)

        telephone = tk.Label(edit_staff_window, text="Telephone: ")
        telephone.grid(row=7, column=0)
        telephone_box = edit_staff_window.search_entry = tk.Entry(edit_staff_window)
        telephone_box.grid(row=7, column=1)

        address = tk.Label(edit_staff_window, text="Address: ")
        address.grid(row=8, column=0)
        address_box = edit_staff_window.search_entry = tk.Entry(edit_staff_window)
        address_box.grid(row=8, column=1)

        postcode = tk.Label(edit_staff_window, text="Postcode: ")
        postcode.grid(row=9, column=0)
        postcode_box = edit_staff_window.search_entry = tk.Entry(edit_staff_window)
        postcode_box.grid(row=9, column=1)

        username = tk.Label(edit_staff_window, text="Username: ")
        username.grid(row=10, column=0)
        username_box = edit_staff_window.search_entry = tk.Entry(edit_staff_window)
        username_box.grid(row=10, column=1)

        password = tk.Label(edit_staff_window, text="Password: ")
        password.grid(row=11, column=0)
        password_box = edit_staff_window.search_entry = tk.Entry(edit_staff_window)
        password_box.grid(row=11, column=1)

        search_button = tk.Button(edit_staff_window, text="Edit staff", command=self.add_staff)
        search_button.grid(row=12, column=1)

        self.variable = variable
        self.staffvariable = staffvariable
        self.first_name_box = first_name_box
        self.surname_box = surname_box
        self.dob_box = dob_box
        self.telephone_box = telephone_box
        self.address_box = address_box
        self.postcode_box = postcode_box
        self.positionvariable = positionvariable
        self.username_box = username_box
        self.password_box = password_box

        self.postcode_box.bind("<Return>", self.add_staff)

    def add_staff(self):
        """
        checks if add staff results are valid and then updates tables
        """
        staffvariable = self.staffvariable.get()
        staffvariable = (ast.literal_eval(staffvariable)[0])  # converts to tuple

        if self.variable.get() == "":
            pass
        else:
            self.cursor.execute("""UPDATE staff SET Prefix = ? WHERE StaffID = ?""",
                                (self.variable.get(), staffvariable,))

        if self.positionvariable.get() == "                        ":
            pass
        else:
            self.cursor.execute("""UPDATE staff SET Position = ? WHERE StaffID = ?""",
                                (self.positionvariable.get(), staffvariable,))

        if self.first_name_box.get() == "":
            pass
        elif self.first_name_box.get().isalpha():
            if 20 > len(self.first_name_box.get()) > 2:
                self.cursor.execute("""UPDATE staff SET FirstName = ? WHERE StaffID = ?""",
                                    (self.first_name_box.get(), staffvariable,))
            else:
                messagebox.showinfo("Error", "First name is an invalid length")
        else:
            messagebox.showinfo("Error", "First name contains non alphabetical characters")

        if self.surname_box.get() == "":
            pass
        elif self.surname_box.get().isalpha():
            if 20 > len(self.surname_box.get()) > 2:
                self.cursor.execute("""UPDATE staff SET Surname = ? WHERE StaffID = ?""",
                                    (self.surname_box.get(), staffvariable,))
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
                self.cursor.execute("""UPDATE staff SET DOB = ? WHERE StaffID = ?""",
                                    (self.dob_box.get(), staffvariable,))
            else:
                messagebox.showinfo("Error", "DOB incorrect format")

        if self.telephone_box.get() == "":
            pass
        elif 10 < len(self.telephone_box.get()) < 12:
            if self.telephone_box.get().isdigit():
                self.cursor.execute("""UPDATE staff SET Telephone = ? WHERE StaffID = ?""",
                                    (self.telephone_box.get(), staffvariable,))
            else:
                messagebox.showinfo("Error", "Telephone number contains non numeric characters")
        else:
            messagebox.showinfo("Error", "Telephone number is an invalid length. Must be 11 digits")

        if self.address_box.get() == "":
            pass
        elif 50 > len(self.address_box.get()) > 5:
            self.cursor.execute("""UPDATE staff SET Address = ? WHERE StaffID = ?""",
                                (self.address_box.get(), staffvariable,))
        else:
            messagebox.showinfo("Error", "Address is an invalid length")

        if self.postcode_box.get() == "":
            pass
        else:
            pattern = r'(GIR|([A-Z-[QVX][0-9][0-9]?)|(([A-Z-[QVX][A-Z-[IJZ][0-9][0-9]?)|(([A-Z-[QVX][0-9][A-HJKSTUW])|([A-Z-[QVX][A-Z-[IJZ][0-9][ABEHMNPRVWXY]))))(?=( )?[0-9][A-Z-[CIKMOV]{2})'
            match = re.search(pattern, self.postcode_box.get())
            if match:
                self.cursor.execute("""UPDATE staff SET Postcode = ? WHERE StaffID = ?""",
                                    (self.postcode_box.get(), staffvariable,))
            else:
                messagebox.showinfo("Error", "Postcode incorrect format")

        if self.username_box.get() == "":
            pass
        elif len(self.username_box.get()) > 6:
            try:
                self.cursor.execute("""UPDATE staff SET Username = ? WHERE StaffID = ?""",
                                    (self.username_box.get(), staffvariable,))
            except sqlite3.IntegrityError:
                messagebox.showinfo("Error", "Username not unique")
        else:
            messagebox.showinfo("Error", "Username too short")

        if self.password_box.get() == "":
            pass
        elif len(self.password_box.get()) > 6:
            self.cursor.execute("""UPDATE staff SET Password = ? WHERE StaffID = ?""",
                                (self.password_box.get(), staffvariable,))
        else:
            messagebox.showinfo("Error", "Password too short")

        self.db.commit()
        self.edit_staff_window.destroy()
        StaffFrame.update_table(self)
