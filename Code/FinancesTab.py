# coding=utf-8

import tkinter as Tkinter
import tkinter.ttk as ttk
import re
import sqlite3
from tkinter import *
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import ast


class FinancesFrame(tk.Frame):
    """
    the frame for the finances tab
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        finances_frame = tk.LabelFrame(self, text="Finances", padx=5, pady=5, width=1250, height=750)
        finances_frame.grid(row=0, column=0)

        OPTIONS = [
            "TransactionID        ",
            "Difference              ",
            "Date And Time      ",
            "Transaction Status"
        ]

        variable = StringVar(finances_frame)
        variable.set(OPTIONS[0])

        # Set the treeview
        finances_frame.tree = ttk.Treeview(finances_frame, height="33", selectmode='browse',
                                           columns=(
                                               'Difference', 'Date And Time', 'Transaction Status'))
        FinancesFrame.tree = finances_frame.tree
        finances_frame.tree.heading('#0', text='TransactionID')
        finances_frame.tree.heading('#1', text='Difference/£')
        finances_frame.tree.heading('#2', text='Date And Time')
        finances_frame.tree.heading('#3', text='Transaction Status')
        finances_frame.tree.column('#0', stretch=Tkinter.YES, width="140", minwidth="140")
        finances_frame.tree.column('#1', stretch=Tkinter.YES, width="140", minwidth="140")
        finances_frame.tree.column('#2', stretch=Tkinter.YES, width="140", minwidth="140")
        finances_frame.tree.column('#3', stretch=Tkinter.YES, width="140", minwidth="140")
        finances_frame.tree.grid(row=5, columnspan=50, rowspan=50, sticky='nsew')
        finances_frame.treeview = finances_frame.tree

        search = tk.Label(finances_frame, text="Search: ")
        search.grid(row=10, column=50)
        search_box = finances_frame.search_entry = tk.Entry(finances_frame)
        search_box.grid(row=10, column=51)
        dropdownsearch = OptionMenu(finances_frame, variable, *OPTIONS)
        dropdownsearch.grid(row=10, column=52)

        save = tk.Label(finances_frame, text="Save transactions: ")
        save.grid(row=19, column=50)
        save_box = finances_frame.search_entry = tk.Entry(finances_frame)
        save_box.grid(row=19, column=51)

        tk.Button(finances_frame, text="Search", command=self.search_table).grid(row=11, column=51)

        tk.Button(finances_frame, text="Add a transaction", command=CreateFinancesFrame).grid(row=13, column=51)

        tk.Button(finances_frame, text="Edit a transaction", command=EditFinancesFrame).grid(row=15, column=51)

        tk.Button(finances_frame, text="Delete selected transaction", command=self.delete_transaction).grid(row=17, column=51)

        tk.Button(finances_frame, text="Save a transaction from a date", command=self.save_transaction_date).grid(row=20, column=51)

        pad = tk.Label(finances_frame, text="")
        pad.grid(row=10, column=55, padx=(0, 30))

        self.tree = finances_frame.tree
        self.variable = variable
        self.search_box = search_box
        self.save_box = save_box
        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()
        self.update_table()

    def save_transaction_date(self):
        date = self.save_box.get()
        pattern = r'(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])'
        match = re.search(pattern, date)
        if match:
            self.cursor.execute("""SELECT * FROM transactions WHERE DateAndTime LIKE ?""", ('%' + date + '%',))
            rows = self.cursor.fetchall()
            self.cursor.execute("""SELECT sum(Difference) FROM transactions WHERE DateAndTime LIKE ?""", ('%' + date + '%',))
            sum = self.cursor.fetchone()
            f = open('financesbydate.txt','w')
            f.write("--------------------" + date + "--------------------" + '\n')
            f.write("| TransactionID | Difference | TransactionStatus |"  + '\n')
            f.write("--------------------------------------------------")
            for row in rows:
                f.write('\n' + "       " + str(row[0]) + "             "  + str(row[1]) + "           " + row[3])
            f.write('\n' + '\n' + "Overall difference: £" + str(sum[0]))
            messagebox.showinfo("Alert", "Transaction saved (financesbydate.txt)")
            f.close()
        else:
            messagebox.showinfo("Error", "Date incorrect format (YYYY-MM-DD)")

    def delete_transaction(self):
        """
        deletes highlighted transaction
        """
        iid_selected = self.tree.focus()
        transaction_id = self.tree.item(iid_selected, 'text')

        self.cursor.execute("""DELETE from transactions WHERE TransactionID = ? """, (transaction_id,))
        self.cursor.execute("""DELETE from appointments WHERE TransactionID = ? """, (transaction_id,))
        self.db.commit()
        self.update_table()

    def search_table(self):
        """
        searches for a keyword from a selected column and shows in treeview
        """
        drop_down = self.variable.get()
        search = self.search_box.get()
        if drop_down == "TransactionID        ":
            self.cursor.execute("""SELECT * FROM transactions WHERE TransactionID LIKE ?""", ('%' + search + '%',))
            drop_down = "TransactionID"
        elif drop_down == "Difference              ":
            self.cursor.execute("""SELECT * FROM transactions WHERE Difference LIKE ?""", ('%' + search + '%',))
            drop_down = "Difference"
        elif drop_down == "Date And Time      ":
            self.cursor.execute("""SELECT * FROM transactions WHERE DateAndTime LIKE ?""", ('%' + search + '%',))
            drop_down = "Date and Time"
        elif drop_down == "Transaction Status":
            self.cursor.execute("""SELECT * FROM transactions WHERE TransactionStatus LIKE ?""", ('%' + search + '%',))
        self.tree.delete(*self.tree.get_children())
        rows = self.cursor.fetchall()
        f = open('finances.txt','w')
        f.write("------------------------ Searched for '" + search + "' by " + drop_down + "------------------------" + '\n')
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=row[1:])
            f.write('\n' + "TransactionID: " + str(row[0]))
            f.write('\n' + "Difference: "  + str(row[1]))
            f.write('\n' + "Date and Time: " + str(row[2]))
            f.write('\n' + "Transaction Status: " + str(row[3]))
            f.write('\n')
        messagebox.showinfo("Alert", "Transaction saved (finances.txt)")
        f.close()
        

    def update_table(self):
        """
        updates the treeview and fills it with all records
        in the transactions table
        """
        self.cursor.execute("""SELECT * FROM transactions""")
        result = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for item in result:
            self.tree.insert('', 'end', text=item[0], values=item[1:])


class CreateFinancesFrame(tk.Frame):
    """
    creates a new window and allows the user to create a new client,
    when completed it will update the treeview in ClientTab
    """

    def __init__(self):
        tk.Frame.__init__(self)
        self.tree = FinancesFrame.tree
        create_transaction_window = tk.Toplevel(self)
        create_transaction_window.geometry("260x80")

        difference = tk.Label(create_transaction_window, text="Difference: £")
        difference.grid(row=0, column=0)
        difference_box = create_transaction_window.search_entry = tk.Entry(create_transaction_window)
        difference_box.grid(row=0, column=1)

        dateandtime = tk.Label(create_transaction_window, text="Date and Time: ")
        dateandtime.grid(row=1, column=0)
        dateandtime_box = create_transaction_window.search_entry = tk.Entry(create_transaction_window)
        dateandtime_box.grid(row=1, column=1)
        
        search_button = tk.Button(create_transaction_window, text="Add transaction", command=self.add_transaction)
        search_button.grid(row=2, column=1)

        self.difference_box = difference_box
        self.dateandtime_box = dateandtime_box
        self.create_transaction_window = create_transaction_window
        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()

        self.dateandtime_box.bind("<Return>", self.add_transaction)

    def add_transaction(self):
        """
        checks if add client results are valid and then updates tables
        """
        pattern = re.compile('\d+(\.\d+)?')
        match = re.search(pattern, self.difference_box.get())
        if match:
            try:
                datetime.strptime(self.dateandtime_box.get(), '%Y-%m-%d %H:%M:%S')
                self.cursor.execute(
                                    """INSERT INTO transactions(Difference, DateAndTime, TransactionStatus) VALUES (?,?,?)""",
                                    (self.difference_box.get(), self.dateandtime_box.get(), "Successful",))
                self.db.commit()
                self.create_transaction_window.destroy()
                FinancesFrame.update_table(self)
            except ValueError:
                messagebox.showinfo("Error", "Transaction format incorrect")
        else:
            messagebox.showinfo("Error", "Difference is invalid format")


class EditFinancesFrame(tk.Frame):
    """
    creates a new window and allows the user to edit a current client,
    when completed it will update the treeview in TransactionTab
    """

    def __init__(self):
        tk.Frame.__init__(self)
        self.tree = FinancesFrame.tree
        edit_transaction_window = tk.Toplevel(self)
        edit_transaction_window.geometry("280x150")

        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()

        self.cursor.execute("""SELECT TransactionID FROM transactions""")

        TRANSACTIONOPTIONS = []
        result = self.cursor.fetchall()
        for item in result:
            TRANSACTIONOPTIONS.append(item)

        transactionvariable = StringVar(edit_transaction_window)
        transactionvariable.set(TRANSACTIONOPTIONS[0])

        psa = tk.Label(edit_transaction_window, text="Leave blank to keep column the same ")
        psa.grid(row=0, column=0, columnspan=2)

        clientid = tk.Label(edit_transaction_window, text="TransactionID: ")
        clientid.grid(row=1, column=0)
        clientidsearch = OptionMenu(edit_transaction_window, transactionvariable, *TRANSACTIONOPTIONS)
        clientidsearch.grid(row=1, column=1)

        difference = tk.Label(edit_transaction_window, text="Difference: £")
        difference.grid(row=2, column=0)
        difference_box = edit_transaction_window.search_entry = tk.Entry(edit_transaction_window)
        difference_box.grid(row=2, column=1)

        dateandtime = tk.Label(edit_transaction_window, text="Date and Time: ")
        dateandtime.grid(row=3, column=0)
        dateandtime_box = edit_transaction_window.search_entry = tk.Entry(edit_transaction_window)
        dateandtime_box.grid(row=3, column=1)
    

        search_button = tk.Button(edit_transaction_window, text="Edit client", command=self.add_transaction)
        search_button.grid(row=4, column=1)

        self.transactionvariable = transactionvariable
        self.difference_box = difference_box
        self.dateandtime_box = dateandtime_box
        self.edit_transaction_window = edit_transaction_window
        self.db = sqlite3.connect('clinic.db')
        self.cursor = self.db.cursor()

        self.dateandtime_box.bind("<Return>", self.add_transaction)

    def add_transaction(self):
        """
        checks if all transaction results are valid and then updates tables
        """
        transactionvariable = self.transactionvariable.get()
        transactionvariable = (ast.literal_eval(transactionvariable)[0])  # converts to tuple
        pattern = re.compile('\d+(\.\d+)?')
        match = re.search(pattern, self.difference_box.get())
        if self.difference_box.get() == "":
            pass
        else:
            if match: 
                self.cursor.execute("""UPDATE transactions SET Difference = ? WHERE TransactionID = ?""",
                                    (self.difference_box.get(), transactionvariable,))
            else:
                messagebox.showinfo("Error", "Transaction incorrect format (+/-DD)")

        if self.dateandtime_box.get() == "":
            pass
        else:
            try:
                datetime.strptime(self.dateandtime_box.get(), '%Y-%m-%d %H:%M:%S') 
                self.cursor.execute("""UPDATE transactions SET DateAndTime = ? WHERE TransactionID = ?""",
                                    (self.dateandtime_box.get(), transactionvariable,))
            except ValueError:
                messagebox.showinfo("Error", "Date and time incorrect format (YYYY-MM-DD HH:MM:SS)")

        self.db.commit()
        self.edit_transaction_window.destroy()
        FinancesFrame.update_table(self)
