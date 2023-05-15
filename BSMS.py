from tkinter import *
from tkinter import ttk, messagebox
from datetime import date
import pymysql
from sqlalchemy import create_engine
from pandas import read_sql
import csv
import openpyxl

# mysql connection.
# mycon = pymysql.connect(host="bbe5qh6iglbhu0xop53e-mysql.services.clever-cloud.com",
#                         user="uf1hsv3fsbddzaby",
#                         passwd="S9mCVNHsGszzZSfAPUhT",
#                         database="bbe5qh6iglbhu0xop53e")
# cur = mycon.cursor()

mycon = pymysql.connect(host="localhost",
                        user="root",
                        passwd="yazan2000",
                        database="BSMS")
cur = mycon.cursor()


#log out
def loggedOut():
    welcomePage()

# clears text in entry widget when clicked inside.
def clearEntry(event):
    event.widget.configure(state=NORMAL)
    event.widget.delete(0, END)

#welcome page choosing login as admin or customer
def welcomePage():
    # root definition and configuration.
    global root
    root.destroy()
    root = Tk()
    root.title("Bookstore Management System")
    root.geometry('960x540')
    root.configure(bg='#FFFFFF')
    root.iconbitmap(r"images\bms.ico")
    # window transparency.
    root.attributes("-alpha", 0.95)
    root.resizable(FALSE,FALSE)

    # frame definition and configuration.
    sty = ttk.Style()
    sty.configure("Bookstore.TFrame", bg="#FFFFFF", borderwidth=5, relief=FLAT)
    Label(text="    BOOKS STORE MANAGEMENT SYSTEM     ", font=("Times New Romans", 34), bg="blue",
          fg="#FFFFFF").grid(row=1, column=0,pady=80)

    Label(text = "Login As", font = ("Berlin Sans FB", 24), bg="#FFFFFF",
          fg="#2e2e2e").place(x=420,y=200)
    Button(text = "Admin", width = 20, bg="blue", fg="#FFFFFF", font = ("Berlin Sans FB", 14),
           bd=2, cursor="hand2", relief=GROOVE, command = Admin).place(x=365,y=300)
    Button(text = "Customer", width = 20, bg="blue", fg="#FFFFFF", font = ("Berlin Sans FB", 14),
           bd=2, cursor="hand2", relief=GROOVE, command = Customer).place(x=365,y=380)


    root.mainloop()

# if username and password exist in admin.
def adminLogin():
    mycursor = mycon.cursor()
    mycursor.execute(f"SELECT username FROM admin WHERE username = '{userVar.get()}' AND password = '{pswdVar.get()}'")
    users = mycursor.fetchall()
    if len(users) == 1:
        user = users[0][0]
        # mode = "memb"
        homeAdmin()
    elif len(users) == 0:
        messagebox.showerror("bookstore management system", "password or username incorrect !!!")

# if username and password exist in customers.
def customerLogin():
    global user
    mycursor = mycon.cursor()
    mycursor.execute(f"SELECT custid  FROM customers WHERE Fname = '{userV.get()}' AND Lname = '{pswdV.get()}' AND member = 'y'")
    users = mycursor.fetchall()
    if len(users) == 1:
        user = users[0][0]
        # mode = "memb"
        homeCustomer()
    elif len(users) == 0:
        messagebox.showerror("bookstore management system", "password or username incorrect !!!")

#admin login page
def Admin():
    global root
    global userVar
    global pswdVar
    global clicked

    root.destroy()
    root = Tk()
    root.title("Admin Login")
    root.geometry('960x540')
    root.configure(bg='#FFFFFF')
    root.iconbitmap(r"images\bms.ico")
    root.attributes("-alpha", 0.95)
    root.resizable(FALSE, FALSE)

    Label(text="    BOOKS STORE MANAGEMENT SYSTEM     ", font=("Times New Romans", 34), bg="blue",
          fg="#FFFFFF").grid(row=2, column=0,pady=80)

    # username entry widget.
    userVar = StringVar()
    Label(text="Username :", font=("Berlin Sans FB", 14), bg="#FFFFFF",
          fg="#2e2e2e").place(x=160,y=205)
    userEntry = Entry(width=40, font=("Berlin Sans FB", 14), textvariable=userVar, fg="#2e2e2e",
                      bg="#FFFFFF", borderwidth=1)
    userEntry.place(x=280, y=200, height=40)
    # remove default text when entry widget is clicked.
    clicked = userEntry.bind('<Button-1>', clearEntry)


    # password entry widget.
    pswdVar = StringVar()
    Label(text="Password :", font=("Berlin Sans FB", 14), bg="#FFFFFF",
          fg="#2e2e2e").place(x=160,y=285)
    pswdEntry = Entry(width=40, font=("Berlin Sans FB", 14), textvariable=pswdVar, fg="#2e2e2e",
                      bg="#FFFFFF", borderwidth=1, show="●")
    pswdEntry.place(x=280, y=280, height=40)
    # remove default text when entry widget is clicked.
    clicked = pswdEntry.bind('<Button-1>', clearEntry)

    #buttons
    Button(text="Login", pady=5, width=20, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14), bd=2,
           cursor="hand2", relief=GROOVE, command=adminLogin).place(x=365,y=370)
    root.bind("<Return>", adminLogin)
    Button(text="Go Back", pady=5, width=20, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14),
           cursor="hand2", relief=GROOVE, command=welcomePage).place(x=365,y=450)

    root.mainloop()

