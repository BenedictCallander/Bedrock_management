import os
import sqlite3
import pandas as pd
from pandastable import Table
from tkinter import *
from tkinter import ttk

# Color configurations
bg_color = "#2E2E2E"
text_color = "#f37367"

def get_tables(conn):
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor = conn.cursor()
    cursor.execute(query)
    tables = cursor.fetchall()
    return [table[0] for table in tables]

def get_data_from_table(conn, table_name):
    df = pd.read_sql_query("SELECT * from " + table_name, conn)
    return df

class TableTab(Frame):
    def __init__(self, master, df, title):
        super().__init__(master, bg=bg_color)
        self.df = df
        self.table = pt = Table(self, dataframe=self.df, showtoolbar=True, showstatusbar=True)
        pt.show()

class DatabaseViewer:
    def __init__(self, root, db_path):
        self.root = root
        self.db_path = db_path
        self.root.config(bg=bg_color)
        self.conn = sqlite3.connect(self.db_path)
        self.tables = get_tables(self.conn)
        self.notebook = ttk.Notebook(self.root)

        for table_name in self.tables:
            df = get_data_from_table(self.conn, table_name)
            tab = TableTab(self.notebook, df, table_name)
            self.notebook.add(tab, text=table_name)

        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

def main_stock():
    root = Toplevel()
    root.title("BEDROCK:Database Viewer")
    app = DatabaseViewer(root, 'bedrockdata/stock.db')
    root.mainloop()

def main_backup():
    root = Toplevel()
    root.title("BEDROCK:Database Viewer")
    app = DatabaseViewer(root, 'bedrockdata/stock_backup.db')
    root.mainloop()

