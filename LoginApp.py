from tkinter import * #brings in all of the gui elements
from tkinter import messagebox as mb #this element is not added so I need to import it myself
import sqlite3 #allows me to use databases
import InventoryApp as inventory #importing my own file
import products 
from passlib.hash import bcrypt #importing a hashing algorithm to secure data

conn = sqlite3.connect("user_data.db")  # connection to database
c = conn.cursor()  # connection to SQL statements

def main(): #function
    win = Tk()  # initialising tkinter window
    new_window = login_window(win)  # creating a new login window
    win.mainloop()  # looping the event


class login_window:
    def __init__(self, master):  # self constructing as class is run.
        # ==Window Configuration==#
        bg_colour = "#55526B" #background colour
        fg_colour = "#FDFDFD" #foreground colour
        btn_colour = "#868590" #button background colour
        entry_bg_colour = "#A8A6B2" #entry button background colour
        self.master = master #making the master avaliable anywhere within the class
        self.master.title("Login") #window title
        self.master.resizable(False, False) #Making the window not resizeable
        self.master.config(bg=bg_colour) #setting the background colour of the window.

        self.lbl_frame = Frame(self.master, width=1350, height=600, bd=10 ,bg=bg_colour) #intialising the frame and seeting the parameters of the frame with its background colour
        self.lbl_frame.pack() #packing the frame so its contents can be seen in the window to the user.

        self.btn_frame = Frame(self.master, width=1000, height=600, bd=10, bg=bg_colour) 
        self.btn_frame.pack()

        # ==Text Variables==#
        #Setting the data type. This would retrive the data from the entry fields
        self.username = StringVar() 
        self.password = StringVar()

        # ==Username==#

        self.username_lbl = Label(self.lbl_frame, text="Username", font=("Open Sans", 20), bg=bg_colour, fg=fg_colour) #setting the label for the username
        self.username_lbl.grid(row=0, column=0, padx=8, pady=20) #displaying the label onto the screen

        self.username_entry = Entry(self.lbl_frame, textvariable=self.username, font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour) #creating the entry field
        self.username_entry.grid(row=0, column=1, padx=8, pady=20) #displaing the entry field onto the field. The padx, pady would determine its padding 

        # ==Password==#

        self.password_lbl = Label(self.lbl_frame, text="Password", font=("Open Sans", 20),bg=bg_colour,fg=fg_colour)
        self.password_lbl.grid(row=1, column=0, padx=8, pady=20)

        self.password_entry = Entry(self.lbl_frame, textvariable=self.password, font=("Open Sans", 20), show="*", bg=entry_bg_colour, fg=fg_colour)
        self.password_entry.grid(row=1, column=1, padx=8, pady=20)

        # ==Buttons==#

        self.login_btn = Button(self.btn_frame, text="Login", width=17, font=("Open Sans", 20), command=self.login, bg=btn_colour, fg=fg_colour) #setting up a button
        self.login_btn.grid(row=0, column=0, padx=8, pady=20) #displaying a button onto the window

        self.forgotPass_btn = Button(self.btn_frame, text="Forgot Password", width=17, font=("Open Sans", 20),
                                     command=self.forgot_pass, bg=btn_colour, fg=fg_colour)
        self.forgotPass_btn.grid(row=0, column=1, padx=8, pady=20)

        self.register_btn = Button(self.btn_frame, text="Register", width=17, font=("Open Sans", 20),
                                   command=self.register, bg=btn_colour, fg=fg_colour)
        self.register_btn.grid(row=0, column=2, padx=8, pady=20)
    def login(self): #login function
        username = self.username.get() #retriving the username input from the entry field. .get() allows me to see what the contents of the variable is
        password = self.password.get()
        user_data = [] #creating a blank array.
        if (username and password) == "": #checking if the username or password is blank. If so then it would display an error
            mb.showerror("ERROR", "Fields cannot be blank") #error pop up, Shown to the user.
        else:
            try: #allows the use of catching any errors 
                count = 0 #initalising the count
                c.execute("SELECT username, password FROM customerInformation") #selecting the username and password from the table
                data = c.fetchall() #fetching all of the usernames and passwords within the field
                for row in data: #for loop, finishes iterating when condition is met
                    user_data.append(row) #adding the data into an array
                while count < len(user_data): #checking if the count is less than the length of the user data. If so then it should loop
                    if username == user_data[count][0]: #checking if the username eneterd is the same as the element within the array
                        password_id = user_data[count][1] #setting the users password based on the index of the username
                        password_verify = bcrypt.verify(password, password_id) #using passlib to see if the password matches the password within the table
                        if password_verify: #If the output is True then it passwords do match
                            mb.showinfo("Success", "Login Complete") #show a pop up to the user telling them that they are signed in
                            self.switcher(username) #accessing a function
                            self.master.withdraw() #removing the login window from the users screen
                            break #breaking the loop so we don't get an infinate loop
                        else: #has anything else happend 
                            mb.showerror("Error", "Incorrect password") #show a pop up as the passwords do not match
                            break #break the loop to prevent an infinate loop
                    elif username != user_data[count][0]: #check if the username is not = to the element in the array
                        count += 1 #increase the count by 1
                if count >= len(user_data): #check if the count is greater or equal to the array
                    mb.showerror("Error,", "Username or Password does not exist") #show an error message as the username cannot be found
            except sqlite3.OperationalError: #If there is no table.
                mb.showerror("Error", "File Not Found Error") # show an error messsage saying that there is no file.

    def forgot_pass(self): #forgot pass window setup function
        self.topLvl_win = Toplevel(self.master) #allowing the window to be based on the current window. It would be placed ontop of the current window
        self.new_win = forgot_window(self.master, self.topLvl_win) #intalising the contents of the window
        self.master.withdraw() 

    def register(self): #register window setup function
        self.topLvl_win = Toplevel(self.master)
        self.new_win = register_window(self.master, self.topLvl_win)
        self.master.withdraw()

    def switcher(self, username): #swither to see which file the system should take the user
        c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{}'".format(username + "productdata")) #selects all of the tables within the database
        table_result = c.fetchone() #only selects one table that belongs to the user
        if table_result[0] == 1: #checks if the table is there
            query = "SELECT max(rowid) FROM {}".format(username + "productdata") #sees how many rows there are
            rows = c.execute(query) #executes the query
            row_id = rows.fetchone() #only fetches the max row id
            if row_id[0] != None: #if there is more than 0 rows
                self.topLvl_win = Toplevel(self.master) #create a window 
                self.new_win = inventory.main(self.master, self.topLvl_win, username) #setup the contents of the invenotry window.
            elif row_id[0] == None: #there is no rows
                self.topLvl_win = Toplevel(self.master) 
                self.new_win = products.main(self.master, self.topLvl_win, username) #sets up contents for the product builder window
        elif table_result[0] == 0: #checks if the table is not there
            self.topLvl_win = Toplevel(self.master)
            self.new_win = products.main(self.master, self.topLvl_win, username) #sets up the content for the product builder window
        else:
            mb.showerror("Error", "Operation Failed") #shows an error message if something went wrong.