def homeAdmin():
    # holds search results.
    results = []

    def searchBox(evt):
        # removes results from previous search.
        for result in results:
            result.destroy()

        data = []
        columns = ('ID', 'Book Name', 'Author', 'Genre', 'Price', 'Copies')
        data.append(columns)

        # get current category and search box entry.
        searchCtg.selection_clear()
        if searchCtg.current() == 0:
            pass
        elif searchCtg.current() == 1:
            ctg = "name"
        elif searchCtg.current() == 2:
            ctg = "author"
        elif searchCtg.current() == 3:
            ctg = "genre"
        se = searchEntry.get()

        # retrieve data and display it.
        mycursor = mycon.cursor()
        mycursor.execute(
            f"SELECT bookid, name, author, genre, price, copies FROM books WHERE {ctg} LIKE '%{se}%' ORDER BY {ctg}")
        contain = mycursor.fetchall()
        data.extend(contain[0:8])

        rown = 8

        # no results found.
        if len(data) == 1:
            empty = Label(mainframe, text="   No Matching Records", bg="#FFFFFF", font=("Berlin Sans FB", 16))
            empty.grid(row=rown, column=0, columnspan=5, sticky=(W), padx=10, pady=5)
            results.append(empty)
            rown = rown + 1

        else:
            for record in data:
                # print records in columns.
                # string formatting of this type requires monospaced fonts to print properly.
                txt = "{: <5} {: <23} {: <23} {: <16} {: <8} {: <6}".format(*record)
                rec = Label(mainframe, text=txt, bg="#FFFFFF", font=("Courier", 12))
                rec.grid(row=rown, column=0, columnspan=5, sticky=(W), padx=10, pady=5)
                results.append(rec)
                rown = rown + 1

    # root definition and configuration.
    global root
    root.destroy()
    root = Tk()
    root.title("Admin Home")
    root.geometry('976x640')
    root.configure(bg='#FFFFFF')
    root.iconbitmap(r"images\bms.ico")
    root.attributes("-alpha", 0.95)
    root.resizable(FALSE, FALSE)

    # frame definition and configuration.
    sty = ttk.Style()
    sty.configure("Bookstore.TFrame", background="#FFFFFF", borderwidth=5, relief=FLAT)
    mainframe = ttk.Frame(root, style="Bookstore.TFrame")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # background image.
    Label(mainframe, text="    BOOKS STORE MANAGEMENT SYSTEM     ", font=("Times New Romans", 34), bg="blue",
          fg="#FFFFFF").grid(row=0, column=0, columnspan=5, rowspan=2)

    #Buttons
    Button(mainframe, text="Logout", width=14, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14),
           cursor="hand2", relief=GROOVE, command=welcomePage).grid(row=3, column=4, padx=10, pady=20)
    Button(mainframe, text="Borrowing", width=14, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14),
           cursor="hand2", relief=GROOVE, command=borrowing).grid(row=2, column=1,padx=10, pady=20)
    Button(mainframe, text="Sells", width=14, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14),
           cursor="hand2", relief=GROOVE, command=sells).grid(row=2, column=2,padx=10, pady=20)
    Button(mainframe, text="Books Details", width=14, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14),
           cursor="hand2", relief=GROOVE, command=bookDetails).grid(row=2, column=3,padx=10, pady=20)
    Button(mainframe, text="Members Details", width=14, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14),
           cursor="hand2", relief=GROOVE, command=editCustomer).grid(row=2, column=0, padx=10, pady=20)
    Button(mainframe, text="unloading", width=14, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14),
           cursor="hand2", relief=GROOVE, command=unloading).grid(row=2, column=4, sticky=W,padx=10, pady=20)

    # search category combobox. choose category to search in.
    global searchCtg
    searchVar = StringVar()
    searchCtg = ttk.Combobox(mainframe, textvariable=searchVar, font=("Berlin Sans FB", 16), width=9,
                             foreground="#2e2e2e", background="#FFFFFF")
    searchCtg['values'] = (' Search By', ' Book Name', ' Author', ' Genre')
    searchCtg.current(0)
    searchCtg.state(["readonly"])

    # searchCtg.bind('<<ComboboxSelected>>', searchBox)
    mainframe.option_add('*TCombobox*Listbox.font', ("Berlin Sans FB", 16))
    searchCtg.grid(row=3, column=0, ipadx=4, ipady=3, pady=14)

    # search entry box. enter what to search for.
    search = StringVar()
    searchEntry = Entry(mainframe, width=45, font=("Berlin Sans FB", 16), textvariable=search, fg="#2e2e2e",
                        bg="#FFFFFF", borderwidth=1)
    searchEntry.insert(0, " Enter Search Query")
    searchEntry.grid(row=3, column=1, columnspan=3, ipadx=5, ipady=5, padx=10, pady=14)

    root.bind("<Return>", searchBox)
    clicked = searchEntry.bind('<Button-1>', clearEntry)

    root.mainloop()

#customer login page
def Customer():
    global root
    global userV
    global pswdV

    # root definition and configuration.
    root.destroy()
    root = Tk()
    root.title("Customer Login")
    root.geometry('960x540')
    root.configure(bg='#FFFFFF')
    root.iconbitmap(r"images\bms.ico")
    root.attributes("-alpha", 0.95)
    root.resizable(FALSE, FALSE)

    Label(text="    BOOKS STORE MANAGEMENT SYSTEM     ", font=("Times New Romans", 34), bg="blue",
          fg="#FFFFFF").grid(row=2, column=0, pady=80)

    # username entry widget.
    userV = StringVar()
    Label(text="FirstName :", font=("Berlin Sans FB", 14), bg="#FFFFFF",
          fg="#2e2e2e").place(x=160, y=205)
    userVEntry = Entry(width=40, font=("Berlin Sans FB", 14), textvariable=userV, fg="#2e2e2e",
                      bg="#FFFFFF", borderwidth=1)
    userVEntry.place(x=280, y=200, height=40)
    # remove default text when entry widget is clicked.
    clicked = userVEntry.bind('<Button-1>', clearEntry)

    # password entry widget.
    pswdV = StringVar()
    Label(text="LastName :", font=("Berlin Sans FB", 14), bg="#FFFFFF",
          fg="#2e2e2e").place(x=160, y=285)
    pswdVEntry = Entry(width=40, font=("Berlin Sans FB", 14), textvariable=pswdV, fg="#2e2e2e",
                      bg="#FFFFFF", borderwidth=1, show="●")
    pswdVEntry.place(x=280, y=280, height=40)
    # remove default text when entry widget is clicked.
    clicked = pswdVEntry.bind('<Button-1>', clearEntry)

    # buttons
    Button(text="Login", pady=5, width=20, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14), bd=2,
           cursor="hand2", relief=GROOVE, command=customerLogin).place(x=365, y=370)
    root.bind("<Return>", customerLogin)
    Button(text="Go Back", pady=5, width=20, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14),
           cursor="hand2", relief=GROOVE, command=welcomePage).place(x=365, y=450)

    root.mainloop()

