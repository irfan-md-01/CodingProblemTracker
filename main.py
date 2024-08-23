from gui import Login, Registration, ProblemTracker
from database import Database
from auth import Auth
from tkinter import *

def proceed_to_dashboard():
    for widget in root.winfo_children():
        widget.destroy()
    ProblemTracker(root, db)  # dashboard    

def show_login_window():
    for widget in root.winfo_children():
        widget.destroy()
    Login(root, auth, show_register_window,proceed_to_dashboard)

def show_register_window():
    for widget in root.winfo_children():
        widget.destroy()
    Registration(root, auth, show_login_window)


if __name__ == '__main__':
    root = Tk()
    db = Database()
    auth = Auth(db)

    # Optionally, switch between Login and Register as needed
    show_login_window()

    root.mainloop()
