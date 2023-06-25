import sqlite3
import tkinter as tk
import customtkinter as ctk

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in self.cursor.fetchall()]

    def get_table_data(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def update_stock(self, table_name, item_id, new_stock):
        self.cursor.execute(f"UPDATE {table_name} SET stock = ? WHERE id = ?", (new_stock, item_id))
        self.conn.commit()

class App:
    def __init__(self, root, db):
        self.root = root
        self.root.geometry('800x600')  # set a suitable window size
        self.db = db
        self.tabs = ctk.CTkTabview(self.root)

        for table in self.db.get_tables():
            tab_frame = tk.Frame(self.tabs)
            self.tabs.add(table)
            #self.populate_tab(tab_frame, table)

        self.tabs.pack(expand=1, fill='both')

    def populate_tab(self, tab, table_name):
        data = self.db.get_table_data(table_name)

        for idx, row in enumerate(data):
            tk.Label(tab, text=row[0]).grid(row=idx, column=0)  # row ID
            tk.Label(tab, text=row[-1]).grid(row=idx, column=1)  # stock quantity

            # Increment button
            inc_button = tk.Button(tab, text="+1", command=lambda row=row: self.update_stock(table_name, row[0], row[-1]+1))
            inc_button.grid(row=idx, column=2)

            # Decrement button
            dec_button = tk.Button(tab, text="-1", command=lambda row=row: self.update_stock(table_name, row[0], row[-1]-1))
            dec_button.grid(row=idx, column=3)

    def update_stock(self, table_name, item_id, new_stock):
        self.db.update_stock(table_name, item_id, new_stock)
        self.tabs.clear_tabs()  # clear current tabs

        for table in self.db.get_tables():
            tab_frame = tk.Frame(self.tabs)
            self.tabs.add_tab(tab_frame, text=table)
            self.populate_tab(tab_frame, table)

if __name__ == "__main__":
    root = tk.Tk()
    db = Database("bedrockdata/stock.db")
    app = App(root, db)
    root.mainloop()
