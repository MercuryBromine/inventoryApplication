#This would import all of the modules that would be needed for this file
from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog
import csv, os, sqlite3, sys, pandas
import numpy as np
import InventoryApp as inventory
import csv_export, products
conn = sqlite3.connect("user_data.db") #connects to the database
c = conn.cursor() #creating a cursor.

def main(root,master,username): #main function
    window(root,master,username)
    master.protocol("WM_DELETE_WINDOW", lambda: window.shutdown(master,username)) #overiding the X protocal
class window:
    def __init__(self,root,master,username):
        #setting the colours of the window
        bg_colour = "#55526B"
        fg_colour = "#FDFDFD"
        btn_colour = "#868590"
        entry_bg_colour = "#6b6b6d"
        #allowing the variables to be accessed anywhere wihtin the class
        self.root = root 
        self.master = master
        self.username = username
        self.master.title("Import to CSV") #setting the title
        self.master.resizable(False,False) #making the window not resizeable
        self.master.config(bg=bg_colour) #setting the background colour.

        #Setting the frames and displaying the frame
        self.lbl_frame = Frame(self.master, bd=10, width=1350, height=600, bg=bg_colour)
        self.lbl_frame.pack()
        self.btn_frame = Frame(self.master, bd=10, width=1000, height=600, bg=bg_colour)
        self.btn_frame.pack()

        self.file_path = StringVar() #data type varible

        #==File Path==#
        self.file_path_lbl = Label(self.lbl_frame, text="File Path", font=("Open Sans", 20), bg=bg_colour, fg=fg_colour) #Creating the label
        self.file_path_lbl.grid(row=0,column=0, padx=8, pady=20) #Displaying the label

        self.file_path_entry = Entry(self.lbl_frame, textvariable=self.file_path, width=35, font=("Open Sans", 20), state=DISABLED, bg=entry_bg_colour, fg=fg_colour) #Showing the entry in a displaled state so the user cannot add data in there
        self.file_path_entry.grid(row=0,column=1, padx=8, pady=20) #displaying the entry

        self.file_path_btn = Button(self.lbl_frame, text="Browse", width=10, font=("Open Sans", 20), command=self.browse, bg=btn_colour, fg=fg_colour)
        self.file_path_btn.grid(row=0,column=2, padx=8, pady=20)

        #==Buttons==#
        self.import_btn = Button(self.btn_frame, text="Import", width=17, font=("Open Sans",20),command=self.import_csv, bg=btn_colour, fg=fg_colour) #Setting the button
        self.import_btn.grid(row=0,column=0, padx=8, pady=20) #displaying the button

        self.export_btn = Button(self.btn_frame, text="Export", width=17, font=("Open Sans",20), command=self.export_csv, bg=btn_colour, fg=fg_colour)
        self.export_btn.grid(row=0,column=1, padx=8, pady=20)

        self.new_product_window = Button(self.btn_frame, text="New Product", width=17, font=("Open Sans",20), command=self.new_product_window, bg=btn_colour, fg=fg_colour)
        self.new_product_window.grid(row=0,column=2, padx=8, pady=20)

        self.finish_btn = Button(self.btn_frame, text="Finish", width=17, font=("Open Sans",20), command=self.finish, bg=btn_colour, fg=fg_colour)
        self.finish_btn.grid(row=0,column=3, padx=8, pady=20)

    def browse(self): #browse function
        user_current_dir = os.getcwd() #finding the current dictionary
        user_dir = filedialog.askopenfilename(parent=self.master, initialdir=user_current_dir, title="Browse", filetypes = (("csv files","*.csv"),)) #creating the browse window
        if len(user_dir) > 0: #checking if there is a file path selected
            self.file_path.set(user_dir) #setting the file_path and showing it onto the window
        else:
            mb.showerror("Error", "Operation Failed") #showing an error message

    def import_csv(self): #import function
        table = self.username + "productdata" #setting the user table
        c.execute("""CREATE TABLE IF NOT EXISTS {}(product TEXT, price REAL, stock INTEGER, min_value INTEGER, max_value INTEGER)""".format(table)) #selecting the colums from the table
        conn.commit() #saving the information
        try:
            query = "SELECT max(rowid) FROM {}".format(table) #selecting the last row id of the table
            rows = c.execute(query) #executing the query
            row_id = rows.fetchone() #only getting one result 
            if int(row_id[0]) >= 150: #checking if its more than 150 items
                mb.showerror("Error", "Cannot add in more data") #showing an error message
            else:
                try:
                    file_path = self.file_path.get() #retriving the file path from 
                    mb.askokcancel("Warning", "Only 150 rows can be added.") #displaying a message to the user
                    df = pandas.read_csv(file_path, nrows=150) #reading the csv file
                    #validation check, presence, and data type
                    if df.isnull().values.any(): 
                        blank_count = df.isnull().values.sum()
                        mb.showerror("Error", str(blank_count) + " blanks in csv file")
                    elif df['product'].dtypes != np.object:
                        mb.showerror("Error", "Product field can only contain string")
                    elif df['price'].dtypes != np.float64:
                        mb.showerror("Error", "Price field can only contain floating point numbers")
                    elif df['stock'].dtypes != np.int64:
                        mb.showerror("Error", "stock field can only contain integers")
                    elif df['min_value'].dtypes != np.int64:
                        mb.showerror("Error", "minimum stock count field can only contain integers")
                    elif df['max_value'].dtypes != np.int64:
                        mb.showerror("Error", "maximum stock count field can only contain integers")
                    else:
                        df['product'] = df['product'].str.capitalize() #captalise the first letter of the product
                        c.execute("SELECT product FROM {}".format(table)) #executing the statement 
                        data = c.fetchall() #fetching all of the data
                        for element in data: #accessing each element within the array
                            for index, row in df.iterrows(): # Checking the the product is in the the csv file
                                mb.showerror("Error", "Product already exists") #displaying an error message
                                break #breaking the loop.
                            break 
                        #setting the variables so its easier to read.
                        product = df['product']
                        price = df['price']
                        stock = df['stock']
                        min_value = df['min_value']
                        max_value = df['max_value']
                        count = 0 #setting the count
                        while count < len(df):
                            if product[count] == "*": #charatcter check
                                mb.showerror("Error", "Character not allowed") #showing an error message
                                break
                            elif len(product[count]) > 50: #length check
                                mb.showerror("Error", "Product has max length of 50")
                                break
                            elif price[count]< 0: #checking if the variable is less than 0
                                mb.showerror("Error", "Fields cannot be less than 0")
                                break
                            elif stock[count] < 0: #checking if the variable is less than 0
                                mb.showerror("Error", "Fields cannot be less than 0")
                                break
                            elif max_value[count] < 0: #checking if the variable is less than 0
                                mb.showerror("Error", "Fields cannot be less than 0")
                                break
                            elif min_value[count] < 0: #checking if the variable is less than 0
                                mb.showerror("Error", "Fields cannot be less than 0")
                                break
                            elif max_value[count] < min_value[count]: #checking if the max value is less than the min value
                                mb.showerror("Error", "Max stock count cannot be less than min stock count")
                                break
                            elif stock[count] > max_value[count]: #checking if the stock is more than the max stock count
                                mb.showerror("Error", "Stock cannot be more than max stock count")
                                break
                            count += 1
                        if count >= len(df): #cheking if the count is more or  = to the length of the data
                            rows = df.shape[0] #finding the number of rows
                            count = 0 #setting the count
                            for element in df['product']: #accessing each element within the array
                                while count < rows: # is the count less than the rows
                                    repeat = df['product'].str.count(element).sum() #checking if the product is reapeated in the csv file
                                    if repeat > 1:
                                        mb.showerror("Error", "Product names must be unique and not repeated") #showing an error message
                                        break
                                    else:
                                        count += 1 #increasing the count by 1
                            if count >= rows:
                                df.to_sql(table, conn, if_exists='replace', index=False) #adding the data to the tbale in the database.
                except KeyError: #Check if the headings are correct
                    mb.showerror("Error", "Column headers need to be defined:\n" + "product, price, stock, min_value, max_value")
                except FileNotFoundError: #Seeing if there is a file selected.
                    mb.showerror("Error", "File not found")
        except TypeError: #Checking if there is nothing the the table
            try:
                file_path = self.file_path.get()
                mb.askokcancel("Warning", "Only 150 rows can be added.")
                df = pandas.read_csv(file_path, nrows=150)
                if df.isnull().values.any():
                    blank_count = df.isnull().values.sum()
                    mb.showerror("Error", str(blank_count) + " blanks in csv file")
                elif df['product'].dtypes != np.object:
                    mb.showerror("Error", "Product field can only contain string")
                elif df['price'].dtypes != np.float64:
                    mb.showerror("Error", "Price field can only contain floating point numbers")
                elif df['stock'].dtypes != np.int64:
                    mb.showerror("Error", "stock field can only contain integers")
                elif df['min_value'].dtypes != np.int64:
                    mb.showerror("Error", "minimum stock count field can only contain integers")
                elif df['max_value'].dtypes != np.int64:
                    mb.showerror("Error", "maximum stock count field can only contain integers")
                else:
                    df['product'] = df['product'].str.capitalize()
                    c.execute("SELECT product FROM {}".format(table))
                    data = c.fetchall()
                    for element in data:
                        for index, row in df.iterrows():
                            mb.showerror("Error", "Product already exists")
                            print("Product already exists")
                            break
                        break
                    product = df['product']
                    price = df['price']
                    stock = df['stock']
                    min_value = df['min_value']
                    max_value = df['max_value']
                    count = 0
                    while count < len(df):
                        if product[count] == "*":
                            mb.showerror("Error", "Character not allowed")
                            break
                        elif len(product[count]) > 50:
                            mb.showerror("Error", "Product has max length of 50")
                            break
                        elif price[count]< 0:
                            mb.showerror("Error", "Fields cannot be less than 0")
                            break
                        elif stock[count] < 0:
                            mb.showerror("Error", "Fields cannot be less than 0")
                            break
                        elif max_value[count] < 0:
                            mb.showerror("Error", "Fields cannot be less than 0")
                            break
                        elif min_value[count] < 0:
                            mb.showerror("Error", "Fields cannot be less than 0")
                            break
                        elif max_value[count] < min_value[count]:
                            mb.showerror("Error", "Max stock count cannot be less than min stock count")
                            break
                        elif stock[count] > max_value[count]:
                            mb.showerror("Error", "Stock cannot be more than max stock count")
                            break
                        count += 1
                    if count >= len(df):
                        rows = df.shape[0]
                        count = 0
                        for element in df['product']:
                            while count < rows:
                                repeat = df['product'].str.count(element).sum()
                                if repeat > 1:
                                    mb.showerror("Error", "Product names must be unique and not repeated")
                                    break
                                else:
                                    count += 1
                        if count >= rows:
                            df.to_sql(table, conn, if_exists='replace', index=False)
            except KeyError:
                mb.showerror("Error", "Column headers need to be defined:\n" + "product, price, stock, min_value, max_value")
            except FileNotFoundError:
                mb.showerror("Error", "File not found")
        
        
    def export_csv(self): 
        self.topLvl_win = Toplevel(self.master) #creating the window
        self.new_win = csv_export.main(self.master, self.topLvl_win, self.username) #intalising the contents within the window
        self.master.withdraw() #closing the window
    def finish(self):
        c.execute("""SELECT COUNT(*) FROM sqlite_master
                  WHERE type='table' AND name='{}'""".format(self.username + "productdata")) #finding if the user has a table
        table_result = c.fetchone() #fetches one result of the query
        if table_result[0] == 1: #checks if there is a table
            self.topLvl_win = Toplevel(self.master)
            self.new_win = inventory.main(self.master, self.topLvl_win, self.username)
            self.master.withdraw()
        elif table_result[0] == 0: #checks if there is not a table
            mb.showerror("Error", "Table does not exist")
        else:
            mb.showerror("Error", "Operation Failed")
    def shutdown(master,username):
        c.execute("""SELECT COUNT(*) FROM sqlite_master
                  WHERE type='table' AND name='{}'""".format(username + "productdata"))
        table_result = c.fetchone()
        if table_result[0] == 1:
            master.destroy() #destroying the window
            sys.exit(0) #closing the python interpreter
        elif table_result[0] == 0:
            mb.showerror("Error", "Table does not exist")
        else:
            mb.showerror("Error", "Operation Failed")
    def new_product_window(self):
        self.topLvl_win = Toplevel(self.master)
        self.new_win = products.main(self.master, self.topLvl_win, self.username)
        self.master.withdraw()

if __name__ == "__main__": #chekcing the the function is called main
    main(root,master,username) #accessing the main function
