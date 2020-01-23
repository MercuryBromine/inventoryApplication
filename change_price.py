#The imports that are required for the file
from tkinter import *
from tkinter import messagebox as mb
import sqlite3, sys
import InventoryApp as inventory

price_click = True

def main(root,master,username): #root is inherited from the the prevoius window, master is the toplevel and username is the user's username
    window(root,master,username) #creates the window
    master.protocol("WM_DELETE_WINDOW", lambda: window.shutdown(master)) #overrides the X function

class window:
    def __init__(self,root,master, username):
        #Colours
        bg_colour = "#55526B"
        fg_colour = "#FDFDFD"
        btn_colour = "#868590"
        entry_bg_colour = "#A8A6B2"
        #Variables to be accessed anywhere in the class
        self.username = username
        self.master = master
        self.root = root
        self.master.title(self.username + " Builder") #window title
        self.master.resizable(False, False) #user will not be able to resize their window
        self.master.config(bg=bg_colour) #setting the background colour of the window

        #Creating the frames and displaying them to the user.

        self.lbl_frame = Frame(self.master, bd=10, width=1350, height=600, bg=bg_colour)
        self.lbl_frame.pack()
        self.btn_frame = Frame(self.master, bd=10, width=1000, height=600, bg=bg_colour)
        self.btn_frame.pack()

        #Data type variables, 

        self.product = StringVar()
        self.price = DoubleVar()

        # ==Product==#

        self.product_lbl = Label(self.lbl_frame, text="Product",
                                 font=("Open Sans", 20), bg=bg_colour, fg=fg_colour) #Creating the label
        self.product_lbl.grid(row=0, column=0, padx=8, pady=20) #showing the label onto the window

        self.product_entry = Entry(self.lbl_frame, textvariable=self.product,
                                   font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour) #creating the entry
        self.product_entry.grid(row=0, column=1, padx=8, pady=20) #showing the entry on the window

        # ==Price==#

        self.price_lbl = Label(self.lbl_frame, text="Price",
                               font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
        self.price_lbl.grid(row=1, column=0, padx=8, pady=20)

        self.price_entry = Entry(self.lbl_frame, textvariable=self.price,
                                 font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
        self.price_entry.bind('<FocusIn>', self.price_entry_click) #Links to function when clicked on 
        self.price_entry.grid(row=1, column=1, padx=8, pady=20)

        # ==Buttons==#

        self.save_btn = Button(self.btn_frame, text="Save", width=17, font=("Open Sans", 20), command=self.saveInfo, bg=btn_colour, fg=fg_colour) #Creating the button
        self.save_btn.grid(row=0, column=0, padx=8, pady=20) #shows the content into the window

        self.reset_btn = Button(self.btn_frame, text="Reset", width=17, font=("Open Sans", 20), command=self.reset, bg=btn_colour, fg=fg_colour)
        self.reset_btn.grid(row=0, column=1, padx=8, pady=20)

        self.finish_btn = Button(self.btn_frame, text="Finish", width=17, font=("Open Sans", 20), command=self.finish, bg=btn_colour, fg=fg_colour)
        self.finish_btn.grid(row=0, column=2, padx=8, pady=20)

    def saveInfo(self):
        #connecting to the database
        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()
        try:
            #retriving the input from the user
            product = self.product.get()
            new_price = self.price.get()
            #2 decimal places for the price
            new_price = '%.2f' % new_price
            productData = [] #blank array
            #Validation: Presecne, Character and if Price is less than 0
            if product == "":
                mb.showerror("Error", "Fields cannot be blank")
            elif product == "*":
                mb.showerror("Error", "Cannot use that character")
            elif float(new_price) < 0:
                mb.showerror("Error", "Price cannot be less than 0")
            else:
                count = 0 
                c.execute("SELECT product, price FROM {}".format(self.username + "productdata")) #selects relevent colums within the table
                data = c.fetchall() #shows all content of the column
                for row in data:
                    productData.append(row) #puts the column data into an array
                while count < len(productData):
                    #this function would look at if the product is in the array. Then it would select the old price based on the index of the
                    # product, it would then update the information into the and inert the data into a table
                    if product == productData[count][0]:
                        old_price = productData[count][1]
                        c.execute("""UPDATE {} SET price = ?
                                  WHERE price =? AND product = ?""".format(self.username + "productdata"),
                                  (new_price, old_price, product))
                        conn.commit()
                        mb.showinfo("Success", "Price Changed")
                        break
                    elif product != productData[count][0]: #if not in the array increase the count by 1 
                        count += 1
                if count >= len(productData): #If the product is not in the database show the user and error message
                    mb.showerror("Error", "Product not in database")
        except TclError: #checks if the data type is correct
            mb.showerror("Error", "Wrong data type")

    def price_entry_click(self, event):
        #This function would check if the user has clicked on the pricen field
        #If so the system would delete the existing data int the field
        global price_click
        if price_click:
            price_click = False
            self.price_entry.delete(0, "end")

    def reset(self):
        #This function would delete all of the contents within the entry fields and focuses on the product field
        global stock_click, price_click
        stock_click = True
        price_click = True
        self.product.set("")
        self.price.set(0.0)
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
        #This would shutdown the window and exit the python interperter.
        master.destroy()
        sys.exit(0)

if __name__ == '__main__': #Checks if a function is called main, if so then it would run the main function
    main(root,master,username)
