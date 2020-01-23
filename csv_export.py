#Imports needed to make the file work
from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog
import csv, os, sqlite3, sys
import InventoryApp as inventory
import csv_import, products
#connection to the database and create cursor
conn = sqlite3.connect("user_data.db")
c = conn.cursor()

def main(root,master,username): #root is inherited from the the previous window, master is the toplevel and username is the user's username
    window(root,master,username) #creates the window
    master.protocol("WM_DELETE_WINDOW", lambda: window.shutdown(master,username)) #overrides the X button
class window:
    def __init__(self,root,master,username):
        #Colours
        bg_colour = "#55526B"
        fg_colour = "#FDFDFD"
        btn_colour = "#868590"
        entry_bg_colour = "#6b6b6d"
        #Allows the variables to be accessed anywher within the frame
        self.root = root
        self.master = master
        self.username = username
        self.master.title("Export to CSV") #window title
        self.master.resizable(False,False) #does not allow the window to be resized
        self.master.config(bg=bg_colour) #sets the background colour of the window

        #Creates the frame and displays the frame to the user

        self.lbl_frame = Frame(self.master, bd=10, width=1350, height=600, bg=bg_colour)
        self.lbl_frame.pack()
        self.btn_frame = Frame(self.master, bd=10, width=1000, height=600, bg=bg_colour)
        self.btn_frame.pack()

        #data type variable
        self.file_path = StringVar()

        #==File Path==#
        self.file_path_lbl = Label(self.lbl_frame, text="File Path", font=("Open Sans", 20), bg=bg_colour, fg=fg_colour) #creates the label
        self.file_path_lbl.grid(row=0,column=0, padx=8, pady=20) #displays onto the the window

        self.file_path_entry = Entry(self.lbl_frame, textvariable=self.file_path, width=35, font=("Open Sans", 20), state=DISABLED, bg=entry_bg_colour, fg=fg_colour) #creates the entry
        self.file_path_entry.grid(row=0,column=1, padx=8, pady=20) #displays onto the window

        self.file_path_btn = Button(self.lbl_frame, text="Browse", width=10, font=("Open Sans", 20), command=self.browse, bg=btn_colour, fg=fg_colour) #Creates the button
        self.file_path_btn.grid(row=0,column=2, padx=8, pady=20) #displays the button onto the window

        #==Buttons==#
        self.export_btn = Button(self.btn_frame, text="Export", width=17, font=("Open Sans",20), command=self.export_csv, bg=btn_colour, fg=fg_colour)
        self.export_btn.grid(row=0,column=0, padx=8, pady=20)

        self.import_btn = Button(self.btn_frame, text="Import", width=17, font=("Open Sans",20),command=self.import_csv, bg=btn_colour, fg=fg_colour)
        self.import_btn.grid(row=0,column=1, padx=8, pady=20)

        self.new_product_window = Button(self.btn_frame, text="New Product", width=17, font=("Open Sans",20), command=self.new_product_window,bg=btn_colour, fg=fg_colour )
        self.new_product_window.grid(row=0,column=2, padx=8, pady=20)

        self.finish_btn = Button(self.btn_frame, text="Finish", width=17, font=("Open Sans",20), command=self.finish, bg=btn_colour, fg=fg_colour)
        self.finish_btn.grid(row=0,column=3, padx=8, pady=20)

    def browse(self):
        #This function would allow the user to choose a folder to add their csv file in
        user_current_dir = os.getcwd()
        user_dir = filedialog.askdirectory(parent=self.master, initialdir=user_current_dir, title="Browse")
        if len(user_dir) > 0:
            self.file_path.set(user_dir)
        else:
            mb.showerror("Error", "Operation Failed")
    def export_csv(self):
        #this function would get the data from the table and export the data into a csv file.
        file_path = self.file_path.get()
        existing_file = os.path.isfile(file_path + "/data.csv")
        if existing_file:
                os.remove(file_path + "/data.csv")
        c.execute("SELECT * FROM {} ORDER BY product ASC".format(self.username + "productdata"))
        data = c.fetchall()
        try:
            with open(file_path + "/data.csv", mode="a", newline="") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow(["Product", "Price", "Stock", "Minimum Stock Count", "Maximum Stock Count"])
                for line in data:
                    writer.writerow(line)
            mb.showinfo("Success", "Export Finished")
        except PermissionError: 
            mb.showerror("Error", "Permission not granted. Please select file path")
        except FileNotFoundError:
            mb.showerror("Error", "Cannot put file into another drive letter")

    def import_csv(self):
        #Takes the user to the import csv window
        self.topLvl_win = Toplevel(self.master)
        self.new_win = csv_import.main(self.master, self.topLvl_win, self.username)
        self.master.withdraw()
        
    def finish(self):
        #This function would check if there is a table for the user. If there is then it would check
        # If there are any contents within the window. If so then the user would be taken to
        # the relevent window. If there is no content or no table then the user would be taken to the other
        # window
        c.execute("""SELECT COUNT(*) FROM sqlite_master
                  WHERE type='table' AND name='{}'""".format(self.username + "productdata"))
        table_result = c.fetchone()
        if table_result[0] == 1:
            self.topLvl_win = Toplevel(self.master)
            self.new_win = inventory.main(self.master, self.topLvl_win, self.username)
            self.master.withdraw()
        elif table_result[0] == 0:
            mb.showerror("Error", "Table does not exist")
        else:
            mb.showerror("Error", "Operation Failed")
    def shutdown(master,username):
        #This function would check if there is a table for the user. If there is then it would check
        # If there are any contents within the window.
        # the user would be able to close the window otherwise they will not be able to close the window
        c.execute("""SELECT COUNT(*) FROM sqlite_master
                  WHERE type='table' AND name='{}'""".format(username + "productdata"))
        table_result = c.fetchone()
        if table_result[0] == 1:
            master.destroy()
            sys.exit(0)
        elif table_result[0] == 0:
            mb.showerror("Error", "Table does not exist")
        else:
            mb.showerror("Error", "Operation Failed")
    def new_product_window(self):
        #Takes the user to the product builder window
        self.topLvl_win = Toplevel(self.master)
        self.new_win = products.main(self.master, self.topLvl_win, self.username)
        self.master.withdraw()
if __name__ == "__main__":
    main(root,master,username)
