import sqlite3
from tkinter import *
from tkinter import Button
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
from typing import ClassVar
import numpy as np
import requests
import bs4
#import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



global eid
global ename
global esalary

# Function Part


def quote():
    try:
        wa = "https://www.brainyquote.com/quote_of_the_day"
        res = requests.get(wa)
        # print(res)

        data = bs4.BeautifulSoup(res.text, "html.parser")
        # print(data)

        info = data.find("img", {"class": "p-qotd"})
        # print(info)

        quote = info["alt"]

    except Exception as e:
        print("Issue", e)
    return quote


def display_add_win():
    add_window.deiconify()
    main_window.withdraw()


def display_main_win():
    main_window.deiconify()
    add_window.withdraw()


def clear():
    aw_ent_id.delete(0, END)
    aw_ent_name.delete(0, END)
    aw_ent_salary.delete(0, END)


def add_emp():
    try:
        con = None
        con = sqlite3.connect("emsproj.db")
        cursor = con.cursor()
        sql = "insert into emp values('%d','%s','%s')"
        eid = int(aw_ent_id.get())
        ename = aw_ent_name.get()
        esalary = aw_ent_salary.get()
        if (eid == "" or ename == "" or esalary == ""):
            showerror("Error in input", "Please fill all the details")
        else:
            if eid > 0:
                if ((len(ename) >= 2) and (ename.isalpha())):
                    if (int(esalary) >= 8000):
                        cursor.execute(sql % (eid, ename, esalary))
                        con.commit()
                        showinfo("Success", "Record Added")
                        clear()
                    else:
                        showerror("Issue", "Salary should be minimum  Rs.8000")
                        clear()
                else:
                    showerror("Issue", "Name should contain only alphabets and length should be more than 2 eg: om")
                    clear()
            else:
                showerror("Issue", "id should be positive integer")
                clear()
    except sqlite3.IntegrityError:
        showerror("Issue","Id exits") 
        clear()
    except ValueError:
        showerror("Issue","Please Enter all details")
        clear()
    con.rollback()


def view_emp():
    view_window.deiconify()
    main_window.withdraw()
    vw_store_data.delete(1.0, END)
    info = ""
    con = None

    try:
        con = connect("emsproj.db")
        cursor = con.cursor()
        cursor.execute("select * from emp")
        data = cursor.fetchall()
        for d in data:
            info = info + "Id:" + \
                str(d[0]) + "  Name:" + str(d[1]) + \
                "      Salary: " + str(d[2]) + "\n"
        vw_store_data.insert(INSERT, info)
        con.commit()

    except Exception as e:
        showerror(e)
    finally:
        if con is not None:
            con.close()


def update_emp():
    try:
        con = None
        con = connect("emsproj.db")
        cursor = con.cursor()

        eid = int(aw_ent_id.get())
        ename = aw_ent_name.get()
        esalary = aw_ent_salary.get()
        if (eid == "" or ename == "" or esalary == ""):
            showerror("Error in input", "Please fill all the details")
        else:
            if eid > 0:
                if ((len(ename) >= 2) and (ename.isalpha())):
                    if (int(esalary) >= 8000):
                        cursor.execute(
                            "update emp set ename =?, esalary=? where eid=?", (ename, esalary, eid))
                        if cursor.rowcount == 1:
                            con.commit()
                            showinfo("Success", "Record updated")
                        else:
                            showerror("Issue", "Id does not exists")
                    else:
                        showerror("Issue", "Salary should be minimum Rs.8000")
                        clear()
                else:
                    showerror(
                        "Issue", "Name should contain only alphabets and length should be more than 2 eg: om")
                    clear()
            else:
                showerror("Issue", "id should be positive integer")
    except ValueError:
        showerror("Issue","Please Enter all details")
        clear()
        con.rollback()
    clear()


def delete_emp():
    con = None
    try:
        con = connect("emsproj.db")
        cursor = con.cursor()
        sql = "delete from emp where eid = '%d'"
        eid = int(aw_ent_id.get())
        cursor.execute(sql % (eid))
        if cursor.rowcount == 1:
            con.commit()
            showinfo("Success", "Record Deleted")
        else:
            showerror("Issue", " Id Does Not Exists")

    except Exception as e:
        showerror("Issue ", e)
        con.rollback()
    finally:
        aw_ent_id.delete(0, END)
        if con is not None:
            con.close()