def homeCustomer():
    # holds search results.
    results = []

    def searchBox(evt):
        # removes results from previous search.
        for result in results:
            result.destroy()

        data = []
        columns = ('ID', 'Book Name', 'Author', 'Genre', 'Price', 'Copies')
        data.append(columns)

        # get current category and search box entry.
        searchCtg.selection_clear()
        if searchCtg.current() == 0:
            pass
        elif searchCtg.current() == 1:
            ctg = "name"
        elif searchCtg.current() == 2:
            ctg = "author"
        elif searchCtg.current() == 3:
            ctg = "genre"
        se = searchEntry.get()

        # retrieve data and display it.
        mycursor = mycon.cursor()
        mycursor.execute(
            f"SELECT bookid, name, author, genre, price, copies FROM books WHERE {ctg} LIKE '%{se}%' ORDER BY {ctg}")
        contain = mycursor.fetchall()
        data.extend(contain[0:8])

        rown = 10
        r = 150
        # no results found.
        if len(data) == 1:
            empty = Label(mainframe, text="   No Matching Records", bg="#FFFFFF", font=("Berlin Sans FB", 16))
            empty.grid(row=rown, column=0, columnspan=5, sticky=(W), padx=10, pady=5)
            results.append(empty)
            rown = rown + 1

        else:
            for record in data:
                # print records in columns.
                # string formatting of this type requires monospaced fonts to print properly.
                txt = "{: <5} {: <23} {: <23} {: <16} {: <8} {: <6}".format(*record)
                rec = Label(mainframe, text=txt, bg="#FFFFFF", font=("Courier", 12))
                rec.place(x=10,y=r)
                results.append(rec)
                r = r + 40

    # root definition and configuration.
    global root
    root.destroy()
    root = Tk()
    root.title("Customer home")
    root.geometry('976x640')
    root.configure(bg='#FFFFFF')
    root.iconbitmap(r"images\bms.ico")
    root.attributes("-alpha", 0.95)
    root.resizable(FALSE, FALSE)

    # frame definition and configuration.
    sty = ttk.Style()
    sty.configure("Bookstore.TFrame", background="#FFFFFF", borderwidth=5, relief=FLAT)
    mainframe = ttk.Frame(root, style="Bookstore.TFrame")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # background image.
    Label(mainframe, text="    BOOKS STORE MANAGEMENT SYSTEM     ", font=("Times New Romans", 34), bg="blue",
          fg="#FFFFFF").grid(row=0, column=0, columnspan=5, rowspan=2)
    Button(mainframe, text="Borrowing", width=14, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14),
           cursor="hand2", relief=GROOVE, command=borrowing).place(x=624,y=70)
    Button(mainframe, text="Logout", width=14, bg="blue", fg="#FFFFFF", font=("Berlin Sans FB", 14),
           cursor="hand2", relief=GROOVE, command=welcomePage).place(x=800,y=70)

    # search category combobox. choose category to search in.
    global searchCtg
    searchVar = StringVar()
    searchCtg = ttk.Combobox(mainframe, textvariable=searchVar, font=("Berlin Sans FB", 16), width=10,
                             foreground="#2e2e2e", background="#FFFFFF")
    searchCtg['values'] = (' Search By', ' Book Name', ' Author', ' Genre')
    searchCtg.current(0)
    searchCtg.state(["readonly"])

    mainframe.option_add('*TCombobox*Listbox.font', ("Berlin Sans FB", 16))
    searchCtg.place(x=10, y=70, height=38)

    # search entry box. enter what to search for.
    search = StringVar()
    searchEntry = Entry(mainframe, width=36, font=("Berlin Sans FB", 16), textvariable=search, fg="#2e2e2e",
                        bg="#FFFFFF", borderwidth=1)
    searchEntry.insert(0, " Enter Search Query")
    searchEntry.place(x=168, y=70, height=38)

    root.bind("<Return>", searchBox)
    clicked = searchEntry.bind('<Button-1>', clearEntry)

    root.mainloop()

