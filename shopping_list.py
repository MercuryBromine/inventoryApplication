#Imports needed for the file
from tkinter import *
from tkinter import messagebox as mb
import sqlite3
import InventoryApp as inventory
conn = sqlite3.connect("user_data.db") #connecting to the database
c = conn.cursor() #creating the cursor
min_click = True #click variables
max_click = True

def main(root,master,username): #root is inherited from the the previous window, master is the toplevel and username is the user's username
    window(root,master,username) #starting up the window
    master.protocol("WM_DELETE_WINDOW", lambda: window.shutdown(master)) #overiding the X command 

class window:
    def __init__(self, root, master, username):
        #Colours
        bg_colour = "#55526B"
        fg_colour = "#FDFDFD"
        btn_colour = "#868590"
        entry_bg_colour = "#A8A6B2"
        #Allows variables to be used anywhere in the class
        self.master = master
        self.username = username
        self.master.title(self.username + " Shopping list") #window title
        self.master.resizable(False, False) #making the window not resizeable
        self.master.config(bg=bg_colour) #making the background colour of the window

        #Making the frames and displaying the frames to the user.
        self.lbl_frame = Frame(self.master, bd=10, width=1350, height=600, bg=bg_colour) 
        self.lbl_frame.pack()
        self.btn_frame = Frame(self.master, bd=10, width=1000, height=600, bg=bg_colour)
        self.btn_frame.pack()
        #Data type variables which allows me to get data from the user
        self.product  = StringVar()
        self.min_value = IntVar()
        self.max_value = IntVar()

        #==Product==#

        self.product_lbl = Label(self.lbl_frame, text="Product",
                                 font=("Open Sans", 20), bg=bg_colour, fg=fg_colour) #Creating the label
        self.product_lbl.grid(row=0, column=0, padx=8, pady=20) #Showing the label on the window

        self.product_entry = Entry(self.lbl_frame, textvariable=self.product,
                                   font=("Open Sans", 20),bg=entry_bg_colour, fg=fg_colour) #Creating the entry
        self.product_entry.grid(row=0, column=1, padx=8, pady=20) #showing the entry on the window

        #==Min Value==#

        self.min_value_lbl = Label(self.lbl_frame, text="Minimum Stock",
                                 font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
        self.min_value_lbl.grid(row=1, column=0, padx=8, pady=20)

        self.min_value_entry = Entry(self.lbl_frame, textvariable=self.min_value,
                                   font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
        self.min_value_entry.bind('<FocusIn>', self.min_entry_click) #Making the contents within the window be deleted when clicked.
        self.min_value_entry.grid(row=1, column=1, padx=8, pady=20)

        #==Max Value==#

        self.max_value_lbl = Label(self.lbl_frame, text="Maximum Stock",
                                 font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
        self.max_value_lbl.grid(row=2, column=0, padx=8, pady=20)

        self.max_value_entry = Entry(self.lbl_frame, textvariable=self.max_value,
                                   font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
        self.max_value_entry.bind('<FocusIn>', self.max_entry_click)
        self.max_value_entry.grid(row=2, column=1, padx=8, pady=20)

        #==Buttons==#

        self.save_btn = Button(self.btn_frame, text="Save", width=17, font=("Open Sans", 20), command=self.save_info, bg=btn_colour, fg=fg_colour) #creating the button
        self.save_btn.grid(row=0, column=0, padx=8, pady=20) #showing the button on the window

        self.reset_btn = Button(self.btn_frame, text="Reset", width=17, font=("Open Sans", 20), command=self.reset,bg=btn_colour, fg=fg_colour )
        self.reset_btn.grid(row=0, column=1, padx=8, pady=20)

        self.finish_btn = Button(self.btn_frame, text="Finish", width=17, font=("Open Sans", 20), command=self.finish, bg=btn_colour, fg=fg_colour)
        self.finish_btn.grid(row=0, column=2, padx=8, pady=20)

    def save_info(self):
        try:
            #Retriving the data input from the user
            product = self.product.get()
            min_value = self.min_value.get()
            max_value = self.max_value.get()

            #Validation check: Presence, Character, Max < Min and Min and Max < 0
            if product == "":
                mb.showerror("Error", "Field cannot be  blank")
            elif product == "*":
                mb.showerror("Error", "Character not allowed")
            elif (max_value and min_value) < 0:
                mb.showerror("Error", "Fields cannot be less than 0")
            elif  max_value < min_value:
                mb.showerror("Error", "Max Stock count cannot be less than min Stock count")
            else:
                count = 0 #setting the count
                c.execute("SELECT product, min_value, max_value FROM {}".format(self.username + "productdata")) #getting the data from the table
                data = c.fetchall() #getting all of the data within the columns and putting it into an array
                while count < len(data):
                    #This would find the old min and max based on the index of the product in the array.
                    if product == data[count][0]:
                        old_min_value = data[count][1]
                        old_max_value = data[count][2]
                        #It would then update the table and replace the old values with the new value
                        c.execute("""UPDATE {} SET min_value=? WHERE min_value=?
                                  AND product=?""".format(self.username + "productdata"),
                                  (min_value, old_min_value, product))
                        c.execute("""UPDATE {} SET max_value=? WHERE max_value=?
                                                      AND product=?""".format(self.username + "productdata"),
                                  (max_value, old_max_value, product))
                        conn.commit() #saving the data

                        mb.showinfo("Success", "Information updated") #showing  a success message.
                        break #breaking the loop
                    elif product != data[count][0]: #checks if the product is not in the database, if so then it would increase the count
                        count += 1
                if count >= len(data): #if it cant find the product then it would show an error message.
                    mb.showerror("Error", "Product not in database")
        except TclError: #checks if the data type is valid 
            mb.showerror("Error", "Wrong data type")

    def min_entry_click(self, event):
        #This function would delete the contents within the window
        global min_click
        if min_click:
            min_click = False
            self.min_value_entry.delete(0, "end")

    def max_entry_click(self, event):
        #This function would delete the contents within the window
        global max_click
        if max_click:
            max_click = False
            self.max_value_entry.delete(0, "end")

    def reset(self):
        #This function would delete the contents within the window
        global min_click, max_click
        min_click = True
        max_click = True
        self.product.set("")
        self.min_value.set(0)
        self.max_value.set(0)
        self.product_entry.focus()

    def finish(self):
        #This function would check if there is a table for the user. If there is then it would check
        # If there are any contents within the window. If so then the user would be taken to
        # the relevent window. If there is no content or no table then the user would be taken to the other
        # window
        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()
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

    def shutdown(master):
        #This function would close the window and close the python interprter
        master.destroy()
        sys.exit(0)

if __name__ == "__main__": #checks if there is a function called main and then it would run the main function
    main(root,master,username)
