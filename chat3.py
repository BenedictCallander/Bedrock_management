from sqlite3 import connect
from tkinter import Toplevel, Frame, simpledialog, messagebox
from customtkinter import CTkButton, CTkLabel
from math import isqrt

def get_data_from_db(table_name, name_column):
    conn = connect('bedrockdata/stock.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT {name_column} FROM {table_name}")
    return cursor.fetchall()

def add_components(window, table_name, name_column):
    window.destroy()
    window = Toplevel()
    window.geometry('1280x720')

    data = get_data_from_db(table_name, name_column)
    grid_size = isqrt(len(data))

    maintitle=CTkLabel(window, text=f"{table_name} Component Import", font=("Berlin",30), text_color="#f37367")
    maintitle.grid(row=0,column=0)

    frame = Frame(window)
    frame.grid(row=1, column=0)

    for i, row in enumerate(data):
        CTkButton(
            frame,
            text=str(row[0]),
            fg_color="#f37367",
            hover_color="#72c05b",
            command=lambda r=row: update_stock(r, table_name, name_column),
            
            
        ).grid(row=i // grid_size, column=i % grid_size, padx=5, pady=5)  # padding between buttons

    CTkButton(
        window,
        text='Exit Window',
        fg_color="#f37367",
        hover_color="#72c05b",
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
