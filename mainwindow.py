from customtkinter import *
from tkinter import * 
from tkinter import ttk
import pandas as pd 
import datetime 
'''
Branded Colours
background: bedrock dark gray "#2E2E2E"
hover: bedrock green "#72c05b"
foreground/accent: bedrock orange "#f37367"
'''
#define branded colours for repeated use in formatting of elements
bedrock_green= "#72c05b"
bedrock_orange= "#f37367"
bedrock_gray="#2E2E2E"

# Custom module imports to provide functionality to each secondary window



import adjust
from add_product import add_product
from BCUTILS import backup
import BCUTILS
import frontend_components
import order_manager
import stock_viewer
import table_edit


def main(): 
    r'''
    Function containing main window Tkinter GUI: includes 8 buttons linking to each main function 
    of software 
    '''
    win = CTk()
    win.geometry("1280x720")
    win.configure(fg_color="#2E2E2E")
    win.title("Bedrock Inventory System 1.1")
    titleframe = CTkFrame(win)
    titleframe.configure(fg_color="#2E2E2E")
    titleframe.grid(row=0, column=0)
    win.iconbitmap('datafiles/icon.ico')
    backup.create_backup()
    titleimg = PhotoImage(file="datafiles/bedrock.png")
    logotitle = Label(titleframe, image = titleimg,bg = "#2E2E2E")
    logotitle.grid(row=0, column= 0)
    titletext = Label(titleframe, text= "Bedrock Computers Inventory Management", font="Berlin, 20", bg="#2E2E2E", fg="#de6210")
    titletext.grid(row=0, column= 1, columnspan= 1,padx=20, pady=20)
    buttonframe= CTkFrame(win)
    buttonframe.configure(fg_color="#2E2E2E")
    buttonframe.grid(row=1, column=0, pady=50)
    hvcol="#72c05b"
    button_fg = "#de6210"

    #create button objects and provide necessary formatting and commands


    button1 = CTkButton(buttonframe, text="Add New Components", command=frontend_components.main,
    fg_color=button_fg,border_color="#72c05b",hover_color="#72c05b", height=100, width=200,corner_radius= 50) 
    
    button2 = CTkButton(buttonframe, text="Configure Shop Product", command=add_product.product_window,
    fg_color=button_fg,border_color="#72c05b",hover_color="#72c05b", height=100, width=200, corner_radius= 50) 

    button3 = CTkButton(buttonframe, text="Order Manager", command=order_manager.main,
    fg_color=button_fg,border_color="#72c05b",hover_color="#72c05b", height=100, width=200, corner_radius= 50)

    button4 = CTkButton(buttonframe, text="View Current Stock", command=stock_viewer.main_stock,
    fg_color=button_fg,border_color="#72c05b",hover_color="#72c05b", height=100, width=200,corner_radius= 50)  

    button5 = CTkButton(buttonframe, text="Stock Dashboard", command=stock_viewer.main_backup,
    fg_color=button_fg,border_color="#72c05b",hover_color="#72c05b", height=100, width=200, corner_radius= 50)

    button6 = CTkButton(buttonframe, text="Manage Database",command=table_edit.launch_stock_database_app,
    fg_color=button_fg,border_color="#72c05b",hover_color="#72c05b", height=100, width=200, corner_radius= 50) 

    button7 = CTkButton(buttonframe, text="Edit Stock |ADMIN|", command=adjust.runwin,
    fg_color=button_fg,border_color="#72c05b",hover_color="#72c05b",height=100, width=200, corner_radius= 50)

    button8 = CTkButton(buttonframe, text="Backup Database", command=BCUTILS.backup.create_backup,
    fg_color=button_fg,border_color="#72c05b",hover_color="#72c05b", height=100, width=200, corner_radius= 50) 
    

    #manually arange button placement on home screen for accessible visual interface. 
    
    button1.grid(row=4, column= 0,padx=15, pady=15)
    button2.grid(row=4, column=1,padx=15, pady=15)
    button3.grid(row=4, column=2,padx=15, pady=15)
    button4.grid(row=4, column=3,padx=15, pady=15)
    button5.grid(row=5, column=0,padx=15, pady=15)
    button6.grid(row=5, column=1,padx=15, pady=15)
    button7.grid(row=5, column=2,padx=15, pady=15)
    button8.grid(row=5, column=3,padx=15, pady=15)
    

    win.mainloop()


main()


