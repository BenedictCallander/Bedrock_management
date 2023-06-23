import sqlite3
from tkinter import *
from tkinter import messagebox, simpledialog
from customtkinter import *
import math
'''
colours
background: bedrock dark gray "#2E2E2E"
hover: bedrock green "#72c05b"
foreground/accent: bedrock orange "#f37367"
'''
def get_data_from_db(table_name, name_column):
    conn = sqlite3.connect('bedrockdata/stock.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT {name_column} FROM {table_name}")
    return cursor.fetchall()

def add_components(window, table_name, name_column):
    window.destroy()
    window = Toplevel()
    window.geometry('1280x720')
    maintitle=CTkLabel(window, text=f"{table_name} Component Import", font=("Berlin",30), text_color="#f37367")
    maintitle.grid(row=0,column=0)
    data = get_data_from_db(table_name, name_column)
    grid_size = math.isqrt(len(data))

    frame = CTkFrame(window)
    frame.grid(row=1,column=0)

    for i, row in enumerate(data):
        CTkButton(
            frame,
            text=str(row[0]),
            fg_color="#f37367",
            hover_color="#72c05b",
            command=lambda r=row: update_stock(r, table_name, name_column),
              # padding in x direction
               # padding in y direction
        ).grid(row=i // grid_size, column=i % grid_size, padx=5, pady=5)  # padding between buttons

    CTkButton(
        window,
        text='Exit Window',
        fg_color="#f37367",
        hover_color="#72c05b",
        command=window.destroy
    ).grid(row=2,column=0,padx=10,pady=10)

    window.mainloop()

def update_stock(row, table_name, name_column):
    num = simpledialog.askinteger("Input", f"How many {row[0]} to add?")
    if num is not None:
        conn = sqlite3.connect('bedrockdata/stock.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table_name} SET stock = stock + ? WHERE {name_column} = ?", (num, row[0]))
        conn.commit()
        messagebox.showinfo("Success", f"Added {num} {row[0]} to stock")

def main():
    window = Toplevel()
    window.geometry('400x400')

    CTkButton(
        window,
        text='GPU',
        fg_color="#f37367",
        hover_color="#72c05b",
        command=lambda: add_components(window, 'GPU', 'name')
    ).grid(row=0, column=0, padx=5, pady=5)

    CTkButton(
        window,
        text='CPU',
        fg_color="#f37367",
        hover_color="#72c05b",
        command=lambda: add_components(window, 'CPU', 'name')
    ).grid(row=1, column=0, padx=5, pady=5)

    CTkButton(
        window,
        text='PSU',
        fg_color="#f37367",
        hover_color="#72c05b",
        command=lambda: add_components(window, 'PSU', 'power')
    ).grid(row=2, column=0, padx=5, pady=5)

    window.mainloop()

if __name__ == "__main__":
    main()
