from tkinter import *
from tkinter import ttk 
import tkinter.messagebox as tmsg
from PIL import Image, ImageTk
from auth import Auth  
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def solve():
    pass


class Registration(Tk):
    def __init__(self, root, auth, show_login_window):
        self.auth = auth
        self.root = root
        root.title("Register")
        root.geometry("450x450")
        root.configure(bg="#f0f0f0")
        frame = Frame(root,bd=2,bg='#ffffff', relief=SOLID, padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        Label(frame, text="Create an Account", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333333").grid(row=0, column=0, columnspan=3, pady=(0, 20))

        self.username_label = Label(frame, text="Username",bg='#ffffff',font=("Arial", 12))
        self.username_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.username_entry =Entry(frame, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        self.email_label = Label(frame, text="Email",bg='#ffffff',font=("Arial", 12 ))
        self.email_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.email_entry = Entry(frame, font=("Arial", 12))
        self.email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        self.contact_label = Label(frame, text="Contact Number",bg='#ffffff', font=("Arial", 12))
        self.contact_label.grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.contact_entry = Entry(frame, font=("Arial", 12))
        self.contact_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        self.password_label = Label(frame, text="Enter Password",bg='#ffffff', font=("Arial", 12))
        self.password_label.grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.password_entry = Entry(frame, show='*', font=("Arial", 12))
        self.password_entry.grid(row=4, column=1,padx=10, pady=5, sticky="we")

        self.repassword_label = Label(frame, text="Re-Enter Password",bg='#ffffff', font=("Arial", 12))
        self.repassword_label.grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.repassword_entry = Entry(frame, show='*',font=("Arial", 12))
        self.repassword_entry.grid(row=5, column=1,padx=10, pady=5, sticky="we")

        self.register_button = Button(frame, text="Register", font=("Arial", 12, "bold"),command=self.register, bg="#4CAF50", fg="#ffffff", relief="raised")
        self.register_button.grid(row=6, column=0, columnspan=3, pady=20)

        self.switch_button = Button(frame, text="Switch to Login",font=("Arial", 12, "bold"),command=show_login_window, bg="#2196F3", fg="#ffffff", relief="raised")
        self.switch_button.grid(row=7, column=0, columnspan=3)


        # frame.place(x=100, y=100)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        repassword = self.repassword_entry.get()
        email = self.email_entry.get()
        phone = self.contact_entry.get()

        if username and password and repassword and email and phone:
            success = self.auth.register_user(username, password, email, phone)
            if success:
                tmsg.showinfo("Success", "User registered successfully!")
            else:
                tmsg.showerror("Error", "Username already exists!")
        else:
            tmsg.showerror("Error", "Please enter all data.")
        
       

class Login(Tk):        
    def __init__(self, root, auth, show_register_window, proceed_to_dashboard):
        # super().__init__()
        self.auth = auth
        self.root = root
        self.root.title("Login")
        # self.root.configure( highlightthickness=5, highlightcolor="blue", relief="sunken")
        root.geometry("500x350")
        root.resizable(False, False)
        self.proceed_to_dashboard = proceed_to_dashboard

        self.image = Image.open("temp_login.jpg")
        self.photo = ImageTk.PhotoImage(self.image)

        self.canvas = Canvas(root, width=500, height=350)
        self.canvas.pack(fill=BOTH, expand=True)

        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

        frame = Frame(self.canvas,bd=2,bg='white', relief=SOLID, padx=20, pady=10)
        self.canvas.create_window((250, 250), window=frame, anchor='center') 

        self.username_label = Label(frame, text="Username",bg='white', padx=20,pady=10,font=("Arial", 12, "bold"))
        self.username_label.grid(row=0, column=0, sticky='w')
        self.username_entry = Entry(frame,justify=CENTER,bd=2, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = Label(frame, text="Password",bg='white', padx=20, pady=10,font=("Arial", 12, "bold"))
        self.password_label.grid(row=1, column=0, sticky='w')
        self.password_entry = Entry(frame, show='*',justify=CENTER, bd=2, font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.register_button = Button(frame, text="Login",font=("Arial", 12, "bold"),command=self.login_func, bg="#4CAF50", fg="white", relief='flat')
        self.register_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.switch_button = Button(frame, text="Create Id",font=("Arial", 10, "bold"),command=show_register_window,bg="#2196F3", fg="white", relief='flat')
        self.switch_button.grid(row=3, column=0, columnspan=2, pady=10)

        frame.place(x=80, y=50)

    def login_func(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            if self.auth.login_user(username, password):
                tmsg.showinfo("Success", "Login successful!")
                # Proceed to the main app or dashboard
                self.proceed_to_dashboard()
            else:
                tmsg.showerror("Error", "Invalid username or password.")
        else:
            tmsg.showerror("Error", "Please enter both username and password.")
            

class ProblemTracker(Tk):
    def __init__(self, root, db):
        self.db = db
        self.root = root    
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        root.title("Coding Problem Tracker")
        root.geometry("1850x1077")
        root.state('zoomed')

        style = ttk.Style()
        style.configure("TNotebook", tabposition="n", background="#e4e6eb")
        style.configure("TNotebook.Tab", padding=[10, 5], relief="flat")

        self.my_notebook = ttk.Notebook(root)
        self.my_notebook.pack(expand=True, fill="both")
        self.frame = Frame(self.my_notebook,bd=2,bg='#F0F4F8', relief=SOLID, padx=20, pady=10)
        self.frame.pack(fill=BOTH, expand=True)
        self.my_notebook.add(self.frame, text="Challenge Corner")

        self.problem_name_label = Label(self.frame, text="Problem Name",padx=21,pady=10,bg="#F0F4F8",font=("Helvetica", 12, "bold"))
        self.problem_name_label.grid(row=0, column=0, sticky="w")
        self.problem_name_entry = Entry(self.frame, width=30, font=("Helvetica", 12))
        self.problem_name_entry.grid(row=0, column=1)

        self.search_label = Label(self.frame, text="Search Problem:",bg="#6C8EBF", fg="white", font=("Helvetica", 12, "bold"))
        self.search_label.grid(row=0, column=3, sticky="w", padx=10, pady=5)
        self.search_entry = Entry(self.frame, font=("Helvetica", 12))
        self.search_entry.grid(row=0, column=4)
        self.search_entry.bind("<KeyRelease>", self.search_problem)

        self.filter_label =Label(self.frame, text="Filter by:",font=("Helvetica", 12, "bold"))
        self.filter_label.grid(row=1, column=3,sticky="w")

        self.level_filter = ttk.Combobox(self.frame, values=["All", "Easy", "Medium", "Hard"],justify=CENTER,state="readonly",font=("Helvetica", 12))
        self.level_filter.grid(row=1, column=4, padx=5, pady=5)
        self.level_filter.bind("<<ComboboxSelected>>", self.filterProblems)

        self.status_filter = ttk.Combobox(self.frame, values=["All", "Solved", "Unsolved"],justify=CENTER,state="readonly",font=("Helvetica", 12))
        self.status_filter.grid(row=2, column=4, padx=5, pady=5)
        self.status_filter.bind("<<ComboboxSelected>>", self.filterProblems)
        
        self.level_label =Label(self.frame, text="Level",bg="#F0F4F8",font=("Helvetica", 12, "bold"),padx=21,pady=10)
        self.level_label.grid(row=2, column=0,sticky="w")
        self.level_combobox = ttk.Combobox(self.frame, values=["Easy", "Medium", "Hard"],width=28,justify=CENTER,state="readonly", font=("Helvetica", 12))
        self.level_combobox.grid(row=2, column=1)
        self.level_combobox.current(0)

        self.topic_label = Label(self.frame, text="Topic",bg="#F0F4F8",font=("Helvetica", 12, "bold"),padx=21,pady=10)
        self.topic_label.grid(row=3, column=0,sticky="w", pady=15)
        self.topic_entry = Entry(self.frame,width=30,justify=CENTER,font=("Helvetica", 12))
        self.topic_entry.grid(row=3, column=1, pady=15)

        self.status_label = Label(self.frame, text="Status",bg="#F0F4F8",font=("Helvetica", 12, "bold"),padx=21)
        self.status_label.grid(row=4, column=0,sticky="w", pady=12)
        self.status_combobox = ttk.Combobox(self.frame, values=["Unsolved", "Solved"],width=28,justify=CENTER,state="readonly",font=("Helvetica", 12))
        self.status_combobox.grid(row=4, column=1, pady=12)
        self.status_combobox.current(0)

        self.url_label = Label(self.frame, text="URL",bg="#F0F4F8",font=("Helvetica", 12, "bold"),padx=21)
        self.url_label.grid(row=5, column=0,sticky="w",pady=18)
        self.url_entry = Entry(self.frame,width=46,fg="#0066CC")
        self.url_entry.grid(row=5, column=1, pady=18)

        self.notes_label = Label(self.frame, text="Notes",padx=21,bg="#F5F5F5",font=("Helvetica", 12, "bold"))
        self.notes_label.grid(row=6, column=0,sticky="w",pady=18)
        self.notes_text = Text(self.frame, height=4, width=34,bg = "#E0F7FA")
        self.notes_text.grid(row=6, column=1,pady=18)

        self.add_problem_button = Button(self.frame, text="Add Problem",command=self.add_problem,bg="#FF4081", fg="white",font=("Helvetica", 12, "bold"))
        self.add_problem_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Treeview box
        self.problemTable = ttk.Treeview(self.frame, columns=("Name", "Level", "Topic", "Status","URL"), show="headings")
        self.problemTable.grid(row=8, column=0, columnspan=3, pady=10, sticky="nsew")
        self.problemTable.heading("Name", text="Problem Name", command=lambda: self.sortProblems())
        self.problemTable.column("Name", width=200, anchor="center")
        self.problemTable.heading("Level", text="Level")
        self.problemTable.heading("Topic", text="Topic")
        self.problemTable.heading("Status", text="Status")
        self.problemTable.heading("URL", text="URL")
        self.problemTable.bind('<Delete>',  self.delete_items)
        self.load_problems(self.problemTable)

        scrollbar =Scrollbar(self.frame, command=self.problemTable.yview)
        self.problemTable.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=8, column=3, sticky='ns')

        self.edit_button = Button(self.frame, text="Edit Problem", command=self.edit_problem,bg="#FF4081",fg="white",font=("Helvetica", 12, "bold"))
        self.edit_button.grid(row=9, column=0, columnspan=2,pady=10)

        # next tab i.e. tab2 ---> Notes section------------------------------------------------------------------
        
        self.tab2 = Frame(self.my_notebook,bd=2,bg='#F0F4F8', relief=SOLID, padx=20, pady=10)
        self.tab2.pack(fill=BOTH, expand=True)
        self.my_notebook.add(self.tab2, text="Notes Section")
        self.frame2 = Frame(self.tab2,background="#F0F4F8")
        self.frame2.pack(fill="x")

        Label(self.frame2, text="Search:", font=("Helvetica", 12, "bold")).grid(row=0, column=0)
        self.search_entryKey = Entry(self.frame2,width=30,font=("Helvetica", 12))
        self.search_entryKey.grid(row=0, column=1,padx=5,pady=10)

        self.search_button = Button(self.frame2, text="Search", command=self.search_tab2,bg="#FF4081",fg="white",font=("Helvetica", 12, "bold"))
        self.search_button.grid(row=0, column=2,padx=5,pady=10,sticky="w")


        self.notes_label_tab2 = Label(self.frame2, text="Notes",font=("Helvetica", 12, "bold"))
        self.notes_label_tab2.grid(row=1,column=0,padx=10, pady=5)
        self.notes_text_tab2 = Text(self.frame2, height=5, width=31)
        self.notes_text_tab2.grid(row=1,column=1)

        self.save_notes_button = Button(self.frame2, text="Save Notes",command=self.saveNotes,font=("Helvetica", 12, "bold"),bg="#FF4081",fg="white")
        self.save_notes_button.grid(row=3,column=2,pady=10)

        self.delete_notes_button =Button(self.frame2, text="Delete Notes",font=("Helvetica", 12, "bold"),bg="#FF4081",fg="white")
        self.delete_notes_button.grid(row=4,column=2)

        # Treeview box
        self.problemTable2 = ttk.Treeview(self.frame2, columns=("Name", "Level", "Topic", "Status","URL"), show="headings")
        self.problemTable2.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")
        self.problemTable2.heading("Name", text="Problem Name")
        self.problemTable2.column("Name", width=200, anchor="center")
        self.problemTable2.heading("Level", text="Level")
        self.problemTable2.heading("Topic", text="Topic")
        self.problemTable2.heading("Status", text="Status")
        self.problemTable2.heading("URL", text="URL")
        self.load_problems(self.problemTable2)

        scrollbar =Scrollbar(self.frame2, command=self.problemTable2.yview)
        self.problemTable2.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=5, column=3, sticky='ns')

        self.view_notes_button =Button(self.frame2, text="View Notes",command=self.viewNotes,font=("Helvetica", 12, "bold"),bg="#FF4081",fg="white")
        self.view_notes_button.grid(row=6,column=0)

    #tab3 --->Statistics-----------------------------------------------------------
        self.tab3 = Frame(self.my_notebook,bd=2,bg='#F0F4F8', relief=SOLID, padx=20, pady=10)
        self.tab3.pack(fill=BOTH, expand=True)
        self.my_notebook.add(self.tab3, text="Progress Tracking")
        self.frame3 = Frame(self.tab3,background="#F0F4F8")
        self.frame3.pack(fill="both", expand=True)

        self.refresh_stats_button = Button(self.tab3, text="Refresh Stats",command=self.display_statistics,font=("Helvetica", 12, "bold"),bg="#FF4081",fg="white")
        self.refresh_stats_button.pack(pady=5)

    #tab4 -->plotting------------------------------------------------------------------
        self.tab4 = Frame(self.my_notebook,bd=2,bg='#F0F4F8', relief=SOLID, padx=20, pady=10)
        self.tab4.pack(fill=BOTH, expand=True)
        self.my_notebook.add(self.tab4, text="Data Visualization")
        self.frame4 = Frame(self.tab4,background="#F0F4F8")
        self.frame4.pack(fill="both", expand=True)
        self.refresh_charts_button = Button(self.tab4, text="Refresh Charts", command=self.display_charts,font=("Helvetica", 12, "bold"),bg="#FF4081",fg="white")
        self.refresh_charts_button.pack()

    def display_charts(self):
        for widget in self.frame4.winfo_children():
            widget.destroy()

        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        self.plot_problems(axs[0])  # Chart1
        self.plot_difficulty(axs[1])   # Chart2
        self.plot_topic(axs[2])  # Chart3
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame4)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def plot_topic(self, ax):
        labels, sizes = self.db.plot_topic_db()
        ax.bar(labels, sizes)
        ax.set_title("Topics")
        ax.set_xlabel("Category")
        ax.set_ylabel("Problems Solved")

    def plot_difficulty(self, ax):
        labels, sizes = self.db.plot_difficulty_db()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title("Solved")

    def plot_problems(self,ax):
        dates, counts = self.db.plot_problems_db()
        ax.plot(dates, counts, marker='x')
        ax.set_title("Problems Solved Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Problems Solved")
        

    def display_statistics(self):
        dataDifficulty = self.db.get_data_by_difficulty()
        dataTopic = self.db.get_data_by_topic()
        daily_progress = self.db.get_solved_problems()
        weekly_progress = self.db.get_weekly_report()

        for widget in self.frame3.winfo_children():
            widget.destroy()
        
        Label(self.frame3, text=f"Problems Solved This Week: {weekly_progress}", font=('Helvetica', 14, 'bold'),bg='#F0F4F8').grid(row=0, pady=5)
        Label(self.frame3, text=f"Problems Solved Today: {daily_progress}", font=('Helvetica', 14, 'bold'),bg='#F0F4F8').grid(row=1,column=0,sticky='w', pady=10)

        #difficulty level
        Label(self.frame3, text="Statistics by Level", font=('Helvetica', 14, 'bold'),bg='#F0F4F8').grid(row=2, column=0, sticky='w')
        i=3
        for level, count in dataDifficulty:
            txt = f"{level}: {count} problems solved"
            Label(self.frame3, text=txt, font=('Helvetica', 12),bg='#F0F4F8').grid(row=i, column=0, sticky='w', padx=20)
            i+=1

        #category
        i+=1
        Label(self.frame3, text="Statistics by Topic", font=('Helvetica', 14, 'bold'),bg='#F0F4F8').grid(row=i, column=0, sticky='w')
        i+=1
        for Topic, count in dataTopic:
            txt = f"{Topic}: {count} problems solved"
            Label(self.frame3, text=txt, font=('Helvetica', 12),bg='#F0F4F8').grid(row=i, column=0, sticky='w', padx=20)
            i+=1

    def deleteNotes(self):
        i = self.problemTable2.focus()  # Get the selected item.
        if not i:
            return  
        selected_problem = self.problemTable2.item(i)['values']
        self.db.deleteNote(selected_problem)
        self.notes_text_tab2.delete("1.0", "end")


    def saveNotes(self):
        i = self.problemTable2.focus()  # Get the selected item.
        if not i:
            return  
        selected_problem = self.problemTable2.item(i)['values']
        data = self.notes_text_tab2.get("1.0", END).strip()
        self.db.updateNote(data,selected_problem)
        self.notes_text_tab2.delete("1.0", "end")


    def viewNotes(self):
        i = self.problemTable2.focus()  # Get the selected item.
        if not i:
            return  
        selected_problem = self.problemTable2.item(i)['values']
        text = self.db.get_Notes(selected_problem)
        self.notes_text_tab2.delete("1.0", "end")
        self.notes_text_tab2.insert(1.0, text)
        self.save_notes_button.config(text="Save Changes",bg="green",command=self.saveNotes,font=("Helvetica", 12, "bold"),fg="white")
        self.delete_notes_button.config(text="Delete Note",bg="red",command=self.deleteNotes,font=("Helvetica", 12, "bold"),fg="white")

        


    def search_tab2(self):
        text = self.search_entryKey.get().lower() 
        if(len(text)!=0):
            candidates = [problem for problem in self.db.get_all_problems() if text in problem[0].lower()]    #list of tuples
            self.update_problemTable(candidates,True) 
        else:
            self.load_problems(self.problemTable2)
            
        


    def search_problem(self, event):                
        text = self.search_entry.get().lower()            
        candidates = [problem for problem in self.db.get_all_problems() if text in problem[0].lower()]    #list of tuples
        self.update_problemTable(candidates)
                

    def update_problemTable(self,candidates,allTableview=False):
        
        if(allTableview==True):
            for i in self.problemTable2.get_children():
                self.problemTable2.delete(i)
            for problem in candidates:
                self.problemTable2.insert('', END, values=problem)
        else:
            for i in self.problemTable.get_children():
                self.problemTable.delete(i)

            for problem in candidates:
                self.problemTable.insert('', END, values=problem)

    def delete_items(self,_):
        l1=[]
        for i in self.problemTable.selection():
            l1.append(self.problemTable.item(i)['values'])

        self.db.deleteProblems(l1)
        self.load_problems(self.problemTable)
        self.load_problems(self.problemTable2)

    def edit_problem(self):
        self.problem_name_entry.delete(0, END)
        self.topic_entry.delete(0, END)
        self.url_entry.delete(0, END)
        self.notes_text.delete("1.0", "end")

        l2=[]
        for i in self.problemTable.selection():
            l2.append(self.problemTable.item(i)['values'])
        if(len(l2)!=0):
            self.problem_name_entry.insert(0, l2[0][0])  
            self.level_combobox.set(l2[0][1])
            self.topic_entry.insert(0, l2[0][2])
            self.status_combobox.set(l2[0][3])
            self.url_entry.insert(0,l2[0][4])
            updated_values=[self.problem_name_entry,self.level_combobox,self.topic_entry,self.status_combobox,self.url_entry]
            self.add_problem_button.config(text="Save Changes", command=lambda:self.update_problem(updated_values,l2),bg="green")

    def update_problem(self, updated_values,prevList):
        updated_name = updated_values[0].get()
        updated_level = updated_values[1].get()
        updated_topic = updated_values[2].get()
        updated_status = updated_values[3].get()
        updated_url = updated_values[4].get()

        # database method
        self.db.update_problem(updated_name, updated_level, updated_topic, updated_status, updated_url,prevList)
        updated_values[0].delete(0, END)
        updated_values[2].delete(0, END)
        updated_values[4].delete(0, END)
        self.load_problems(self.problemTable)
        self.load_problems(self.problemTable2)
        self.add_problem_button.config(text="Add Problem", command=self.add_problem, bg="#FF4081", fg="white",font=("Helvetica", 12, "bold"))

  
    def add_problem(self):
        name = self.problem_name_entry.get()
        difficulty = self.level_combobox.get()
        topic = self.topic_entry.get()
        status = self.status_combobox.get()
        url = self.url_entry.get()
        notes = self.notes_text.get("1.0", END).strip()

        if name and difficulty and topic and status and url:
            self.db.insert_problem(name, difficulty, topic, status, url, notes)
            self.problem_name_entry.delete(0, END)
            self.topic_entry.delete(0, END)
            self.url_entry.delete(0, END)
            self.notes_text.delete("1.0", "end")
            self.load_problems(self.problemTable)
            self.load_problems(self.problemTable2)
        else:
            tmsg.showerror("Error", "All fields must be filled out.")

    def load_problems(self,treeview):
        for i in treeview.get_children():
            treeview.delete(i)

        problems = self.db.get_all_problems()
        for i in problems:
            treeview.insert('', 0, values=i)

    def filterProblems(self, event):
        level = self.level_filter.get()
        status = self.status_filter.get()
        candidates = self.db.filter_problems(level, status)
        self.update_problemTable(candidates)

    def sortProblems(self):
        prev=[]
        for i in self.problemTable.get_children():
            prev.append(tuple(self.problemTable.item(i)['values']))
        sorted_problems = sorted(self.db.get_all_problems(), key=lambda x: x[0][0])

        if(prev==sorted_problems):
            sorted_problems=sorted(self.db.get_all_problems(), key=lambda x: x[0][0],reverse=True)
        self.update_problemTable(sorted_problems)

    def on_closing(self):
        plt.close('all')  # Close all Matplotlib figures
        self.root.destroy()  # Destroy the Tkinter window 
        self.root.quit()  # Quit the main loop 

            