def emp_chart():
    con = None
    try:
        conn=sqlite3.connect('emsproj.db')
        CC=conn.cursor()
        plt.figure()
        # ax1=plt.subplot(1, 1, 1)
        def addlabels(names,int_salary):
            for i in range(len(names)):
                plt.text(i, int_salary[i], int_salary[i], ha = 'center')

        def graph_data():

            CC.execute('SELECT ename,esalary FROM emp ORDER BY esalary LIMIT 5 ')
        
            names=[]
            salary=[]
        
            for row in CC.fetchall():
                names.append(row[0])
                salary.append(row[1])

            int_salary =[int(i) for i in salary]
            plt.bar(names,int_salary,label='salary')
            addlabels(names, int_salary)
            plt.xlabel("Names")
            plt.ylabel("Salary")

            plt.title("Top 5 highest paid employees")

            plt.show()
        graph_data()

        
    except Exception as e:
        print("Issue", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()



def display_main_win1():
    main_window.deiconify()
    view_window.withdraw()


def display_update_win():
    update_window.deiconify()
    main_window.withdraw()


def display_main_win2():
    main_window.deiconify()
    update_window.withdraw()


def display_delete_win():
    delete_window.deiconify()
    main_window.withdraw()


def display_main_win3():
    main_window.deiconify()
    delete_window.withdraw()

def display_main_win4():
    main_window.deiconify()
    chart_window.withdraw()


def display_chart_win():
    chart_window.deiconify()
    main_window.withdraw()

# Design Part
# main window
main_window = Tk()
main_window.title("Employee Management System")
main_window.geometry("500x500+100+100")

f = ("Comic Sans MS", 10, "bold")
quoteFont = ("Times New Roman", 12)
authFont = ("Times New Roman", 18, "bold")


eid = IntVar()
ename = StringVar()
esalary = StringVar()

# declaring button
mw_btn_add = Button(main_window, text="ADD", font=f,
                    width=10, command=display_add_win)
mw_btn_view = Button(main_window, text="VIEW", font=f,
                     width=10, command=view_emp)
mw_btn_update = Button(main_window, text="UPDATE", font=f,
                       width=10, command=display_update_win)
mw_btn_delete = Button(main_window, text="DELETE", font=f,
                       width=10, command=display_delete_win)
mw_btn_chart = Button(main_window, text="CHARTS", font=f, width=10,command=display_chart_win)


# Everyday Quote
quotes = quote()
quote = quotes[:quotes.find("-")]
authorName = quotes[quotes.find("-"):]

mw_lbl = Label(main_window, text=quote, font=quoteFont)
mw_auth_lbl = Label(main_window, text=authorName, font=authFont)

# packing of buttons
mw_btn_add.pack(pady=10)
mw_btn_view.pack(pady=10)
mw_btn_update.pack(pady=10)
mw_btn_delete.pack(pady=10)
mw_btn_chart.pack(pady=10)
mw_lbl.pack(padx=10, pady=10)
mw_auth_lbl.pack(pady=10)


# Add Window
add_window = Toplevel(main_window)
add_window.title("Add Employee")
add_window.geometry("500x500+100+100")

aw_lbl_id = Label(add_window, text="Enter Emp ID:", font=f)
aw_ent_id = Entry(add_window, textvariable=eid, font=f, bd=4)

aw_lbl_name = Label(add_window, text="Enter Emp Name:", font=f)
aw_ent_name = Entry(add_window, textvariable=ename, font=f, bd=4)

aw_lbl_salary = Label(add_window, text="Enter Emp Salary:", font=f)
aw_ent_salary = Entry(add_window, textvariable=esalary, font=f, bd=4)

aw_btn_save = Button(add_window, text="Save", font=f, command=add_emp)
aw_btn_back: Button = Button(
    add_window, text="Back", font=f, command=display_main_win)

aw_lbl_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_lbl_name.pack(pady=10)
aw_ent_name.pack(pady=10)
aw_lbl_salary.pack(pady=10)
aw_ent_salary.pack(pady=10)
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)

add_window.withdraw()

# View Employee details

view_window = Toplevel(main_window)
view_window.title("View Employee Details")
view_window.geometry("500x500+100+100")

vw_store_data = ScrolledText(view_window, width=100, height=10, font=f)
vw_btn_back = Button(view_window, text="Back", font=f,
                     command=display_main_win1)

vw_store_data.pack(pady=10)
vw_btn_back.pack(pady=10)

view_window.withdraw()

# Update Employee Window
update_window = Toplevel(main_window)
update_window.title("Update Employee")
update_window.geometry("500x500+100+100")

aw_lbl_id = Label(update_window, text="Enter Emp ID:", font=f)
aw_ent_id = Entry(update_window, textvariable=eid, font=f, bd=4)

aw_lbl_name = Label(update_window, text="Enter Emp Name:", font=f)
aw_ent_name = Entry(update_window, textvariable=ename, font=f, bd=4)

aw_lbl_salary = Label(update_window, text="Enter Emp Salary:", font=f)
aw_ent_salary = Entry(update_window, textvariable=esalary, font=f, bd=4)

aw_btn_save = Button(update_window, text="Save", font=f, command=update_emp)
aw_btn_back: Button = Button(
    update_window, text="Back", font=f, command=display_main_win2)

aw_lbl_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_lbl_name.pack(pady=10)
aw_ent_name.pack(pady=10)
aw_lbl_salary.pack(pady=10)
aw_ent_salary.pack(pady=10)
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)

update_window.withdraw()

# Delete Emp Details
delete_window = Toplevel(main_window)
delete_window.title("Delete Employee")
delete_window.geometry("500x500+100+100")

aw_lbl_id = Label(delete_window, text="Enter Emp ID:", font=f)
aw_ent_id = Entry(delete_window, textvariable=eid, font=f, bd=4)

aw_btn_delete = Button(delete_window, text="Delete",
                       font=f, command=delete_emp)
aw_btn_back: Button = Button(
    delete_window, text="Back", font=f, command=display_main_win3)

aw_lbl_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_btn_delete.pack(pady=10)
aw_btn_back.pack(pady=10)

delete_window.withdraw()

# Chart of Top 5 highest paid salary emp
chart_window = Toplevel(main_window)
chart_window.title("Bar Chart of top 5 highest salaried Employee")
chart_window.geometry("500x500+100+100")

cw_btn_view_chart = Button(chart_window, text="View Chart", font=f, command=emp_chart)
cw_btn_back = Button(chart_window, text="Back", font=f, command=display_main_win4)

cw_btn_view_chart.pack(pady=10)
cw_btn_back.pack(pady=10)
chart_window.withdraw()

main_window.mainloop()
