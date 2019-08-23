# coding=utf-8

import tkinter as Tkinter
import tkinter.ttk as ttk
import re
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import ast


class MedicalRecordsFrame(tk.Frame):
    """
    the frame for the medical records tab
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        medical_records_frame = tk.LabelFrame(self, text="Medical Records", padx=5, pady=5, width=1000, height=750)
        medical_records_frame.grid(row=0, column=0)

        notebook = ttk.Notebook(parent)

        OPTIONS = [
            "MedicalRecordID",
            "ClientID                ",
            "Sex                        ",
            "Gender                  ",
            "Blood Type           ",
            "Height                   ",
            "Mass                      "
        ]

        variable = StringVar(medical_records_frame)
        variable.set(OPTIONS[0])

        # Set the treeview
        medical_records_frame.tree = ttk.Treeview(medical_records_frame, height="33", selectmode='browse',
                                                  columns=(
                                                      'ClientID', 'Sex', 'Gender', 'Blood Type', 'Height/(m)',
                                                      'Mass/(kg)'))
        MedicalRecordsFrame.tree = medical_records_frame.tree
        medical_records_frame.tree.heading('#0', text='MedicalRecordID')
        medical_records_frame.tree.heading('#1', text='ClientID')
        medical_records_frame.tree.heading('#2', text='Sex')
        medical_records_frame.tree.heading('#3', text='Gender')
        medical_records_frame.tree.heading('#4', text='Blood Type')
        medical_records_frame.tree.heading('#5', text='Height/(m)')
        medical_records_frame.tree.heading('#6', text='Mass/(kg)')
        medical_records_frame.tree.column('#0', stretch=Tkinter.YES, width="140", minwidth="100")
        medical_records_frame.tree.column('#1', stretch=Tkinter.YES, width="105", minwidth="50")
        medical_records_frame.tree.column('#2', stretch=Tkinter.YES, width="90", minwidth="50")
        medical_records_frame.tree.column('#3', stretch=Tkinter.YES, width="140", minwidth="85")
        medical_records_frame.tree.column('#4', stretch=Tkinter.YES, width="140", minwidth="85")
        medical_records_frame.tree.column('#5', stretch=Tkinter.YES, width="105", minwidth="75")
        medical_records_frame.tree.column('#6', stretch=Tkinter.YES, width="105", minwidth="75")
        medical_records_frame.tree.grid(row=5, columnspan=50, rowspan=50, sticky='nsew')
        medical_records_frame.treeview = medical_records_frame.tree

        search = tk.Label(medical_records_frame, text="Search: ")
        search.grid(row=10, column=50)
        search_box = medical_records_frame.search_entry = tk.Entry(medical_records_frame)
        search_box.grid(row=10, column=51)
        dropdownsearch = OptionMenu(medical_records_frame, variable, *OPTIONS)
        dropdownsearch.grid(row=10, column=52)

        tk.Button(medical_records_frame, text="Search", command=self.search_table).grid(row=11, column=51)

        tk.Button(medical_records_frame, text="Edit a medical record", command=EditMedicalRecordFrame).grid(row=13,
                                                                                                            column=51)

        tk.Button(medical_records_frame, text="Delete selected medical record", command=self.delete_client).grid(row=15,
                                                                                                                 column=51)

        tk.Button(medical_records_frame, text="Calculate BMI", command=self.calculate_bmi).grid(row=17, column=51)

        pad = tk.Label(medical_records_frame, text="")
        pad.grid(row=10, column=55, padx=(0, 30))

        self.tree = medical_records_frame.tree
        self.variable = variable
        self.search_box = search_box
        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()
        self.update_table()
        
    def calculate_bmi(self):
        """
        calculates bmi of selected client
        """
        iid_selected = self.tree.focus()
        medical_record_id = self.tree.item(iid_selected, 'text')
        self.cursor.execute("""SELECT * FROM medicalrecords WHERE MedicalRecordID = ?""", (medical_record_id,))
        fetch = self.cursor.fetchone()
        try:
            height = float(fetch[5])
            mass = float(fetch[6])
            height_squared = height * height
            bmi = mass/height_squared
            bmi = round(bmi, 1)
            messagebox.showinfo("Alert", "The BMI of the selected client is " + str(bmi))
            self.db.commit()
            self.update_table()
        except TypeError:
            messagebox.showinfo("Error", "Mass and/or height is None")

    def delete_client(self):
        """
        deletes highlighted client
        """
        iid_selected = self.tree.focus()
        medical_record_id = self.tree.item(iid_selected, 'text')
        self.cursor.execute("""DELETE from medicalrecords WHERE MedicalRecordID = ? """, (medical_record_id,))
        self.cursor.execute("""DELETE from clients WHERE MedicalRecordID = ? """, (medical_record_id,))
        self.db.commit()
        self.update_table()

    def search_table(self):
        """
        searches for a keyword from a selected column and shows in treeview
        """
        drop_down = self.variable.get()
        search = self.search_box.get()
        if drop_down == "MedicalRecordID":
            self.cursor.execute("""SELECT * FROM medicalrecords WHERE MedicalRecordID LIKE ?""", ('%' + search + '%',))
        elif drop_down == "ClientID                ":
            self.cursor.execute("""SELECT * FROM medicalrecords WHERE ClientID LIKE ?""", ('%' + search + '%',))
            drop_down = "ClientID"
        elif drop_down == "Sex                        ":
            self.cursor.execute("""SELECT * FROM medicalrecords WHERE Sex LIKE ?""", ('%' + search + '%',))
            drop_down = "Sex"
        elif drop_down == "Gender                  ":
            self.cursor.execute("""SELECT * FROM medicalrecords WHERE Gender LIKE ?""", ('%' + search + '%',))
            drop_down = "Gender"
        elif drop_down == "Blood Type           ":
            self.cursor.execute("""SELECT * FROM medicalrecords WHERE BloodType LIKE ?""", ('%' + search + '%',))
            drop_down = "Blood Type"
        elif drop_down == "Height                   ":
            self.cursor.execute("""SELECT * FROM medicalrecords WHERE Height LIKE ?""", ('%' + search + '%',))
            drop_down = "Height"
        elif drop_down == "Mass                      ":
            self.cursor.execute("""SELECT * FROM medicalrecords WHERE Mass LIKE ?""", ('%' + search + '%',))
            drop_down = "Mass"
        self.tree.delete(*self.tree.get_children())
        rows = self.cursor.fetchall()
        f = open('medicalrecords.txt','w')
        f.write("--------------------------------------- Searched for '" + search + "' by " + drop_down + "---------------------------------------" + '\n')
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=row[1:])
            f.write('\n' + "MedicalRecordID: " + str(row[0]))
            f.write('\n' + "ClientID: "  + str(row[1]))
            f.write('\n' + "Sex: " + str(row[2]))
            f.write('\n' + "Gender: " + str(row[3]))
            f.write('\n' + "Blood Type: " + str(row[4]))
            f.write('\n' + "Height: " + str(row[5]))
            f.write('\n' + "Mass: " + str(row[6]))
            f.write('\n')
        messagebox.showinfo("Alert", "Medical records saved (medicalrecords.txt)")
        f.close()

    def update_table(self):
        """
        updates the treeview and fills it with all records
        in the ClientID table
        """
        self.cursor.execute("""SELECT * FROM medicalrecords""")
        result = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for item in result:
            self.tree.insert('', 'end', text=item[0], values=item[1:])


class EditMedicalRecordFrame(tk.Frame):
    """
    creates a new window and allows the user to edit a current client,
    when completed it will update the treeview in ClientTab
    """

    def __init__(self):
        tk.Frame.__init__(self)
        self.tree = MedicalRecordsFrame.tree
        edit_medical_record_window = tk.Toplevel(self)
        edit_medical_record_window.geometry("280x230")
        self.edit_medical_record_window = edit_medical_record_window

        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()

        SEXOPTIONS = [
            "",
            "M",
            "F"
        ]

        sexvariable = StringVar(edit_medical_record_window)
        sexvariable.set(SEXOPTIONS[0])

        GENDEROPTIONS = [
            "",
            "Male",
            "Female",
            "Other"
        ]

        gendervariable = StringVar(edit_medical_record_window)
        gendervariable.set(GENDEROPTIONS[0])

        BLOODTYPEOPTIONS = [
            "",
            "A+",
            "A-",
            "B+",
            "B-",
            "O+",
            "O-",
            "AB+",
            "AB-"
        ]

        bloodtypevariable = StringVar(edit_medical_record_window)
        bloodtypevariable.set(BLOODTYPEOPTIONS[0])

        self.cursor.execute("""SELECT MedicalRecordID FROM medicalrecords""")

        MEDICALRECORDOPTIONS = []
        result = self.cursor.fetchall()
        for item in result:
            MEDICALRECORDOPTIONS.append(item)

        medicalrecordvariable = StringVar(edit_medical_record_window)

        try:
            medicalrecordvariable.set(MEDICALRECORDOPTIONS[0])
        except IndexError:
            messagebox.showinfo("Error", "No medical records available")
            self.edit_medical_record_window.destroy()

        psa = tk.Label(edit_medical_record_window, text="Leave blank to keep column the same ")
        psa.grid(row=0, column=0, columnspan=2)

        medicalrecordid = tk.Label(edit_medical_record_window, text="MedicalRecordID: ")
        medicalrecordid.grid(row=1, column=0)
        medicalrecordidsearch = OptionMenu(edit_medical_record_window, medicalrecordvariable, *MEDICALRECORDOPTIONS)
        medicalrecordidsearch.grid(row=1, column=1)

        sex = tk.Label(edit_medical_record_window, text="Sex: ")
        sex.grid(row=2, column=0)
        sexsearch = OptionMenu(edit_medical_record_window, sexvariable, *SEXOPTIONS)
        sexsearch.grid(row=2, column=1)

        gender = tk.Label(edit_medical_record_window, text="Gender: ")
        gender.grid(row=3, column=0)
        gendersearch = OptionMenu(edit_medical_record_window, gendervariable, *GENDEROPTIONS)
        gendersearch.grid(row=3, column=1)

        bloodtype = tk.Label(edit_medical_record_window, text="Blood Type: ")
        bloodtype.grid(row=4, column=0)
        bloodtypesearch = OptionMenu(edit_medical_record_window, bloodtypevariable, *BLOODTYPEOPTIONS)
        bloodtypesearch.grid(row=4, column=1)

        height = tk.Label(edit_medical_record_window, text="Height (m): ")
        height.grid(row=5, column=0)
        height_box = edit_medical_record_window.search_entry = tk.Entry(edit_medical_record_window)
        height_box.grid(row=5, column=1)

        mass = tk.Label(edit_medical_record_window, text="Mass (kg): ")
        mass.grid(row=6, column=0)
        mass_box = edit_medical_record_window.search_entry = tk.Entry(edit_medical_record_window)
        mass_box.grid(row=6, column=1)

        search_button = tk.Button(edit_medical_record_window, text="Edit Medical Record",
                                  command=self.add_medical_record)
        search_button.grid(row=7, column=1)

        self.medicalrecordvariable = medicalrecordvariable
        self.sexvariable = sexvariable
        self.gendervariable = gendervariable
        self.bloodtypevariable = bloodtypevariable
        self.height_box = height_box
        self.mass_box = mass_box

        self.mass_box.bind("<Return>", self.add_medical_record)

    def add_medical_record(self):
        """
        checks if medical record results are valid and then updates tables
        """

        pattern = re.compile('\d+(\.\d+)?')
        
        medicalrecordvariable = self.medicalrecordvariable.get()
        medicalrecordvariable = (ast.literal_eval(medicalrecordvariable)[0])  # converts to tuple

        if self.sexvariable.get() == "":
            pass
        else:
            self.cursor.execute("""UPDATE medicalrecords SET Sex = ? WHERE MedicalRecordID = ?""",
                                (self.sexvariable.get(), medicalrecordvariable,))

        if self.gendervariable.get() == "":
            pass
        else:
            self.cursor.execute("""UPDATE medicalrecords SET Gender = ? WHERE MedicalRecordID = ?""",
                                (self.gendervariable.get(), medicalrecordvariable,))

        if self.bloodtypevariable.get() == "":
            pass
        else:
            self.cursor.execute("""UPDATE medicalrecords SET BloodType = ? WHERE MedicalRecordID = ?""",
                                (self.bloodtypevariable.get(), medicalrecordvariable,))

        match = re.search(pattern, self.height_box.get())
        if self.height_box.get() == "":
            pass
        elif match:
            if 1 < float(self.height_box.get()) < 2.5:
                self.cursor.execute("""UPDATE medicalrecords SET Height = ? WHERE MedicalRecordID = ?""",
                                    (self.height_box.get(), medicalrecordvariable,))
            else:
                messagebox.showinfo("Error", "Height is an invalid amount")
        else:
            messagebox.showinfo("Error", "Height contains non numerical characters")

        match = re.search(pattern, self.mass_box.get())
        if self.mass_box.get() == "":
            pass
        elif match:
            if 30 < float(self.mass_box.get()) < 500:
                self.cursor.execute("""UPDATE medicalrecords SET Mass = ? WHERE MedicalRecordID = ?""",
                                    (self.mass_box.get(), medicalrecordvariable,))
            else:
                messagebox.showinfo("Error", "Mass is an invalid amount")
        else:
            messagebox.showinfo("Error", "Mass contains non numerical characters")

        self.db.commit()
        self.edit_medical_record_window.destroy()
        MedicalRecordsFrame.update_table(self)
