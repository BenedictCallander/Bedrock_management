from sqlite3 import connect
from tkinter import *
from tkinter import Toplevel, Frame, simpledialog, messagebox
from customtkinter import *
from math import isqrt
'''
colours
background: bedrock dark gray "#2E2E2E"
hover: bedrock green "#72c05b"
foreground/accent: bedrock orange "#f37367"
'''
bedrock_green= "#72c05b"
bedrock_orange= "#f37367"
bedrock_gray="#2E2E2E"
def get_data_from_db(table_name, name_column):
    conn = connect('bedrockdata/stock.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT {name_column} FROM {table_name}")
    return cursor.fetchall()

def add_components(window, table_name, name_column):
    window.destroy()
    window = Toplevel()
    window.geometry('1280x720')
    window.config(bg="#2E2E2E")
    window.iconbitmap("datafiles/icon.ico")
    data = get_data_from_db(table_name, name_column)
    grid_size = isqrt(len(data))

    maintitle=CTkLabel(window, text=f"{table_name} Component Import", font=("Berlin",30), text_color="#f37367")
    maintitle.grid(row=0,column=0)

    frame = CTkFrame(window,fg_color="#2E2E2E", border_color='black', border_width=2)
    frame.grid(row=1, column=0)

    for i, row in enumerate(data):
        CTkButton(
            frame,
            text=str(row[0]),
            fg_color="#f37367",
            hover_color="#72c05b",
            width=150, height=50, corner_radius=15,
            command=lambda r=row: update_stock(r, table_name, name_column),
            
            
        ).grid(row=i // grid_size, column=i % grid_size, padx=5, pady=5)  # padding between buttons

    CTkButton(
        window,
        text='Exit Window',
        fg_color="#f37367",
        hover_color="#72c05b",
        width=150, height=50,
        command=lambda: main(window)
    ).grid(row=2, column=0, pady=10)

    window.mainloop()

def update_stock(row, table_name, name_column):
    num = simpledialog.askinteger("Input", f"How many {row[0]} to add?")
    if num is not None:
        conn = connect('bedrockdata/stock.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table_name} SET stock = stock + ? WHERE {name_column} = ?", (num, row[0]))
        conn.commit()
        messagebox.showinfo("Success", f"Added {num} {row[0]} to stock")

def main(window=None):
    if window:
        window.destroy()
    window = Toplevel()
    window.geometry('600x300')
    window.iconbitmap("datafiles/icon.ico")
    window.config(bg=bedrock_gray)
    title_label=CTkLabel(window, text="Select Component Type", font=("Berlin",40), text_color=bedrock_orange)
    title_label.grid(row=0, column=0, columnspan=3)
    CTkButton(
        window,
        text='GPU',
        fg_color="#f37367",
        hover_color="#72c05b",
        width=150,height=50, corner_radius=20,
        command=lambda: add_components(window, 'GPU', 'name')
    ).grid(row=1, column=0, padx=5, pady=5)

    CTkButton(
        window,
        text='CPU',
        fg_color="#f37367",
        hover_color="#72c05b",
        width=150,height=50, corner_radius=20,
        command=lambda: add_components(window, 'CPU', 'name')
    ).grid(row=1, column=1, padx=5, pady=5)

    CTkButton(
        window,
        text='PSU',
        fg_color="#f37367",
        hover_color="#72c05b",
        width=150,height=50, corner_radius=20,
        command=lambda: add_components(window, 'PSU', 'power')
    ).grid(row=1, column=2, padx=5, pady=5)

    window.mainloop()

