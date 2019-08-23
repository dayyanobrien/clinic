# coding=utf-8

from ClientsTab import *
from StaffTab import *
from database_setup import *


class SwitchFrame(tk.Tk):
    """
    the initially run class, it creates the ability to change the
    frame of the window without creating a new one
    as well as making the initial frame LoginPage
    """

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)  # puts login frame at top
        self.geometry("1275x750")
        self.title("Physio Database")
        self.iconbitmap('logo.ico')

    def switch_frame(self, frame_class):
        """destroys the current frame and replaces it with specifed one"""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()  # destroys the login frame so the other frame (tabbed one) is showm
        self._frame = new_frame
        self._frame.grid(row=0, column=0)


class LoginFrame(tk.Frame):
    """
    creates the login page frame, allows the user to input the username
    and password and when the button is pressed it switches the frame
    to HomepageTab and shows all the tab options
    """

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        tk.Label(self, text="Username: ").grid(row=0, column=0, padx=(500, 0), pady=(250, 0))
        tk.Label(self, text="Password: ").grid(row=1, column=0, padx=(500, 0))
        self.un_entry = tk.Entry(self)
        self.un_entry.grid(row=0, column=1, padx=(0, 500), pady=(250, 0))
        self.pw_entry = tk.Entry(self, show='*')  # use stars for password
        self.pw_entry.grid(row=1, column=1, padx=(0, 500))

        self.username = self.un_entry.get()
        self.password = self.pw_entry.get()

        tk.Button(self, text="Login", command=self.check_login).grid(row=2, column=0, padx=(500, 0), pady=(0, 250))

    def check_login(self):
        """
        checks if the username and password is
        correct and then sets LoggedIn = True
        """

        username = self.un_entry.get()
        password = self.password = self.pw_entry.get()
        cursor.execute("""SELECT LoggedIn FROM staff WHERE Username = ? AND Password = ?""", (username, password))
        result = cursor.fetchone()
        if result:
            cursor.execute("""UPDATE staff SET LoggedIn = ? WHERE Username = ? AND Password = ?""",
                           (True, username, password))
            db.commit()
            self.master.switch_frame(TabFrame)  # puts tab frame on top
        else:
            messagebox.showinfo("Error", "Username and/or password incorrect")


class TabFrame(tk.Frame):
    """
    this is the frame which holds all the tabs, this allows users
    to select which tab they want to use
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        notebook = ttk.Notebook(parent)

        cursor.execute("""SELECT Position FROM staff WHERE LoggedIn = ?""", (True,))
        pos = cursor.fetchone()[0]  # does views to see which tabs to show
        if pos == 'IT                    ' or pos == 'Owner               ' or pos == 'Nurse               ' or pos == 'Physiotherapist' or pos == 'Receptionist     ':
            notebook.add(ClientsFrame(notebook), text='Clients')  # shows client tab
        if pos == 'IT                    ' or pos == 'Owner               ':
            notebook.add(StaffFrame(notebook), text='Staff')  # shows staff tab

        notebook.grid(row=0, column=0)


if __name__ == "__main__":
    SwitchFrame().mainloop()
