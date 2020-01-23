#Imports to make the system functional
from tkinter import *
from tkinter import messagebox as mb
import sqlite3, sys
import InventoryApp as inventory
#connection to database
conn = sqlite3.connect("user_data.db")
c = conn.cursor()
def main(root,master,username):#root is inherited from the the prevoius window, master is the toplevel and username is the user's username
    delete_products(root,master,username)#creates the window. 
    master.protocol("WM_DELETE_WINDOW", lambda: delete_products.shutdown(master)) #Overrides the X protocal

class delete_products:
    def __init__(self, root, master, username):
        # ==Window Configeration==#
        #SETS THE COLOURS
        bg_colour = "#55526B"
        fg_colour = "#FDFDFD"
        btn_colour = "#868590"
        entry_bg_colour = "#A8A6B2"
        #Allows the variables to be accessed anywhere wihthin the file
        self.username = username
        self.master = master
        self.root = root
        self.master.title(self.username + " Product Deleter") #window title
        self.master.resizable(False,False) #does not allow the window to be resized
        self.master.config(bg=bg_colour) #sets the background colour of the window

        # ==Frame Setup==#
        #Creates the frames and displays the frame into the window
        self.lbl_frame = Frame(self.master, bd=10, width=1350, height=600, bg=bg_colour) 
        self.lbl_frame.pack()
        self.btn_frame = Frame(self.master, bd=10, width=1000, height=600, bg=bg_colour)
        self.btn_frame.pack()

        # ==Entry Variables==#

        self.product = StringVar()

        #==Product==#

        self.product_lbl = Label(self.lbl_frame, text="Product",
                                 font=("Open Sans", 20), bg=bg_colour, fg=fg_colour) #Creates the label
        self.product_lbl.grid(row=0,column=0) #Displays label into the window

        self.product_entry = Entry(self.lbl_frame, textvariable=self.product,
                                   font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour) #Creates the entry
        self.product_entry.grid(row=0,column=1,  padx=8, pady=20) #displays the entry into the window

        #==Butttons==#

        self.delete_btn= Button(self.btn_frame, text="Delete", width=17, font=("Open Sans", 20), command=self.delete_product, bg=btn_colour, fg=fg_colour) #Creates the button
        self.delete_btn.grid(row=0, column=0, padx=8, pady=20) #Displays the button into the window

        self.reset_btn = Button(self.btn_frame, text="Reset", width=17, font=("Open Sans", 20), command=self.reset, bg=btn_colour, fg=fg_colour)
        self.reset_btn.grid(row=0, column=1, padx=8, pady=20)

        self.finish_btn = Button(self.btn_frame, text="Finish", width=17, font=("Open Sans", 20), command=self.finish, bg=btn_colour, fg=fg_colour)
        self.finish_btn.grid(row=0, column=2, padx=8, pady=20)

    def delete_product(self):
        #This function woudl retrive the user input and do a Presence check and a Character check
        # It would then select and retrive all of the products within the table and pack them into an
        #array. The system would find if the product is there if so it would delete the product. If not
        #Then it would show an error message
        product = self.product.get()
        if product == "":
            mb.showerror("Error", "Fields cannot be blank")
        elif product == "*":
            mb.showerror("Error", "Cannot use that character")
        else:
            count = 0
            c.execute("SELECT * FROM {}".format(self.username + "productdata"))
            data = c.fetchall()
            while count < len(data):
                if product == data[count][0]:
                    c.execute("DELETE FROM {} WHERE product=?".format(self.username + "productdata"), (product,))
                    conn.commit()
                    mb.showinfo("Success", "Product Deleted")
                    break
                elif product != data[count][0]:
                    count += 1
            if count >= len(data):
                mb.showerror("Error", "Product not in database")

    def reset(self):
        #THIS FUNCTION WOULD CLEAR ALL OF THE CONTENTS THAT IS WITHIN THE ENTRY FIELD
        self.product.set("")
        self.product_entry.focus()

    def finish(self):
        #This function would create a new window by toplevel and close the current window
        self.topLvl_win = Toplevel(self.master)
        self.new_win = inventory.main(self.master, self.topLvl_win, self.username)
        self.master.withdraw()
        
    def shutdown(master):
        #This would destroy the window and exit the python interpreter.
        master.destroy()
        sys.exit(0)
        
                
        
if __name__ == "__main__":
    main(root,master,username)
    
