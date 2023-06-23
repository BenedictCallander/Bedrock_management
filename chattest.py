import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk

def get_data_from_db(table_name, name_column):
    conn = sqlite3.connect('bedrockdata/stock.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT {name_column} FROM {table_name}")
    return cursor.fetchall()

def add_components(window, table_name, name_column):
    window.destroy()
    window = tk.Tk()
    window.geometry('400x400')

    data = get_data_from_db(table_name, name_column)
    for i, row in enumerate(data):
        ctk.CTkButton(
            window,
            text=str(row[0]),
            fg_color="#f37367",
            hover_color="#72c05b",
            command=lambda r=row: update_stock(r, table_name, name_column)
        ).grid(row=i, column=0)

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
    window = tk.Toplevel()
    window.geometry('400x400')

    ctk.CTkButton(
        window,
        text='GPU',
        fg_color="#f37367",
        hover_color="#72c05b",
        command=lambda: add_components(window, 'GPU', 'name')
    ).grid(row=0, column=0)

    ctk.CTkButton(
        window,
        text='CPU',
        fg_color="#f37367",
        hover_color="#72c05b",
        command=lambda: add_components(window, 'CPU', 'name')
    ).grid(row=1, column=0)

    ctk.CTkButton(
        window,
        text='PSU',
        fg_color="#f37367",
        hover_color="#72c05b",
        command=lambda: add_components(window, 'PSU', 'power')
    ).grid(row=2, column=0)

    window.mainloop()

if __name__ == "__main__":
    main()
