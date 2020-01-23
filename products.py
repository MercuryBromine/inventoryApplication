from tkinter import * #retives all of the gui elements  
from tkinter import messagebox as mb #not obtained from * so will need to rerieve it manually
import sqlite3, sys, string #imports extrnal modules
import csv_import, csv_export #imports internal modules
import InventoryApp as inventory
conn = sqlite3.connect("user_data.db") #makes connection to database
c = conn.cursor() #creates the cursor
price_click = True #Evalutes the state of the click
stock_click = True
min_click = True
max_click = True

def main(root,master,username): #main function, root is inherited from the window it was opened by.  master is the toplevel of that window and username is the user's username 
    window(root,master,username) #creates the window
    master.protocol("WM_DELETE_WINDOW", lambda: window.shutdown(master,username)) #overrides the X protocal
class window: #window class
    def __init__(self,root,master,username):
        bg_colour = "#55526B" #sets the background colour
        fg_colour = "#FDFDFD" #foreground colour
        btn_colour = "#868590" #button background colour
        entry_bg_colour = "#A8A6B2" #entry background colour
        self.username = username #making the varables avaliable anywhere in the class
        self.master = master
        self.root = root
        self.master.title(self.username + " Builder") #setting the title of the window
        self.master.resizable(False, False) #making the windwo unresizable
        self.master.config(bg=bg_colour) #setting the background colour of the window

        self.menubar = Menu(self.master) #creating the menu bar
        self.file_menu = Menu(self.menubar, tearoff=0) #making the menu
        self.file_menu.add_command(label="Import CSV", command=self.csv_import_app) #adding content to the menu
        self.file_menu.add_command(label="Export CSV", command=self.csv_export_app)
        self.menubar.add_cascade(label="File", menu=self.file_menu) #adding the contents under the file menu
        self.master.config(menu=self.menubar) #making thw window display the menu

        self.lbl_frame = Frame(self.master, bd=10, width=1350, height=600, bg=bg_colour) #creating a frame for the main body content
        self.lbl_frame.pack() #packing the frame, displaying it to the user
        self.btn_frame = Frame(self.master, bd=10, width=1000, height=600, bg=bg_colour) #creating a frame for the main button content
        self.btn_frame.pack()

        self.product = StringVar() #setting the variables for the entry field
        self.price = DoubleVar() #defining what data type the variable should take in
        self.stock = IntVar()
        self.min_value = IntVar()
        self.max_value = IntVar()

        # ==Product==#

        self.product_lbl = Label(self.lbl_frame, text="Product",
                                 font=("Open Sans", 20), bg=bg_colour, fg=fg_colour) #creating the label
        self.product_lbl.grid(row=0, column=0, padx=8, pady=20) #displaying the label on the window

        self.product_entry = Entry(self.lbl_frame, textvariable=self.product,
                                   font=("Open Sans", 20),bg=entry_bg_colour, fg=fg_colour) #creating the entry
        self.product_entry.grid(row=0, column=1, padx=8, pady=20) #displaying the entry onto the window

        # ==Price==#

        self.price_lbl = Label(self.lbl_frame, text="Price",
                               font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
        self.price_lbl.grid(row=1, column=0, padx=8, pady=20)

        self.price_entry = Entry(self.lbl_frame, textvariable=self.price,
                                 font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
        self.price_entry.bind('<FocusIn>', self.price_entry_click) # accessing a function when the field is clicked
        self.price_entry.grid(row=1, column=1, padx=8, pady=20)

        # ==Stock==#

        self.stock_lbl = Label(self.lbl_frame, text="Stock",
                               font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
        self.stock_lbl.grid(row=2, column=0, padx=8, pady=20)

        self.stock_entry = Entry(self.lbl_frame, textvariable=self.stock,
                                 font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
        self.stock_entry.bind('<FocusIn>', self.stock_entry_click)
        self.stock_entry.grid(row=2, column=1, padx=8, pady=20)

        # ==Min Value==#

        self.min_value_lbl = Label(self.lbl_frame, text="Minimum Stock Count",
                                   font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
        self.min_value_lbl.grid(row=3, column=0, padx=8, pady=20)

        self.min_value_entry = Entry(self.lbl_frame, textvariable=self.min_value,
                                     font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
        self.min_value_entry.bind('<FocusIn>', self.min_entry_click)
        self.min_value_entry.grid(row=3, column=1, padx=8, pady=20)

        # ==Max Value==#

        self.max_value_lbl = Label(self.lbl_frame, text="Maximum Stock Count",
                                   font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
        self.max_value_lbl.grid(row=4, column=0, padx=8, pady=20)

        self.max_value_entry = Entry(self.lbl_frame, textvariable=self.max_value,
                                     font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
        self.max_value_entry.bind('<FocusIn>', self.max_entry_click)
        self.max_value_entry.grid(row=4, column=1, padx=8, pady=20)

        # ==Buttons==#

        self.save_btn = Button(self.btn_frame, text="Save", width=17, font=("Open Sans", 20), command=self.saveInfo, bg=btn_colour, fg=fg_colour) #creating the button
        self.save_btn.grid(row=0, column=0, padx=8, pady=20) #displaying the button to the user

        self.reset_btn = Button(self.btn_frame, text="Reset", width=17, font=("Open Sans", 20), command=self.reset, bg=btn_colour, fg=fg_colour)
        self.reset_btn.grid(row=0, column=1, padx=8, pady=20)

        self.finish_btn = Button(self.btn_frame, text="Finish", width=17, font=("Open Sans", 20), command=self.finish, bg=btn_colour, fg=fg_colour)
        self.finish_btn.grid(row=0, column=2, padx=8, pady=20)

    def saveInfo(self): #save function
        table = self.username + "productdata" #the user's table
        c.execute("""CREATE TABLE IF NOT EXISTS {}(
                  product TEXT, price REAL, stock INTEGER, min_value INTEGER, max_value INTEGER)"""
                  .format(table)) #creating a table if it is not there 
        conn.commit() #saving the information
        try:
            query = "SELECT max(rowid) FROM {}".format(table) #selecting the last row.
            rows = c.execute(query) #execting the query
            row_id = rows.fetchone() #fetching one item from the query
            if int(row_id[0]) >= 150: #checking if the number of rows is greater than 150
                mb.showerror("Error", "Cannot add in more data") #showing qn error message
            else:
                try:
                    #retriving tbe values from the enrty fields
                    product = string.capwords(self.product.get()) #making the string capital letters at the start
                    price = self.price.get() 
                    stock = self.stock.get()
                    min_value = self.min_value.get()
                    max_value = self.max_value.get()
                    price = '%.2f' % price #setting the price to 2 decimal places

                    if (product) == "": #chekcing ig the product field is empty
                        mb.showerror("Error", "Fields cannot be blank") #displaying an error message
                    elif (product) == "*": #checking if the product contains the character 
                        mb.showerror("Error", "Character not allowed") #showing en erro messgae 
                    elif len(product) > 50: #cheking that the length of the prodcut is more than 50
                        mb.showerror("Error", "Product has max length of 50") #shwoing an error message
                    elif (price and stock and min_value and max_value) < 0: #cheking is the fields have a value less thnn 0
                        mb.showerror("Error", "Fields cannot be less than 0") #showing an eror message 
                    elif max_value < min_value: #chekcing the max value is less than the minimum value
                        mb.showerror("Error", "Max stock count cannot be less than min stock count")
                    elif stock > max_value: #chechking if the stock is more than the max value
                        mb.showerror("Error", "Stock cannot be more than max stock count")            
                    else:
                        productData = [] #creating an empty array
                        count = 0 #setting the count
                        c.execute("SELECT Product FROM {}".format(self.username + "productdata")) #selecting the product column from the table
                        data = c.fetchall() #fetching all of the data wihtin the column
                        for row in data: #accessing each row of the data
                            productData.append(row) #adding the data into an array
                        if len(productData) != 0: #checking if the product is not empty
                            while count < len(productData): #execing the loop unitl the count is more than or eqaual to he length of the array
                                if product == productData[count][0]: #chekcing if the product exists in the database
                                    mb.showerror("Error", "Product already exists") #shwoing an eror message
                                    break #braking the loop to prevent an infinate loop
                                elif product != productData[count][0]: # checking if the product is notin the array
                                    count += 1 #increasing the coubt by 1
                                if count >= len(productData): #chekcing the count is more than the length of the array
                                    c.execute("""INSERT INTO {}(
                                                              product, price, stock, min_value, max_value) VALUES(?,?,?,?,?)"""
                                              .format(table), (product, price, stock, min_value, max_value)) #insering the values into  the table
                                    conn.commit() #saving the changes
                                    mb.showinfo("Success", "Information Added") #showing a success message
                                    break #breaking out of the loop
                        else:
                            c.execute("""INSERT INTO {}(
                                      product, price, stock, min_value, max_value) VALUES(?,?,?,?,?)"""
                                      .format(table), (product, price, stock, min_value, max_value)) #inserting values into the table
                            conn.commit() #saving the changes
                            mb.showinfo("Success", "Information Added") #showing the success message
                except TclError: #catch if the data type is wrong for the field
                    mb.showerror("Error", "Wrong data type") #show an error message 
        except TypeError: #catch if there is a type error an execute the code above again
            try:
                product = string.capwords(self.product.get())
                price = self.price.get()
                stock = self.stock.get()
                min_value = self.min_value.get()
                max_value = self.max_value.get()
                price = '%.2f' % price

                if (product) == "":
                    mb.showerror("Error", "Fields cannot be blank")
                elif (product) == "*":
                    mb.showerror("Error", "Character not allowed")
                elif len(product) > 50:
                    mb.showerror("Error", "Product has max length of 50")
                elif (price and stock and min_value and max_value) < 0:
                    mb.showerror("Error", "Fields cannot be less than 0")
                elif max_value < min_value:
                    mb.showerror("Error", "Max stock count cannot be less than min stock count")
                elif stock > max_value:
                    mb.showerror("Error", "Stock cannot be more than max stock count")            
                else:
                    productData = []
                    count = 0
                    c.execute("SELECT Product FROM {}".format(self.username + "productdata"))
                    data = c.fetchall()
                    for row in data:
                        productData.append(row)
                    if len(productData) != 0:
                        while count < len(productData):
                            if product == productData[count][0]:
                                mb.showerror("Error", "Product already exists")
                                break
                            elif product != productData[count][0]:
                                count += 1
                            if count >= len(productData):
                                c.execute("""INSERT INTO {}(
                                                          product, price, stock, min_value, max_value) VALUES(?,?,?,?,?)"""
                                          .format(table), (product, price, stock, min_value, max_value))
                                conn.commit()
                                mb.showinfo("Success", "Information Added")
                                break
                    else:
                        c.execute("""INSERT INTO {}(
                                  product, price, stock, min_value, max_value) VALUES(?,?,?,?,?)"""
                                  .format(table), (product, price, stock, min_value, max_value))
                        conn.commit()
                        mb.showinfo("Success", "Information Added")
            except TclError:
                mb.showerror("Error", "Wrong data type")
            
    def price_entry_click(self, event): #price entry click function
        global price_click #making the valriable global
        if price_click: #chekcing if its True
            price_click = False #Making it false
            self.price_entry.delete(0, "end")  #deleting the contnets within the field

    def stock_entry_click(self, event): #stock entry click function
        global stock_click
        if stock_click:
            stock_click = False
            self.stock_entry.delete(0, "end")

    def min_entry_click(self, event): #min entry click functtion
        global min_click
        if min_click:
            min_click = False
            self.min_value_entry.delete(0, "end")

    def max_entry_click(self, event): #max entry click function
        global max_click
        if max_click:
            max_click = False
            self.max_value_entry.delete(0, "end")

    def reset(self): #reset fucntion
        global stock_click, price_click, min_click, max_click #aking the variables global
        stock_click = True #changing the states back into their origianl value
        price_click = True
        min_click = True
        max_click = True
        #setting the default values back to the original 
        self.product.set("")
        self.price.set(0.0)
        self.stock.set(0)
        self.min_value.set(0)
        self.max_value.set(0)
        self.product_entry.focus() #focusing on the product entry field

    def finish(self): #finish function
        c.execute("""SELECT COUNT(*) FROM sqlite_master
                  WHERE type='table' AND name='{}'""".format(self.username + "productdata")) #finding if the tbale exists in the database
        table_result = c.fetchone() #fetching one result
        if table_result[0] == 1: #chekcing if the table is there
            self.topLvl_win = Toplevel(self.master) #making a window
            self.new_win = inventory.main(self.master, self.topLvl_win, self.username) #intialsing the contents of the window
            self.master.withdraw() #withdrawing the current window.
        elif table_result[0] == 0: #checking if the table is nor there
            mb.showerror("Error", "Table does not exist") #showing an error messgae
        else:
            mb.showerror("Error", "Operation Failed") #showinf an error message
    def csv_import_app(self): # importing csv window function
        self.topLvl_win = Toplevel(self.master) #making the window
        self.new_win = csv_import.main(self.master, self.topLvl_win, self.username) #setting up the contents of the window
        self.master.withdraw() #withdrawing the current window
    def csv_export_app(self): #exprt csv function
        self.topLvl_win = Toplevel(self.master)
        self.new_win = csv_export.main(self.master, self.topLvl_win, self.username)
        self.master.withdraw()
    def shutdown(master,username): #shutdown function 
        c.execute("""SELECT COUNT(*) FROM sqlite_master
                  WHERE type='table' AND name='{}'""".format(username + "productdata")) #finding if the table exists wihtin the database
        table_result = c.fetchone() #fetching one result
        if table_result[0] == 1: #checking if the table exists 
            master.destroy() #destroying the window
            sys.exit(0) #closing the python interpreter
        elif table_result[0] == 0: #chekcing if the table is not there.
            mb.showerror("Error", "Table does not exist") #showing an eror message 
        else:
            mb.showerror("Error", "Operation Failed") #showing an error message
if __name__ == '__main__': #finding if a function is called main
    main(root,master,username) #accesing the function
    c.close() #closing the cursor
    conn.close() #cliosing the connection
