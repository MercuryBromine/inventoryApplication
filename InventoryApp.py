from tkinter import * #gets all of tnhe gui elements for tkinter
from tkinter import messagebox as mb #not included with *
from tkinter import filedialog #also not included with *, allows me to create a browse window
from tkinter import ttk #allows me to create a notebook
import sqlite3, os, sys, pandas #importing the external modules
import products, change_price, shopping_list, deleting_products, csv_import, csv_export ##importing my files

conn = sqlite3.connect("user_data.db") #connecting to the database
c = conn.cursor() #making a cursor

def main(root,master,username): #root is inherited from the the prevoius window, master is the toplevel and username is the user's username
    inventory_app(root,master,username) #inttalising the window
    master.protocol("WM_DELETE_WINDOW", lambda: inventory_app.shutdown(master)) # overiding the close button protocal

class inventory_app: #inventory app class
    def __init__(self,root,master, username):
        bg_colour = "#55526B" #background colour
        fg_colour = "#FDFDFD" #foreground colour
        btn_colour = "#868590" #button background colour
        entry_bg_colour = "#A8A6B2" #entry field background colour
        tab_bg_colour = "#888889" #notebook tab background colour (this is only in the inventory application)
        self.username = username #makes the username present thorughout the whole class
        self.master = master #makes the master avaliable wihtin the whole class
        self.root = root #maskes the root avaliable within the whole classs
        self.master.title(username + " Inventory") #titles the window
        self.master.config(bg=bg_colour) #sets the background colour of the window

        style = ttk.Style() #gives the ttk elements a sytle
        style.theme_use("clam") #using the clam theme
        style.configure("TNotebook", background=bg_colour, borderwidth=0) #setting the configerations of the notbook frame
        style.configure("TNotebook.Tab", background=tab_bg_colour, foreground="black", lightcolor=fg_colour, borderwidth=0) #setting the contents of the notbook tab frame
        style.configure("TFrame", background=bg_colour, foreground=fg_colour, borderwidth=0) # setting the contents of the ttk frame
        

        self.menubar = Menu(self.master) #creating a menubar
        self.file_menu = Menu(self.menubar, tearoff=0) #Allows the menubar to be right to the edge of the window
        self.file_menu.add_command(label="Information", command=self.information) #adding a label and assging it a command
        self.file_menu.add_command(label="Browse", command=self.browse)
        self.file_menu.add_command(label="Change Shopping List Details", command=self.change_shopping_list_details)
        self.file_menu.add_command(label="Delete Product", command=self.delete_products)
        self.file_menu.add_command(label="Import CSV", command=self.import_csv_app)
        self.file_menu.add_command(label="Export CSV", command=self.export_csv_app)
        self.file_menu.add_command(label="Close", command= lambda: self.root.destroy())
        self.menubar.add_cascade(label="File", menu=self.file_menu) #naming the file_menu
        self.master.config(menu=self.menubar) #configering the master to show the menu bar

        notebook = ttk.Notebook(self.master) #creating the noteboook template

        c.execute("SELECT * FROM {} ORDER BY product ASC".format(self.username + "productdata")) #selecting allo of the contents wihtin the table alphabetically
        #the array of the data would be [product, price, stock, min_value, max_value]
        data = c.fetchmany(150) #only fetching the first 150 items
        data_length = len(data) #checks how big the data is
        # frame_arr = [frame names], [notebook frames], [lbl_frames], [btn_frames], [stock_entry], [int_vars]
        self.frame_arr = [[], [], [], [], [], []]
        count = 0 #intlasing the count
        slow_count = 0 #intialising the slow counter, the slow counter will allow the program to know how many tabs have been created
        power_of_ten = 10 #how many items can fit onto on page
        page_counter = 1 #The page counter
        floor = data_length // 10 #Seeing how many perfect numbers go into the length of the data, 140 // 10 = 14 so there is 14 pages
        mod = data_length % 10 #seeing if there is any remainders, this would tell me if I would need to add an extra page on the end of the total pages. eg if remainder of 2 then then extra page so 14 becomes 15 pages and there are 2 items of the 15th page


        for element in data: #accessing every single element within the array. the c.fetchmany() provides an array. 
            if " " in element[0]: #checking if there is a space in the data
                string_var = element[0].replace(" ", "") #closes the space in the element
                self.frame_arr[4].append(string_var) #adds the element into the array, the position would be in the 4th array
            elif " " not in element[0]: #checks if there is no space
                self.frame_arr[4].append(element[0]) #adds the element to the array (4th array)

        for num in range(floor): #for every number in the perfet page numbers
            self.frame_arr[0].append("frame" + str(num)) #adding the number of page frames into the array (0th position)
            count += 1 #increases the count by 1
        if mod != 0: #if there is a remainder
            self.frame_arr[0].append("frame" + str(count)) #adds the last page frame into the array (0th posiiton)

        for element in self.frame_arr[0]: #accesses every element in the array (0th position)
            notebook_frame = ttk.Frame(notebook) #makes a notebook frame
            notebook.add(notebook_frame, text="Page " + str(page_counter)) #assgins a page number to the notebook frame
            self.frame_arr[1].append(notebook_frame) #adds the frame into the array in the first posisition of the array
            page_counter += 1 #increases the page counter by 1

        notebook.pack() #packs the notebook so the user would be able to see the contents within the frame

        for element_frame in self.frame_arr[1]: #accesses each element within the array (1st position)
            lbl_frame = Frame(element_frame, bd=10, bg=bg_colour) #makes a frame based of the notebook frame, this frame would contian the main body of the content
            btn_frame = Frame(element_frame, bd=10, bg=bg_colour) #makes a frame based of the notebook fram, this frame would contain the main buttons of the window
            lbl_frame.pack() #packs the frames to ollow the user to see the contents within the frame
            btn_frame.pack() 
            self.frame_arr[2].append(lbl_frame) #appends the frame into the 2nd position within the array
            self.frame_arr[3].append(btn_frame) #appends the frame into the 3rd position within the array


        count = 0

        counter = floor * 10 #sets how many items there are within the frame, I could use teh data_length but this allows the code to be more clear
        for element in data: #accessed each element within the array
            if count < counter: #checks if the count is less than the counter
                self.product = Label(self.frame_arr[2][slow_count], text=element[0], font=("Open Sans", 20), bg=bg_colour, fg=fg_colour) #adds in the label.
                self.product.grid(row=count, column=0, padx=8, pady=4) #displays the label into the window

                price = '%.2f' % element[1] # sets the price to 2 decimal places

                self.price = Label(self.frame_arr[2][slow_count], text="£" + str(price), font=("Open Sans", 20), bg=bg_colour, fg=fg_colour) 
                self.price.grid(row=count, column=1, padx=8, pady=4)

                self.int_var = self.frame_arr[4][count] #sets the stock entry from the values gained from the table
                self.int_var = IntVar() #makes the data type being collected to be integers only
                self.frame_arr[5].append(self.int_var) #adds the vars of the stock entry to the array (5th position)
                self.int_var.set(element[2]) #sets the field to contain what the stock is wihtin the table

                self.stock = Entry(self.frame_arr[2][slow_count], textvariable=self.int_var, font=("Open Sans", 20),
                                   justify="center", width=20, bg=entry_bg_colour, fg=fg_colour) #creates the entry field
                self.stock.grid(row=count, column=2, padx=8, pady=4) #displays the entry field

                self.plus_btn = Button(self.frame_arr[2][slow_count], text="+", font=("Open Sans", 15), bg=btn_colour, fg=fg_colour, width=10) #creates the button, the plus and the minus button woudl be on each row 
                self.plus_btn.configure(command=lambda stock_variable=self.int_var: self.incrementation(stock_variable)) #allows the stock to go up by one for the row that the button was pressed in. This would mean that it would not affect the rest of the entries
                self.plus_btn.grid(row=count, column=3, padx=8, pady=4) #displays the button

                self.minus_btn = Button(self.frame_arr[2][slow_count], text="-", font=("Open Sans", 15), bg=btn_colour, fg=fg_colour, width=10)
                self.minus_btn.configure(command=lambda stock_variable=self.int_var: self.decrementation(stock_variable))
                self.minus_btn.grid(row=count, column=4, padx=8, pady=4)

                # ==Buttons==#

                self.save_btn = Button(self.frame_arr[3][slow_count], text="Save", font=("Open Sans", 15), width=20,
                                       command=self.save, bg=btn_colour, fg=fg_colour) #creates the button
                self.save_btn.grid(row=0, column=0, padx=8) #displays the button

                self.new_product = Button(self.frame_arr[3][slow_count], text="New Product", font=("Open Sans", 15),
                                          width=20, command=self.new_product_window, bg=btn_colour, fg=fg_colour)
                self.new_product.grid(row=0, column=1, padx=8)

                self.change_price = Button(self.frame_arr[3][slow_count], text="Change Price", font=("Open Sans", 15),
                                           width=20, command=self.new_price, bg=btn_colour, fg=fg_colour)
                self.change_price.grid(row=0, column=2, padx=8)

                count += 1 #increases the count by 1 after a data is added.

            if count == power_of_ten: #checks if the frame has hit its 10th item 
                if slow_count < floor: #checks if the slow_count is less than the perfect dividoe
                    power_of_ten += 10 #increases by 10
                    slow_count += 1 #increase the slow count by 1
                if slow_count == floor: #checks if the slow count is equal to the perfect integer that goes into the length of the data
                    self.vars = [] #creates an empty array
                    for element in data: #checks for every element within data
                        self.vars.append(element) #adds the variables of the data into the array
                    del data[:count] #deletes the current data that has been used. This is to avoid confusion in the code
        if mod != 0: #checks if there is a remainder
            for element in data:
                self.product = Label(self.frame_arr[2][slow_count], text=element[0], font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
                self.product.grid(row=count, column=0, padx=8, pady=4)

                price = '%.2f' % element[1]

                self.price = Label(self.frame_arr[2][slow_count], text="£" + str(price), font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
                self.price.grid(row=count, column=1, padx=8, pady=4)

                self.int_var = self.frame_arr[4][count]
                self.int_var = IntVar()
                self.frame_arr[5].append(self.int_var)
                self.int_var.set(element[2])

                self.stock = Entry(self.frame_arr[2][slow_count], textvariable=self.int_var, font=("Open Sans", 20),
                                   justify="center", width=20, bg=entry_bg_colour, fg=fg_colour)
                self.stock.grid(row=count, column=2, padx=8, pady=4)

                self.plus_btn = Button(self.frame_arr[2][slow_count], text="+", font=("Open Sans", 15), bg=btn_colour, fg=fg_colour, width=10)
                self.plus_btn.configure(command=lambda stock_variable=self.int_var: self.incrementation(stock_variable))
                self.plus_btn.grid(row=count, column=3, padx=8, pady=4)

                self.minus_btn = Button(self.frame_arr[2][slow_count], text="-", font=("Open Sans", 15), bg=btn_colour, fg=fg_colour, width=10)
                self.minus_btn.configure(command=lambda stock_variable=self.int_var: self.decrementation(stock_variable))
                self.minus_btn.grid(row=count, column=4, padx=8, pady=4)

                # ==Buttons==#

                self.save_btn = Button(self.frame_arr[3][slow_count], text="Save", font=("Open Sans", 15), width=20,
                                       command=self.save, bg=btn_colour, fg=fg_colour)
                self.save_btn.grid(row=0, column=0, padx=8)

                self.new_product = Button(self.frame_arr[3][slow_count], text="New Product", font=("Open Sans", 15),
                                          width=20, command=self.new_product_window, bg=btn_colour, fg=fg_colour)
                self.new_product.grid(row=0, column=1, padx=8)

                self.change_price = Button(self.frame_arr[3][slow_count], text="Change Price", font=("Open Sans", 15),
                                           width=20, command=self.new_price, bg=btn_colour, fg=fg_colour)
                self.change_price.grid(row=0, column=2, padx=8)

                count += 1

    def save(self): #save function
        arr = [] #creating a blank array
        new_data = [] 
        self.file_path = []
        c.execute("SELECT product, price, stock, min_value, max_value FROM {} ORDER BY product ASC".format(self.username + "productdata")) #selectung everything from thr table
        data = c.fetchmany(150) #fetching the first 150 data items
        try:
            for element in self.frame_arr[5]: #accessing each elemenet within tht array
                element  = element.get() #retribing the actual data the user inputted into the system
                arr.append(element) #adding the data into an array
            with open("file-path.txt", "r") as r: #Opening a txt file
                for line in r: #looking at each line of the file
                    if line == "": #checking if there is something in the file
                        mb.showerror("Error", "Please select file path: File - Browse") #showing an error message if the if statement was evaluated to True
                    else: #If there is something there
                        self.file_path.append(line) #adds the file path into the array
            existing_file = os.path.isfile(self.file_path[0] + "/shopping-list.txt")  #checks if there is a file with the chosen file path
            count = 0
            while count < len(data): #checks if the count is within the length of the data
                new_stock = arr[count] #acceses each element within the array after the while loop is run again 
                if new_stock < 0: #checks if the new stock is less than 0
                    mb.showerror("Error", "Value cannot be less than 0") #shows an error message if it is
                    self.reset_values(data[count][0], data[count][2]) #resets the value that was inputted
                    count += 1 #increases the count by 1
                    continue #skips the value and restarts the while loop
                if new_stock > data[count][4]: #checks if the stock is greater than the maximum stock level
                    mb.showerror("Error", str(data[count][0] + " " + "Value cannot be greater than max stock count\nThe max stock count is" + " " +str(data[count][3]))) #showsing the user a message
                    self.reset_values(data[count][0], data[count][2]) #resets the value 
                    count += 1 #increases the count by 1
                    continue #skips over the value and restarts the while loop
                else: #checks if it passes the valiadation above                  
                    items = (data[count][0], data[count][1], new_stock, data[count][3], data[count][4]) #Makes the input of a row into a list so it can be appended as one set
                    new_data.append(items) #adds the item to the array
                    count += 1 #increases the count by 1
                df = pandas.DataFrame(new_data, columns=["product", "price", "stock", "min_value", "max_value"]) #creates a dataframe with the items within the array
                table = self.username + "productdata" #setting the table location
                df.to_sql(table, conn, if_exists='replace', index=False) #inserting the data into the array.
            mb.showinfo("Success", "Data saved") #shows the user a succcess message
            if existing_file: #checks if the file is there 
                os.remove(self.file_path[0] + "/shopping-list.txt") #removes the file
                self.gen_shopping_list() #access the function
            else: #checks if the file is not there
                self.gen_shopping_list() #accesses the shopping list function
        except TclError: #catch if there is a data type error
            mb.showerror("Error", "Wrong Data type") #show a message to the user
        except IndexError: #catch if there is  index error
            mb.showerror("Error", "Operation Failed") #show a message to this user
        except FileNotFoundError: #catch if there is a file not found error 
            mb.showerror("Error", "File path not set: File - Browse") #tell the user that they must select a file path
            self.browse() #execute the broswse function
    def gen_shopping_list(self): #shoppig list function
        arr = [] #empty array
        text_vars = []
        c.execute("SELECT product, stock, min_value, max_value FROM {} ORDER BY product ASC".format(self.username + "productdata")) #selects the required columns
        data = c.fetchmany(150) #finds up to the first 150
        for element in self.frame_arr[5]:
            element = element.get() 
            arr.append(element)
        count = 0
        try:
            with open(self.file_path[0] + "/shopping-list.txt") as f: #opens the shopping list file
                for line in f: #looks at each line of the shopping list
                    line = line.strip("\n") #removes all of the new lines 
                    line = line.split(" ") #creates the elements which are split at the " "/ e.g. "Apple Bear" --> "Apple", "Bear"
                    text_vars.append(line) #adds the line into the array
        except FileNotFoundError: #catches if there is not file found
            open(self.file_path[0] + "/shopping-list.txt", "a") #creates a new file
        while count < len(data):
            if arr[count] < data[count][2]: #checks if the stock is less than the stocks is less than the minimum
                if text_vars: #is the text_vars populated
                    if data[count][0] == text_vars[count][0]: #does the product already exist in the file
                        count += 1 #increases the count by 1
                        continue #skips the value and restarts the loop
                stock = data[count][3] - arr[count] #finds out how much stock is needed to get the max stock count
                with open(self.file_path[0] + "/shopping-list.txt", "a+") as f: #opens the file
                    f.write(data[count][0] + " " + str(stock) + "\n") #writes data into the file
                    f.close() #closes the file
                    mb.showwarning("Warning", "Products added to shopping list") #shows a warning message to the user telling them that a product was added to the database
            elif arr[count] >= data[count][2]: #checks if the stock is bigger than the minmum
                pass #passes the value and restarts the loop
            count += 1 #increases the count by 1
            
    def new_product_window(self): #product builder window setup
        self.save() #saving the information
        self.topLvl_win = Toplevel(self.master) #creating a window based on the current window opened
        self.new_win = products.main(self.master, self.topLvl_win, self.username) #initalising the contents wihtin the file
        self.master.withdraw() #removing the current window from the user
        

    def new_price(self): #new price winodow setup
        self.save()
        self.topLvl_win = Toplevel(self.master)
        self.new_win = change_price.main(self.master, self.topLvl_win, self.username)
        self.master.withdraw()

    def change_shopping_list_details(self): #change shopping list details window setup
        self.save()
        self.topLvl_win = Toplevel(self.master)
        self.new_win = shopping_list.main(self.master, self.topLvl_win, self.username)
        self.master.withdraw()

    def delete_products(self): #delete products windwo setup
        self.save()
        self.topLvl_win = Toplevel(self.master)
        self.new_win = deleting_products.main(self.master, self.topLvl_win, self.username)
        self.master.withdraw()

    def reset_values(self, product, stock): #reset value function
        count = 0 #setting the count
        while count < len(self.vars): #checking if the count is less than the length of the array
            if product == self.vars[count][0]: #finds the product within the array
                self.frame_arr[5][count].set(stock) #sets the stock back to its original passable value
                break #breaks the statement to prevent an infinate loop
            elif product != self.vars[count][0]: #checks if the product is not in the array
                count += 1 #increases the count by 1
    def import_csv_app(self): #import csv window setup
        self.topLvl_win = Toplevel(self.master)
        self.new_win = csv_import.main(self.master, self.topLvl_win, self.username)
        self.master.withdraw()

    def export_csv_app(self): #export csv window setup
        self.topLvl_win = Toplevel(self.master)
        self.new_win = csv_export.main(self.master, self.topLvl_win, self.username)
        self.master.withdraw()
    
    def incrementation(self, stock): #incrementation function
        inventory_count = stock.get() #retriving the count of the stock
        inventory_count += 1 #increasing the count by 1
        stock.set(inventory_count) #setting the field to show the new count

    def decrementation(self, stock): #decremenation function
        inventory_count = stock.get() #retriving the count of the stock
        inventory_count -= 1 #decreasing the count by 1
        stock.set(inventory_count) #setting the field to show the new stock count
        
    def information(self): #information function
        string = "Inputting a decimal value such as 3.5 can be saved, It will be stored as 4" #first part of message
        string2 = "If you was to input a value of -0.5, the value would be rounded to 0" #second part of message
        mb.showinfo("Information", string + "\n" + string2) #showing the user a pop up telling the some information
    
    def browse(self): #browse function
        user_current_dir = os.getcwd() #retrievs the current dictionary
        user_dir = filedialog.askdirectory(parent=self.master, initialdir=user_current_dir, title="Browse") #Creates the browse window
        if len(user_dir) > 0: #checks if there is a file path
            with open("file-path.txt", "w") as f: #creates a file
                f.write(user_dir) #adds the file path into the the file
                
    def shutdown(master): #shutdown function
        master.destroy() #destroys the current window
        sys.exit(0) #exits the python interpreter

if __name__ == "__main__": #checks if there is a function called main
    main(root,master,username) #runs the main. 

#### ACCESSSING THIS FILE ON ITS OWN WONT WORK AS THE USER MUST LOGIN, IT WOULD INHERIT THE ROOT FROM THAT WINDOW ####