class forgot_window: #forgot window class
    def __init__(self, root, master): #self allows me to access the data anywhere within the class, root is inherted from the login window and master is the current window
        ## WARNING: AS SOME OF THE CODE IS REPEATED I WILL NOT BE ADDING IN THE COMMENTS AGAIN PLEASE REFER TO THE LoginApp to see what the variables do
        bg_colour = "#55526B"
        fg_colour = "#FDFDFD"
        btn_colour = "#868590"
        entry_bg_colour = "#A8A6B2"
        self.master = master
        self.root = root #allows the root to be accessed from anywhere within the file
        self.master.title("Forgot Password")
        self.master.resizable(False, False)
        self.master.config(bg=bg_colour)
        master.protocol("WM_DELETE_WINDOW", lambda: forgot_window.shutdown(master)) #Closes the window and python

        self.lbl_frame = Frame(self.master, width=1350, height=600, bd=10, bg=bg_colour)
        self.lbl_frame.pack()

        self.btn_frame = Frame(self.master, width=1000, height=600, bd=10, bg=bg_colour)
        self.btn_frame.pack()

        self.new_pass = StringVar()
        self.conf_new_pass = StringVar()
        self.username = StringVar()
        self.passcode = StringVar()

        variable_arr = [self.new_pass, self.conf_new_pass, self.username, self.passcode] #packs the data type variables into an array
        string_arr = ["New Password", "Confirm New Password", "Username", "Passcode"] #creates an array for the labels to be used
        

        count = 0
        for element in string_arr: # accesses every element within the array
            lbl = Label(self.lbl_frame, text=element, font=("Open Sans", 20), bg=bg_colour, fg=fg_colour) 
            lbl.grid(row=count, column=0)

            if "Pass" in element: #checks if there is a Pass within the array element if so then the text as the user types would be ***** instead of 1234
                entry = Entry(self.lbl_frame, textvariable=variable_arr[count], show="*", font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
                entry.grid(row=count, column=1, padx=8, pady=20)
            else: #if there isn't pass in there then do this
                entry = Entry(self.lbl_frame, textvariable=variable_arr[count], font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
                entry.grid(row=count, column=1, padx=8, pady=20)

            count += 1 #increasing the count by 1
            
        change_btn = Button(self.btn_frame, text="Change Password", width=17, font=("Open Sans", 20),
                            command=self.forgot_pass, bg=btn_colour, fg=fg_colour)
        change_btn.grid(row=0, column=0, pady=20, padx=8)
        login_btn = Button(self.btn_frame, text="Login", width=17,font=("Open Sans", 20), command=self.login, bg=btn_colour, fg=fg_colour)
        login_btn.grid(row=0, column=1, pady=20, padx=8)
        register_btn = Button(self.btn_frame, text="Register", width=17, font=("Open Sans", 20), command=self.register, bg=btn_colour, fg=fg_colour)
        register_btn.grid(row=0, column=2, pady=20, padx=8)

    def forgot_pass(self): #forgot password function
        #retriving all user input from enteries
        new_pass = self.new_pass.get()
        conf_new_pass = self.conf_new_pass.get()
        username = self.username.get()
        passcode = self.passcode.get()

        new_pass = bcrypt.hash(new_pass) #hashing the password
        password_verify = bcrypt.verify(conf_new_pass, new_pass) #checking the the passwords match

        if (new_pass and conf_new_pass and username and passcode) == "": #checks if the fields are blank
            mb.showerror("Error", "Fields cannot be blank") #shows an erorr message if the fields are blank
        elif (new_pass and conf_new_pass and username and passcode) == "*": #checks if there is an * within the field
            mb.showerror("Error", "Charater not allowed") #shows the error message
        elif (len(new_pass) and len(conf_new_pass)) < 8 or (len(new_pass) and len(conf_new_pass)) > 21: #checks if the password is within the range of charaters specified.
            mb.showerror("Error", "Password has to be between 8 to 21 characters") #shows an error message if this is not the case
        elif not password_verify: #checks if the passwords do not match
            mb.showerror("Error", "Passwords do not match") #shows an error message telling the user that the password do not match
        else:
            try:
                user_data = []
                count = 0
                c.execute("SELECT username, password, passcode FROM customerInformation") #selects username password and passcode from the field
                data = c.fetchall()
                for row in data:
                    user_data.append(row)
                while count < len(user_data):
                    if username == user_data[count][0]:
                        passcode_id = user_data[count][2]
                        passcode_verify = bcrypt.verify(passcode, passcode_id) #checks if the passcode entered matches with the passcode in the table
                        if passcode_verify: #checks if the variable is true
                            old_pass = user_data[count][1] #sets the old password based on the index of the passcode and username
                            c.execute("UPDATE customerInformation SET password = ? WHERE password  = ?",
                                      (new_pass, old_pass)) # Changes the password where the username is specified
                            conn.commit() #saves the changes to the database
                            mb.showinfo("Success", "Password Changed") #tells the user that their function was successful
                            break #breaks the loop to prevent an infincate loop
                        else:
                            mb.showerror("Error", "Operation Failed") #shows an error message.
                            break

                    elif username != user_data[count][0]:
                        count += 1
                if count >= len(user_data):
                    mb.showerror("Error", "Incorrect Username or Passcode")
            except sqlite3.OperationalError:
                mb.showerror("Error", "File Not Found Error")

    def login(self): #login function setup window.
        self.topLvl_win = Toplevel(self.master) #creates the window ontop of the current window.
        self.new_win = login_window(self.topLvl_win) #setups the contents within the window
        self.master.forget(self.master) #removes the current screen from the user.

    def register(self): #register function setup window.
        self.topLvl_win = Toplevel(self.master)
        self.new_win = register_window(self.root, self.topLvl_win) #self.root is passed as this window is based on the login window.
        self.master.forget(self.master)
        
    def shutdown(master): #shutdown function
        master.destroy() #destroys the current window
        sys.exit(0) #exits the python interpreter


class register_window: #register window class
    def __init__(self, root, master):
        ## WARNING: AS SOME OF THE CODE IS REPEATED I WILL NOT BE ADDING IN THE COMMENTS AGAIN PLEASE REFER TO THE LoginApp to see what the variables do
        bg_colour = "#55526B"
        fg_colour = "#FDFDFD"
        btn_colour = "#868590"
        entry_bg_colour = "#A8A6B2"
        self.master = master
        self.root = root
        self.master.title("Register")
        self.master.resizable(False, False)
        self.master.config(bg=bg_colour)
        master.protocol("WM_DELETE_WINDOW", lambda: register_window.shutdown(master))

        self.lbl_frame = Frame(self.master, width=1350, height=600, bd=10, bg=bg_colour)
        self.lbl_frame.pack()

        self.btn_frame = Frame(self.master, width=1000, height=600, bd=10, bg=bg_colour)
        self.btn_frame.pack()

        self.forename = StringVar()
        self.surname = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.conf_pass = StringVar()
        self.passcode = StringVar()
        
        variable_arr = [self.forename, self.surname, self.username, self.password, self.conf_pass, self.passcode]
        string_arr = ["Surname", "Username", "Password", "Confirm Password", "Passcode"]

        self.forename_lbl = Label(self.lbl_frame, text="Forename", font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
        self.forename_lbl.grid(row=0, column=0)
        self.forename_entry = Entry(self.lbl_frame, textvariable=variable_arr[0], font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
        self.forename_entry.grid(row=0, column=1, padx=8, pady=20)

        count = 1
        for element in string_arr:
            lbl = Label(self.lbl_frame, text=element, font=("Open Sans", 20), bg=bg_colour, fg=fg_colour)
            lbl.grid(row=count, column=0)
            if "Pass" in element:
                entry = Entry(self.lbl_frame, textvariable=variable_arr[count], show="*",
                              font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
                entry.grid(row=count, column=1, padx=8, pady=20)
            else:
                entry = Entry(self.lbl_frame, textvariable=variable_arr[count],
                              font=("Open Sans", 20), bg=entry_bg_colour, fg=fg_colour)
                entry.grid(row=count, column=1, padx=8, pady=20)
            count += 1

        register_btn = Button(self.btn_frame, text="Register", command=self.register, font=("Open Sans", 20), bg=btn_colour, fg=fg_colour)
        register_btn.grid(row=0, column=0, pady=20, padx=8)

        reset_btn = Button(self.btn_frame, text="Reset", command=self.reset, font=("Open Sans", 20), bg=btn_colour, fg=fg_colour)
        reset_btn.grid(row=0, column=1, pady=20, padx=8)

        login_btn = Button(self.btn_frame, text="Login", command=self.login, font=("Open Sans", 20), bg=btn_colour, fg=fg_colour)
        login_btn.grid(row=0, column=2, pady=20, padx=8)

    def register(self):
        c.execute("""CREATE TABLE IF NOT EXISTS customerInformation(
                  forename TEXT,
                  surname TEXT,
                  username TEXT,
                  password TEXT,
                  passcode TEXT
                  )""") #creating the table within the database.
        conn.commit() #saving the changes

        forename = self.forename.get()
        surname = self.surname.get()
        username = self.username.get()
        password = self.password.get()
        conf_pass = self.conf_pass.get()
        passcode = self.passcode.get()

        if(forename and surname and username and password and conf_pass and passcode)== "":
            mb.showerror("Error", "Fields cannot be blank")
        elif not forename.isalpha() and not surname.isalpha(): #checks if the surname and forename only contain letters
            mb.showerror("Error", "Forename and surname can only contian letters")
        elif (forename and surname and username and password and conf_pass and passcode) == "*":
            mb.showerror("Error", " Character not allowed")
        elif len(username) < 4 or len(username) > 21: #checking if the username is wihthin the range of characters
            mb.showerror("Error", "Username length has to be between 4 to 21 characters") #shows an error message if the if statement is true
        elif not username.isalnum(): #checks if the username is not alphanumeric
             mb.showerror("Error", "Username needs to be alphanumeric") #shows an error message to the user
        elif (len(password) and len(conf_pass)) < 8 or (len(password) and len(conf_pass)) > 21: 
            mb.showerror("Error", "Password has to be between 8 to 21 characters")
        elif len(passcode) < 4: #checks if the length of the passcode is less than 4
            mb.showerror("Error", "Passcode has to be 4 characters or more")
        elif conf_pass != password:
            mb.showerror("Error", "Passwords don't match")
        else:
            username_data = []
            count = 0
            password  = bcrypt.hash(password) #hashes the password 
            passcode = bcrypt.hash(passcode) #hashes the passcode
            c.execute("SELECT username FROM customerInformation") #selects the username in the table
            data = c.fetchall() #fetches all of the usernames
            for row in data:
                username_data.append(row) #adds the usernames into a database.
            if len(username_data) != 0: #checks if the length of the data is not 
                while count < len(username_data): #creates a loop until the condtion is met
                    if username == username_data[count][0]: 
                        mb.showerror("Error", "Username already in use")
                        break #prevents an infiniate loop
                    elif username != username_data[count][0]:
                        count += 1
                    if count >= len(username_data):
                        c.execute("""INSERT INTO customerInformation(forename, surname, username, password, passcode)
                                  VALUES(?,?,?,?,?)""", (forename, surname, username, password, passcode)) #adds in the data into the table
                        conn.commit() #saves the information
                        mb.showinfo("Success", "Information Added") #shows a success message
                        break #breaks the loop.
            else:
                c.execute("""INSERT INTO customerInformation(forename, surname, username, password, passcode)
                          VALUES(?,?,?,?,?)""",(forename, surname, username, password, passcode)) 
                conn.commit()
                mb.showinfo("Success", "Information Added")

    def reset(self): #reset function
        #sets all of the field to blank
        self.forename.set("")
        self.surname.set("")
        self.username.set("")
        self.password.set("")
        self.conf_pass.set("")
        self.passcode.set("")
        self.forename_entry.focus() #focuses the input into the forename input.

    def login(self):
        self.topLvl_win = Toplevel(self.master)
        self.new_win = login_window(self.topLvl_win)
        self.master.forget(self.master)
        
    def shutdown(master): #shutdown function
        master.destroy() #destroys the current window
        sys.exit(0) #exits the python interpreter


if __name__ == '__main__': #checks if there is a module called main
    main() #executes the main function

c.close() #closes the cursor of the database
conn.close() #closes the connection to the database.
