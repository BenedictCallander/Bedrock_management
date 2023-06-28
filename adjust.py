import sqlite3
import tkinter as tk
from tkinter import ttk

class Application(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title('Stock Management')
        
        # Connect to the database
        self.conn = sqlite3.connect('bedrockdata/stock.db')
        self.cursor = self.conn.cursor()

        # Get list of tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = [table[0] for table in self.cursor.fetchall()]
        
        # Initialize notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        
        # Add tabs
        for table in self.tables:
            frame = TableFrame(self.notebook, self.conn, table)
            self.notebook.add(frame, text=table)

class TableFrame(tk.Frame):
    def __init__(self, parent, conn, table):
        tk.Frame.__init__(self, parent)
        
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.table = table
        
        self.build_gui()

    def build_gui(self):
        # Get table columns
        self.cursor.execute(f"PRAGMA table_info({self.table})")
        self.columns = [column[1] for column in self.cursor.fetchall()]

        # Get table data
        self.cursor.execute(f"SELECT * FROM {self.table}")
        self.rows = self.cursor.fetchall()

        # Build treeview
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')
        for column in self.columns:
            self.tree.heading(column, text=column)

        # Insert data to treeview
        for row in self.rows:
            self.tree.insert('', 'end', text=row[0], values=row, tags=row[0])

        self.tree.pack(fill='both', expand=True)

        # Add increment and decrement buttons
        self.incr_button = tk.Button(self, text="+1", command=self.increment_stock)
        self.decr_button = tk.Button(self, text="-1", command=self.decrement_stock)
        self.incr_button.pack(side='left')
        self.decr_button.pack(side='left')

    def update_stock(self, increment):
        selected_item = self.tree.selection()[0]
        stock_index = self.columns.index('stock')
        current_stock = self.tree.item(selected_item)['values'][stock_index]
        new_stock = current_stock + increment

        # Update in treeview
        values = list(self.tree.item(selected_item)['values'])
        values[stock_index] = new_stock
        self.tree.item(selected_item, values=values)

        # Update in database
        name_column = self.columns[0]
        item_name = self.tree.item(selected_item)['tags'][0]
        self.cursor.execute(f"UPDATE {self.table} SET stock = ? WHERE {name_column} = ?", (new_stock, item_name))
        self.conn.commit()

    def increment_stock(self):
        self.update_stock(1)

    def decrement_stock(self):
        self.update_stock(-1)

def runwin():
    app = Application()
    app.mainloop()
