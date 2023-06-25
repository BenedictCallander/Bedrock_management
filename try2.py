import sqlite3
import customtkinter as ctk
from tkinter import Tk, Toplevel

class StockTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Connect to the database
        self.conn = sqlite3.connect('bedrockdata/stock.db')
        self.cursor = self.conn.cursor()

        # Get list of tables in the database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = self.cursor.fetchall()

        # Create a tab for each table
        for table in self.tables:
            self.add(table[0])

            # Get the name of the first column in the current table
            self.cursor.execute(f"PRAGMA table_info({table[0]});")
            first_column_name = self.cursor.fetchone()[1]

            # Query the database for the rows in the current table
            self.cursor.execute(f"SELECT {first_column_name}, stock FROM {table[0]};")
            rows = self.cursor.fetchall()

            # Display each row in the tab, along with buttons to adjust the stock quantity
            for i, (item, stock) in enumerate(rows):
                # Determine which column to place the item based on its index
                row = i // 2
                column = (i % 2) * 3

                label = ctk.CTkLabel(master=self.tab(table[0]), text=f"{item}: {stock}", fg_color="#f37367")
                label.grid(row=row, column=column, padx=10, pady=10, sticky='w')

                increase_button = ctk.CTkButton(master=self.tab(table[0]), text="+1", command=lambda item=item, table=table: self.adjust_stock(table[0], item, 1), fg_color="#f37367")
                increase_button.grid(row=row, column=column + 1, padx=10, pady=10)

                decrease_button = ctk.CTkButton(master=self.tab(table[0]), text="-1", command=lambda item=item, table=table: self.adjust_stock(table[0], item, -1), fg_color="#f37367")
                decrease_button.grid(row=row, column=column + 2, padx=10, pady=10)

    def adjust_stock(self, table, item, change):
        # Adjust the stock quantity in the database
        self.cursor.execute(f"UPDATE {table} SET stock = stock + {change} WHERE rowid = ?;", (item,))
        self.conn.commit()
        self.conn.close()

root = Tk()
root.withdraw()  # Hide the main Tk root window

app = Toplevel(root)
app.geometry("800x600")  # Set the window size
app.configure(background="#2E2E2E")

tab_view = StockTabView(master=app, fg_color="#2E2E2E")
tab_view.grid(row=0, column=0, padx=20, pady=20)

root.mainloop()