def borrowing():
    def addbor():
        # add button clicked.
        # adding record to "borrowing" table.
        mycursor = mycon.cursor()
        mycursor.execute(f"INSERT INTO borrowing(custid, bookid, copies, date) VALUES ("
            f"{int(addCustIDE.get())},{int(addBookIDE.get())},{int(addCopiesE.get())},'{str(date.today())}')")
        mycon.commit()
        addCustIDE.delete(0, END)

        # clear all entries after adding
        addCustIDE.delete(0, END)
        addBookIDE.delete(0, END)
        addCopiesE.delete(0, END)

        # updates borrowing id.
        rid.destroy()
        mycursor = mycon.cursor()
        mycursor.execute("SELECT borrowerid FROM borrowing ORDER BY borrowerid DESC LIMIT 1")
        transid = mycursor.fetchone()
        transactionid = transid[0] + 1
        trid = Label(addResF, text=transactionid, bg="#FFFFFF", font=("Berlin Sans FB", 12))
        trid.grid(row=3, column=1, sticky=(W), padx=10, pady=10)

        return

    def modbor():
        # modify button clicked.
        # updating record in "borrowed" table.
        mycursor = mycon.cursor()
        mycursor.execute(
            f"UPDATE borrowing SET custid = {int(modCustIDE.get())}, bookid = {int(modBookIDE.get())}"
            f", copies = {int(modCopiesE.get())}, date = '{modDateE.get()}', returned = '"
            f"{modFulfilledE.get()}' WHERE resid = {int(modResIDE.get())}")
        mycon.commit()

        # clear all entries after modifying
        modResIDE.delete(0, END)
        modCustIDE.delete(0, END)
        modBookIDE.delete(0, END)
        modCopiesE.delete(0, END)
        modDateE.delete(0, END)
        modFulfilledE.delete(0, END)
        return

    def delbor():
        # remove button clicked.
        # deleting record from "reserved" table.
        mycursor = mycon.cursor()
        mycursor.execute(f"DELETE FROM borrowing WHERE borrowerid = {int(delResIDE.get())}")
        mycon.commit()

        # clear all entries after removing
        delResIDE.delete(0, END)
        return

    # root definition and configuration.
    global root
    root.destroy()
    root = Tk()
    root.title("Bookstore Management System")
    root.geometry('960x540')
    root.configure(bg='#FFFFFF')
    root.iconbitmap(r"images\bms.ico")
    root.attributes("-alpha", 0.95)
    root.resizable(FALSE, FALSE)

    # styles.
    sty1 = ttk.Style()
    sty1.configure("Bookstore.TFrame", background="#FFFFFF", borderwidth=5, relief=FLAT)
    sty2 = ttk.Style()
    sty2.configure("Bookstore.TNotebook", background="#FFFFFF", padding=10, tabmargins=2)
    sty3 = ttk.Style()
    sty3.configure("Bookstore.TNotebook.Tab", font=("Berlin Sans FB", 12), padding=5)

    # mainframe definition and configuration.
    mainframe = ttk.Frame(root, style="Bookstore.TFrame")
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    Label(mainframe, text="    BOOKS STORE MANAGEMENT SYSTEM     ", font=("Times New Romans", 34), bg="blue",
          fg="#FFFFFF").grid(row=0, column=0, columnspan=5, rowspan=2)


    # notebook and frames definition.
    reserveNBK = ttk.Notebook(mainframe, width=940, height=390, style="Bookstore.TNotebook")
    addResF = ttk.Frame(reserveNBK, style="Bookstore.TFrame")
    modResF = ttk.Frame(reserveNBK, style="Bookstore.TFrame")
    delResF = ttk.Frame(reserveNBK, style="Bookstore.TFrame")
    reserveNBK.add(addResF, text='New Borrowing', padding=40)
    reserveNBK.add(modResF, text='Modify Borrowing', padding=40)
    reserveNBK.add(delResF, text='Remove Borrowing', padding=40)
    reserveNBK.grid(row=2, column=0, columnspan=4, sticky=(W))

    # add reservation frame.
    # reservation id is auto-incremented.
    Label(addResF, text="Borrowing ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=3, column=0, sticky=(E),padx=10, pady=10)
    mycursor = mycon.cursor()
    mycursor.execute("SELECT borrowerid FROM borrowing ORDER BY borrowerid DESC LIMIT 1")
    resid = mycursor.fetchone()
    reservationid = resid[0] + 1
    rid = Label(addResF, text=reservationid, bg="#FFFFFF", font=("Berlin Sans FB", 12))
    rid.grid(row=3, column=1, sticky=(W), padx=10, pady=10)

    # labels and entry widgets for reservation details.
    addCustID = StringVar()
    Label(addResF, text="Customer ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=4, column=0, sticky=(E), padx=10, pady=10)
    addCustIDE = Entry(addResF, textvariable=addCustID, width=40, font=("Berlin Sans FB", 12), bd=2)
    addCustIDE.grid(row=4, column=1, padx=10, pady=10)

    addCustIDE = Entry(addResF, textvariable=addCustID, width=40, font=("Berlin Sans FB", 12), bd=2)
    addCustIDE.grid(row=4, column=1, padx=10, pady=10)

    addBookID = StringVar()
    Label(addResF, text="Book ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=5, column=0, sticky=(E),padx=10, pady=10)

    addBookIDE = Entry(addResF, textvariable=addBookID, width=40, font=("Berlin Sans FB", 12), bd=2)
    addBookIDE.grid(row=5, column=1, padx=10, pady=10)

    addCopies = StringVar()
    Label(addResF, text="Copies:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=6, column=0, sticky=(E), padx=10,
                                                                                   pady=10)
    addCopiesE = Entry(addResF, textvariable=addCopies, width=40, font=("Berlin Sans FB", 12), bd=2)
    addCopiesE.grid(row=6, column=1, padx=10, pady=10)
    # addDate = StringVar()
    Label(addResF, text="Date:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=7, column=0, sticky=(E), padx=10,
                                                                                 pady=10)
    Label(addResF, text=str(date.today()), bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=7,
                                                                  column=1, sticky=(W),padx=10, pady=10)

    # add button.
    Button(addResF, text="Add", command=addbor, bg="blue", fg="#FFFFFF", cursor="hand2", width=17,
           font=("Berlin Sans FB", 12)).grid(row=9, column=2, padx=20, pady=40)

    # go back button.
    Button(addResF, text="Go Back", width=10, pady=2, font=("Berlin Sans FB", 12), bg="blue", fg="#FFFFFF", cursor="hand2",
            command=homeAdmin).grid(row=9, column=3, sticky=(E), padx=5, pady=10)

    # modify reservation frame.
    # labels and entry widgets for reservation details.
    modResID = StringVar()
    Label(modResF, text="Borrowing ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=3, column=0, sticky=(E),
                                                                                           padx=10, pady=10)
    modResIDE = Entry(modResF, textvariable=modResID, width=40, font=("Berlin Sans FB", 12), bd=2)
    modResIDE.grid(row=3, column=1, padx=10, pady=10)

    modCustID = StringVar()
    Label(modResF, text="Customer ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=4, column=0, sticky=(E),
                                                                                        padx=10, pady=10)
    modCustIDE = Entry(modResF, textvariable=modCustID, width=40, font=("Berlin Sans FB", 12), bd=2)
    modCustIDE.grid(row=4, column=1, padx=10, pady=10)

    modBookID = StringVar()
    Label(modResF, text="Book ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=5, column=0, sticky=(E),
                                                                                     padx=10, pady=10)
    modBookIDE = Entry(modResF, textvariable=modBookID, width=40, font=("Berlin Sans FB", 12), bd=2)
    modBookIDE.grid(row=5, column=1, padx=10, pady=10)

    modCopies = StringVar()
    Label(modResF, text="Copies:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=6, column=0, sticky=(E), padx=10,
                                                                                   pady=10)
    modCopiesE = Entry(modResF, textvariable=modCopies, width=40, font=("Berlin Sans FB", 12), bd=2)
    modCopiesE.grid(row=6, column=1, padx=10, pady=10)

    modDate = StringVar()
    Label(modResF, text="Date:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=7, column=0, sticky=(E), padx=10,
                                                                                 pady=10)
    modDateE = Entry(modResF, textvariable=modDate, width=40, font=("Berlin Sans FB", 12), bd=2)
    modDateE.grid(row=7, column=1, padx=10, pady=10)

    modFulfilled = StringVar()
    Label(modResF, text="Returned(y/n):", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=8, column=0, sticky=(E),
                                                                                           padx=10, pady=10)
    modFulfilledE = Entry(modResF, textvariable=modFulfilled, width=40, font=("Berlin Sans FB", 12), bd=2)
    modFulfilledE.grid(row=8, column=1, padx=10, pady=10)
    # modify button.
    Button(modResF, text="Modify", bg="blue", fg="#FFFFFF", command=modbor, cursor="hand2", width=17,
           font=("Berlin Sans FB", 12)).grid(row=9, column=2, padx=20, pady=10)

    Button(modResF, text="Go Back", bg="blue", fg="#FFFFFF", command=homeAdmin, cursor="hand2", width=10,
           font=("Berlin Sans FB", 12)).grid(row=9, column=3, padx=20, pady=10)

    # delete transaction frame.
    delResID = StringVar()
    Label(delResF, text="Borrowing ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)
          ).grid(row=3, column=0, padx=10,pady=10)

    delResIDE = Entry(delResF, textvariable=delResID, width=40, font=("Berlin Sans FB", 12), bd=2)
    delResIDE.grid(row=3, column=1, padx=10, pady=10)
    # remove button.
    Button(delResF, text="Remove", bg="blue", fg="#FFFFFF", command=delbor, cursor="hand2", width=17,
           font=("Berlin Sans FB", 12)).grid(row=4,column=2,padx=20,pady=40)

    Button(delResF, text="Go Back",  bg="blue", fg="#FFFFFF", width=10, pady=2, font=("Berlin Sans FB", 12), cursor="hand2",
                       command=homeAdmin).grid(row=4, column=3, sticky=(E), padx=5, pady=10)

    root.mainloop()

def sells():
    def addTrans():
        # check if customer already exists in "customers" table.
        mycursor = mycon.cursor()
        mycursor.execute(f"SELECT custid FROM customers WHERE Fname = '{addCustFNameE.get()}' "
                         f"AND Lname = '{addCustLNameE.get()}' AND contact = '{addContactE.get()}'")
        custid = mycursor.fetchone()

        if custid == None:
            # if new customer, create record in "customers" table.
            mycursor.execute(f"INSERT INTO customers(Fname, Lname, contact) VALUES ('{addCustFNameE.get()}',"
                             f" '{addCustLNameE.get()}', '{addContactE.get()}')")
            mycon.commit()

        # retrieve customer id from "customers" table.
        mycursor.execute(f"SELECT custid FROM customers WHERE Fname = '{addCustFNameE.get()}'"
                         f" AND Lname = '{addCustLNameE.get()}' AND contact = '{addContactE.get()}'")
        custid = mycursor.fetchone()
        customerid = custid[0]
        # retrieve book price from "books" table.
        mycursor.execute(f"SELECT price FROM books WHERE bookid = {int(addBookIDE.get())}")
        price = mycursor.fetchone()
        pricebook = price[0]
        # retrieve member status from "customers" table.
        mycursor.execute(f"SELECT member FROM customers WHERE custid = {customerid}")
        memberstatus = mycursor.fetchone()
        memberstatusstr = memberstatus[0]

        # check if customer is a member. if member apply discount.
        if memberstatusstr == "y":
            discount = 0.2
        else:
            discount = 0

        totalnodiscount = float(pricebook) * int(addCopies.get())
        total = totalnodiscount - (discount) * (totalnodiscount)

        # displays bill details.
        messagebox.showinfo("Bookstore Manager",
                            f"Total Cost : {totalnodiscount}₽ \nDiscount : {discount * 100}% \nAmount : {total}₽")

        # create new sell in "sells" table.
        mycursor.execute(
            f"INSERT INTO sells(custid,bookid,copies,price,discount) VALUES ({customerid},"
            f" {int(addBookIDE.get())}, {int(addCopiesE.get())}, {totalnodiscount}, {total})")
        mycon.commit()

        # update copies available in "books" table.
        mycursor.execute(
            f"UPDATE books SET copies = copies - {int(addCopiesE.get())} WHERE bookid = {int(addBookIDE.get())}")
        mycon.commit()

        # clear all entries after adding
        addBookIDE.delete(0, END)
        addContactE.delete(0, END)
        addCopiesE.delete(0, END)
        addCustFNameE.delete(0, END)
        addCustLNameE.delete(0, END)
        #addNorUE.delete(0, END)

        # updates transaction id.
        sid.destroy()
        mycursor = mycon.cursor()
        mycursor.execute("SELECT sellid FROM sells ORDER BY sellid DESC LIMIT 1")
        sellid = mycursor.fetchone()
        sellsid = sellid[0] + 1
        seid = Label(addSellF, text=sellsid, bg="#FFFFFF", font=("Berlin Sans FB", 12))
        seid.grid(row=3, column=1, sticky=(W), padx=10, pady=10)
        return

    # root definition and configuration.
    global root
    root.destroy()
    root = Tk()
    root.title("Bookstore Management System")
    root.geometry('960x540')
    root.configure(bg='#FFFFFF')
    root.iconbitmap(r"images\bms.ico")
    root.attributes("-alpha", 0.95)
    #root.wm_protocol("WM_DELETE_WINDOW", goodBye)
    root.resizable(FALSE, FALSE)

    # styles.
    sty1 = ttk.Style()
    sty1.configure("Bookstore.TFrame", background="#FFFFFF", borderwidth=5, relief=FLAT)
    sty2 = ttk.Style()
    sty2.configure("Bookstore.TNotebook", background="#FFFFFF", padding=10, tabmargins=2)
    sty3 = ttk.Style()
    sty3.configure("Bookstore.TNotebook.Tab", font=("Berlin Sans FB", 12), padding=5)

    # maninframe definition and configuration.
    mainframe = ttk.Frame(root, style="Bookstore.TFrame")
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    Label(mainframe, text="    BOOKS STORE MANAGEMENT SYSTEM     ", font=("Times New Romans", 34), bg="blue",
          fg="#FFFFFF").grid(row=0, column=0, columnspan=5, rowspan=2)

    # notebook and frames definition.
    sellsNBK = ttk.Notebook(mainframe, width=940, height=390, style="Bookstore.TNotebook")
    addSellF = ttk.Frame(sellsNBK, style="Bookstore.TFrame")
    sellsNBK.add(addSellF, text='New Sell')
    sellsNBK.grid(row=2, column=0, columnspan=4, sticky=(W))

    # add transaction frame.
    # transaction id is auto incremented.
    Label(addSellF, text="Sell ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=3, column=0,
                                                                  sticky=(E), padx=10,pady=10)
    mycursor = mycon.cursor()
    mycursor.execute("SELECT sellid FROM sells ORDER BY sellid DESC LIMIT 1")
    sellid = mycursor.fetchone()
    selllid = sellid[0] + 1
    sid = Label(addSellF, text=selllid, bg="#FFFFFF", font=("Berlin Sans FB", 12))
    sid.grid(row=3, column=1, sticky=(W), padx=10, pady=10)

    # labels and entries for checkout details.
    addCustFName = StringVar()
    Label(addSellF, text="Customer First Name:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=5, column=0,
                                                                      sticky=(E), padx=10, pady=10)
    addCustFNameE = Entry(addSellF, textvariable=addCustFName, width=40, font=("Berlin Sans FB", 12), bd=2)
    addCustFNameE.grid(row=5, column=1, padx=10, pady=10)

    addCustLName = StringVar()
    Label(addSellF, text="Customer Last Name:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=6, column=0,
                                                                        sticky=(E), padx=10, pady=10)
    addCustLNameE = Entry(addSellF, textvariable=addCustLName, width=40, font=("Berlin Sans FB", 12), bd=2)
    addCustLNameE.grid(row=6, column=1, padx=10, pady=10)

    addContact = StringVar()
    Label(addSellF, text="Phone Number:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=7, column=0,
                                                                               sticky=(E), padx=10, pady=10)
    addContactE = Entry(addSellF, textvariable=addContact, width=40, font=("Berlin Sans FB", 12), bd=2)
    addContactE.grid(row=7, column=1, padx=10, pady=10)

    addBookID = StringVar()
    Label(addSellF, text="Book ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=8, column=0, sticky=(E),
                                                                                       padx=10, pady=10)
    addBookIDE = Entry(addSellF, textvariable=addBookID, width=40, font=("Berlin Sans FB", 12), bd=2)
    addBookIDE.grid(row=8, column=1, padx=10, pady=10)

    addCopies = StringVar()
    Label(addSellF, text="Copies:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=9, column=0, sticky=(E),
                                                                                     padx=10, pady=10)
    addCopiesE = Entry(addSellF, textvariable=addCopies, width=40, font=("Berlin Sans FB", 12), bd=2)
    addCopiesE.grid(row=9, column=1, padx=10, pady=10)

    # add and go back button.
    Button(addSellF, text="Add", command=addTrans, bg="blue", fg="#FFFFFF", cursor="hand2", width=17,
           font=("Berlin Sans FB", 12)).grid(row=11, column=2, padx=20, pady=30)
    Button(addSellF, text="Go Back", bg="blue", fg="#FFFFFF", width=10, pady=2, font=("Berlin Sans FB", 12),
           cursor="hand2", command=homeAdmin).grid(row=11, column=3, sticky=(E), padx=15, pady=10)

    root.mainloop()

def bookDetails():
    def addBook():
        # add button clicked.
        # create new record in "books" table.
        mycursor = mycon.cursor()
        mycursor.execute(
            f"INSERT INTO books(name,author,genre,yop,price,copies) VALUES ('{addBookNameE.get()}',"
            f"'{addBookAuthE.get()}','{addBookGenreE.get()}','{addBookYoPE.get()}',"
            f"{float(addBookPriceE.get())},{int(addBookNewE.get())})")
        mycon.commit()

        # clear all entries after adding
        addBookAuthE.delete(0, END)
        addBookGenreE.delete(0, END)
        addBookNameE.delete(0, END)
        addBookNewE.delete(0, END)
        addBookPriceE.delete(0, END)
        #addBookSecE.delete(0, END)
        addBookYoPE.delete(0, END)

        # updates book id.
        bkid.destroy()
        mycursor = mycon.cursor()
        mycursor.execute("SELECT bookid FROM books ORDER BY bookid DESC LIMIT 1")
        transid = mycursor.fetchone()
        transactionid = transid[0] + 1
        trid = Label(addBookF, text=transactionid, bg="#FFFFFF", font=("Berlin Sans FB", 12))
        trid.grid(row=3, column=1, sticky=(W), padx=10, pady=10)
        return

    def modBook():
        # modify button clicked.
        # update record in "books" table.
        mycursor = mycon.cursor()
        mycursor.execute(
            f"UPDATE books SET name = '{modBookNameE.get()}', author = '{modBookAuthE.get()}',"
            f" genre = '{modBookGenreE.get()}', yop = '{modBookYoPE.get()}',"
            f" price = {float(modBookPriceE.get())}, new = {int(modBookNewE.get())} "
            f" WHERE bookID = {int(modBookIDE.get())}")
            # f" used = {int(modBookSecE.get())} WHERE bookID = {int(modBookIDE.get())}")

        mycon.commit()

        # clear all entries after modifying
        modBookAuthE.delete(0, END)
        modBookGenreE.delete(0, END)
        modBookIDE.delete(0, END)
        modBookNameE.delete(0, END)
        modBookNewE.delete(0, END)
        modBookPriceE.delete(0, END)
        #modBookSecE.delete(0, END)
        modBookYoPE.delete(0, END)
        return

    # root definition and configuration.
    global root
    root.destroy()
    root = Tk()
    root.title("Bookstore Management System")
    root.geometry('960x540')
    root.configure(bg='#FFFFFF')
    root.iconbitmap(r"images\bms.ico")
    root.attributes("-alpha", 0.95)
    root.resizable(FALSE, FALSE)

    # styles.
    sty1 = ttk.Style()
    sty1.configure("Bookstore.TFrame", background="#FFFFFF", borderwidth=5, relief=FLAT)
    sty2 = ttk.Style()
    sty2.configure("Bookstore.TNotebook", background="#FFFFFF", padding=10)
    sty3 = ttk.Style()
    sty3.configure("Bookstore.TNotebook.Tab", font=("Berlin Sans FB", 12), padding=5)

    # mainframe definition and configuration.
    mainframe = ttk.Frame(root, style="Bookstore.TFrame")
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    Label(mainframe, text="    BOOKS STORE MANAGEMENT SYSTEM     ", font=("Times New Romans", 34), bg="blue",
          fg="#FFFFFF").grid(row=0, column=0, columnspan=5, rowspan=2)

    # notebook and frames defintion.
    BookNBK = ttk.Notebook(mainframe, width=940, height=390, style="Bookstore.TNotebook")
    addBookF = ttk.Frame(BookNBK, style="Bookstore.TFrame")
    modBookF = ttk.Frame(BookNBK, style="Bookstore.TFrame")
    BookNBK.add(addBookF, text='Add Book', padding=5)
    BookNBK.add(modBookF, text='Modify Book', padding=5)
    BookNBK.grid(row=2, column=0, columnspan=6, sticky=(W))

    # add book frame.
    # book id is auto incremented.
    Label(addBookF, text="Book ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=3, column=0, sticky=(E),
                                                                                     padx=10, pady=10)
    mycursor = mycon.cursor()
    mycursor.execute("SELECT bookid FROM books ORDER BY bookid DESC LIMIT 1")
    bookid = mycursor.fetchone()
    bid = bookid[0] + 1
    bkid = Label(addBookF, text=bid, bg="#FFFFFF", font=("Berlin Sans FB", 12))
    bkid.grid(row=3, column=1, sticky=(W), padx=10, pady=10)

    # labels and entry widgets for book details.
    addBookName = StringVar()
    Label(addBookF, text="Book Name:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=4, column=0, sticky=(E),
                                                                                       padx=10, pady=10)
    addBookNameE = Entry(addBookF, textvariable=addBookName, width=40, font=("Berlin Sans FB", 12), bd=2)
    addBookNameE.grid(row=4, column=1, padx=10, pady=10, columnspan=3)

    addBookAuth = StringVar()
    Label(addBookF, text="Author:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=5, column=0, sticky=(E),
                                                                                    padx=10, pady=10)
    addBookAuthE = Entry(addBookF, textvariable=addBookAuth, width=40, font=("Berlin Sans FB", 12), bd=2)
    addBookAuthE.grid(row=5, column=1, padx=10, pady=10, columnspan=3)

    addBookGenre = StringVar()
    Label(addBookF, text="Genre:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=6, column=0, sticky=(E), padx=10,
                                                                                   pady=10)
    addBookGenreE = Entry(addBookF, textvariable=addBookGenre, width=40, font=("Berlin Sans FB", 12), bd=2)
    addBookGenreE.grid(row=6, column=1, padx=10, pady=10, columnspan=3)

    addBookYoP = StringVar()
    Label(addBookF, text="Year of Publication:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=8, column=0,
                                                                           sticky=(E), padx=10, pady=10)
    addBookYoPE = Entry(addBookF, textvariable=addBookYoP, width=40, font=("Berlin Sans FB", 12), bd=2)
    addBookYoPE.grid(row=8, column=1, padx=10, pady=10, columnspan=3)

    addBookNew = StringVar()
    Label(addBookF, text="Copies:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=9, column=0, sticky=(E),
                                                                                        padx=10, pady=10)
    addBookNewE = Entry(addBookF, textvariable=addBookNew, width=10, font=("Berlin Sans FB", 12), bd=2)
    addBookNewE.grid(row=9, column=1, padx=10, pady=10)

    addBookPrice = StringVar()
    Label(addBookF, text="Book Price:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=10, column=0, sticky=(E),
                                                                                        padx=10, pady=10)
    addBookPriceE = Entry(addBookF, textvariable=addBookPrice, width=10, font=("Berlin Sans FB", 12), bd=2)
    addBookPriceE.grid(row=10, column=1, padx=10, pady=10)
    # add button and go back button.
    Button(addBookF, text="Add", command=addBook, bg="blue", fg="#FFFFFF", cursor="hand2", width=17, font=("Berlin Sans FB", 12)).grid(row=10,
                                                                                       column=5, padx=20, pady=10)
    Button(addBookF, text="Go Back", bg="blue", fg="#FFFFFF", width=10, pady=2, font=("Berlin Sans FB", 12), cursor="hand2",
           command=homeAdmin).grid(row=10, column=6, sticky=(E), padx=15, pady=10)

    # modify book frame.
    # labels and entry widgets for book details.
    modBookID = StringVar()
    Label(modBookF, text="Book ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=3, column=0, sticky=(E),
                                                                                     padx=10, pady=10)
    modBookIDE = Entry(modBookF, textvariable=modBookID, width=40, font=("Berlin Sans FB", 12), bd=2)
    modBookIDE.grid(row=3, column=1, padx=10, pady=10, columnspan=3)
    modBookName = StringVar()
    Label(modBookF, text="Book Name:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=4, column=0, sticky=(E),
                                                                                       padx=10, pady=10)
    modBookNameE = Entry(modBookF, textvariable=modBookName, width=40, font=("Berlin Sans FB", 12), bd=2)
    modBookNameE.grid(row=4, column=1, padx=10, pady=10, columnspan=3)
    modBookAuth = StringVar()
    Label(modBookF, text="Author:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=5, column=0, sticky=(E),
                                                                                    padx=10, pady=10)
    modBookAuthE = Entry(modBookF, textvariable=modBookAuth, width=40, font=("Berlin Sans FB", 12), bd=2)
    modBookAuthE.grid(row=5, column=1, padx=10, pady=10, columnspan=3)
    modBookGenre = StringVar()
    Label(modBookF, text="Genre:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=6, column=0, sticky=(E), padx=10,
                                                                                   pady=10)
    modBookGenreE = Entry(modBookF, textvariable=modBookGenre, width=40, font=("Berlin Sans FB", 12), bd=2)
    modBookGenreE.grid(row=6, column=1, padx=10, pady=10, columnspan=3)
    modBookYoP = StringVar()
    Label(modBookF, text="Year of Publication:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=8, column=0,
                                                                          sticky=(E), padx=10,pady=10)
    modBookYoPE = Entry(modBookF, textvariable=modBookYoP, width=40, font=("Berlin Sans FB", 12), bd=2)
    modBookYoPE.grid(row=8, column=1, padx=10, pady=10, columnspan=3)
    modBookNew = StringVar()
    Label(modBookF, text="Copies:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=9, column=0, sticky=(E),
                                                                                        padx=10, pady=10)
    modBookNewE = Entry(modBookF, textvariable=modBookNew, width=10, font=("Berlin Sans FB", 12), bd=2)
    modBookNewE.grid(row=9, column=1, padx=10, pady=10)

    modBookPrice = StringVar()
    Label(modBookF, text="Book Price:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=10, column=0, sticky=(E),
                                                                                        padx=10, pady=10)
    modBookPriceE = Entry(modBookF, textvariable=modBookPrice, width=10, font=("Berlin Sans FB", 12), bd=2)
    modBookPriceE.grid(row=10, column=1, padx=10, pady=10)
    # modify and go back button.
    Button(modBookF, text="Modify", bg="blue", fg="#FFFFFF", command=modBook, cursor="hand2", width=17, font=("Berlin Sans FB", 12)).grid(row=10,
                                                                        column=5, padx=20, pady=10)
    Button(modBookF, text="Go Back", bg="blue", fg="#FFFFFF", width=10, pady=2, font=("Berlin Sans FB", 12), cursor="hand2",
           command=homeAdmin).grid(row=10, column=6, sticky=(E), padx=15, pady=10)

    root.mainloop()

def editCustomer():
    def addCust():
        # add button clicked.
        # create new record in "books" table.
        mycursor = mycon.cursor()
        mycursor.execute(
            f"INSERT INTO customers(Fname,Lname,contact) VALUES ('{addFnameE.get()}','{addLnameE.get()}',"
            f"'{addContactE.get()}')")
        mycon.commit()

        # clear all entries after adding
        addFnameE.delete(0, END)
        addLnameE.delete(0, END)
        addContactE.delete(0, END)

        # updates Customer id.
        cid.destroy()
        mycursor = mycon.cursor()
        mycursor.execute("SELECT custid FROM customers ORDER BY custid DESC LIMIT 1")
        cuid = mycursor.fetchone()
        customerid = cuid[0] + 1
        cusid = Label(addCustF, text=customerid, bg="#FFFFFF", font=("Berlin Sans FB", 12))
        cusid.grid(row=3, column=1, sticky=(W), padx=10, pady=10)

        return

    def modCust():
        # modify button clicked.
        # update record in "books" table.
        mycursor = mycon.cursor()
        mycursor.execute(
            f"UPDATE customers SET Fname = '{modFnameE.get()}', Lname = '{modLnameE.get()}',"
            f" contact = '{modContactE.get()}', member = '{modMemberE.get()}'"
            f" WHERE custid = {int(modCustIDE.get())}")
        mycon.commit()

        # clear all entries after modifying
        modFnameE.delete(0, END)
        modLnameE.delete(0, END)
        modCustIDE.delete(0, END)
        modContactE.delete(0, END)
        modMemberE.delete(0, END)
        return

    # root definition and configuration.
    global root
    root.destroy()
    root = Tk()
    root.title("Bookstore Management System")
    root.geometry('960x540')
    root.configure(bg='#FFFFFF')
    root.iconbitmap(r"images\bms.ico")
    root.attributes("-alpha", 0.95)
    root.resizable(FALSE, FALSE)

    # styles.
    sty1 = ttk.Style()
    sty1.configure("Bookstore.TFrame", background="#FFFFFF", borderwidth=5, relief=FLAT)
    sty2 = ttk.Style()
    sty2.configure("Bookstore.TNotebook", background="#FFFFFF", padding=10, tabmargins=2)
    sty3 = ttk.Style()
    sty3.configure("Bookstore.TNotebook.Tab", font=("Berlin Sans FB", 12), padding=5)

    # mainframe definition and configuration.
    mainframe = ttk.Frame(root, style="Bookstore.TFrame")
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    Label(mainframe, text="    BOOKS STORE MANAGEMENT SYSTEM     ", font=("Times New Romans", 34), bg="blue",
          fg="#FFFFFF").grid(row=0, column=0, columnspan=5, rowspan=2)

    # notebook and frames definition.
    customerNBK = ttk.Notebook(mainframe, width=940, height=390, style="Bookstore.TNotebook")
    addCustF = ttk.Frame(customerNBK, style="Bookstore.TFrame")
    modCustF = ttk.Frame(customerNBK, style="Bookstore.TFrame")
    customerNBK.add(addCustF, text='Add Customer', padding=40)
    customerNBK.add(modCustF, text='Modify Customer', padding=40)
    customerNBK.grid(row=2, column=0, columnspan=4, sticky=(W))

    # add Customer frame.
    # Customer id is auto-incremented.
    Label(addCustF, text="Customer ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=3, column=0, sticky=(E),
                                                                                            padx=10, pady=10)
    mycursor = mycon.cursor()
    mycursor.execute("SELECT custid FROM customers ORDER BY custid DESC LIMIT 1")
    ccid = mycursor.fetchone()
    ccustomerid = ccid[0] + 1
    cid = Label(addCustF, text=ccustomerid, bg="#FFFFFF", font=("Berlin Sans FB", 12))
    cid.grid(row=3, column=1, sticky=(W), padx=10, pady=10)

    # labels and entry widgets for Customer details.
    addFname = StringVar()
    Label(addCustF, text="First Name:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=4, column=0, sticky=(E),
                                                                                         padx=10, pady=10)
    addFnameE = Entry(addCustF, textvariable=addFname, width=40, font=("Berlin Sans FB", 12), bd=2)
    addFnameE.grid(row=4, column=1, padx=10, pady=10)

    addLname = StringVar()
    Label(addCustF, text="Last Name:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(
        row=5, column=0, sticky=(E), padx=10, pady=10)

    addLnameE = Entry(addCustF, textvariable=addLname, width=40, font=("Berlin Sans FB", 12), bd=2)
    addLnameE.grid(row=5, column=1, padx=10, pady=10)

    addContact = StringVar()
    Label(addCustF, text="Contact:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=6, column=0, sticky=(E),
                                                              padx=10, pady=10)
    addContactE = Entry(addCustF, textvariable=addContact, width=40, font=("Berlin Sans FB", 12), bd=2)
    addContactE.grid(row=6, column=1, padx=10, pady=10)

    # add button.
    Button(addCustF, text="Add", command=addCust, bg="blue", fg="#FFFFFF", cursor="hand2", width=17,
           font=("Berlin Sans FB", 12)).grid(row=9, column=2, padx=20, pady=40)

    # go back button.
    Button(addCustF, text="Go Back", width=10, pady=2, font=("Berlin Sans FB", 12), bg="blue", fg="#FFFFFF",
           cursor="hand2", command=homeAdmin).grid(row=9, column=3, sticky=(E), padx=5, pady=10)

    # modify customers frame.
    # labels and entry widgets for customers details.
    modCusID = StringVar()
    Label(modCustF, text="Customer ID:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=3, column=0, sticky=(E),
                                                                                            padx=10, pady=10)
    modCustIDE = Entry(modCustF, textvariable=modCusID, width=40, font=("Berlin Sans FB", 12), bd=2)
    modCustIDE.grid(row=3, column=1, padx=10, pady=10)

    modFname = StringVar()
    Label(modCustF, text="First Name:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=4, column=0, sticky=(E),
                                                                                         padx=10, pady=10)
    modFnameE = Entry(modCustF, textvariable=modFname, width=40, font=("Berlin Sans FB", 12), bd=2)
    modFnameE.grid(row=4, column=1, padx=10, pady=10)

    modLname = StringVar()
    Label(modCustF, text="Last Name:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=5, column=0, sticky=(E),
                                                                                      padx=10, pady=10)
    modLnameE = Entry(modCustF, textvariable=modLname, width=40, font=("Berlin Sans FB", 12), bd=2)
    modLnameE.grid(row=5, column=1, padx=10, pady=10)

    modContact = StringVar()
    Label(modCustF, text="Contact:", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=6,
                                                   column=0, sticky=(E), padx=10, pady=10)
    modContactE = Entry(modCustF, textvariable=modContact, width=40, font=("Berlin Sans FB", 12), bd=2)
    modContactE.grid(row=6, column=1, padx=10, pady=10)

    modMem = StringVar()
    Label(modCustF, text="Membership(y/n):", bg="#FFFFFF", font=("Berlin Sans FB", 12)).grid(row=7, column=0, sticky=(E), padx=10,
                                                                                  pady=10)
    modMemberE = Entry(modCustF, textvariable=modMem, width=40, font=("Berlin Sans FB", 12), bd=2)
    modMemberE.grid(row=7, column=1, padx=10, pady=10)

    Button(modCustF, text="Modify", bg="blue", fg="#FFFFFF", command=modCust, cursor="hand2", width=17,
           font=("Berlin Sans FB", 12)).grid(row=9, column=2, padx=20, pady=10)

    Button(modCustF, text="Go Back", bg="blue", fg="#FFFFFF", command=homeAdmin, cursor="hand2", width=10,
           font=("Berlin Sans FB", 12)).grid(row=9, column=3, padx=20, pady=10)


    root.mainloop()

def unloading():
    # MySQL database connection
    engine = create_engine("mysql+pymysql://%s:%s@localhost:3306/%s"
                           % ('root', 'yazan2000', 'BSMS'), echo=False)
    source_connection = engine.connect()

    # Read the data from the database connection into a pandas DataFrame
    df = read_sql('SELECT * FROM admin', con=source_connection)
    df.to_csv('C:/users/yazon/Desktop/DBKursovaya/data/admin.csv')
    df.to_excel('C:/users/yazon/Desktop/DBKursovaya/data/admin.xlsx')

    df = read_sql('SELECT * FROM books', con=source_connection)
    df.to_csv('C:/users/yazon/Desktop/DBKursovaya/data/books.csv')
    df.to_excel('C:/users/yazon/Desktop/DBKursovaya/data/books.xlsx')

    df = read_sql('SELECT * FROM customers', con=source_connection)
    df.to_csv('C:/users/yazon/Desktop/DBKursovaya/data/customers.csv')
    df.to_excel('C:/users/yazon/Desktop/DBKursovaya/data/customers.xlsx')

    df = read_sql('SELECT * FROM sells', con=source_connection)
    df.to_csv('C:/users/yazon/Desktop/DBKursovaya/data/sells.csv')
    df.to_excel('C:/users/yazon/Desktop/DBKursovaya/data/sells.xlsx')

    df = read_sql('SELECT * FROM borrowing', con=source_connection)
    df.to_csv('C:/users/yazon/Desktop/DBKursovaya/data/borrowing.csv')
    df.to_excel('C:/users/yazon/Desktop/DBKursovaya/data/borrowing.xlsx')

if __name__ == '__main__':
    root = Tk()
    welcomePage()
    root.mainloop()
