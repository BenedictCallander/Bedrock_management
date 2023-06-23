import tkinter as tk
from tkinter import messagebox
import sqlite3


class StockDatabaseApp:
    def __init__(self, master):
        self.master = master
        master.title("Stock Database")
        master.geometry("800x600")
        master.configure(bg="#2C2C2C")

        # Create Frames
        self.add_frame = tk.Frame(master, bg="#2C2C2C")
        self.add_frame.grid(row=0, column=0, padx=20, pady=20)
        self.read_frame = tk.Frame(master, bg="#2C2C2C")
        self.read_frame.grid(row=0, column=1, padx=20, pady=20)

        self.create_widgets()

    def create_widgets(self):
        self.create_add_frame()
        self.create_read_frame()

    def create_add_frame(self):
        add_title_label = tk.Label(
            self.add_frame,
            text="Add Database Elements",
            font=("Arial", 16, "bold"),
            fg="#FFFFFF",
            bg="#2C2C2C",
        )
        add_title_label.pack(pady=10)

        # Create labels and entry fields for adding tables
        table_name_label = tk.Label(
            self.add_frame, text="Table Name:", fg="#FFFFFF", bg="#2C2C2C"
        )
        table_name_label.pack()
        self.table_name_entry = tk.Entry(self.add_frame)
        self.table_name_entry.pack()

        column_label = tk.Label(
            self.add_frame,
            text="Columns (separated by commas):",
            fg="#FFFFFF",
            bg="#2C2C2C",
        )
        column_label.pack()
        self.column_entry = tk.Entry(self.add_frame)
        self.column_entry.pack()

        heading_label = tk.Label(
            self.add_frame,
            text="Headings (separated by commas):",
            fg="#FFFFFF",
            bg="#2C2C2C",
        )
        heading_label.pack()
        self.heading_entry = tk.Entry(self.add_frame)
        self.heading_entry.pack()

        data_type_label = tk.Label(
            self.add_frame,
            text="Data Types (separated by commas):",
            fg="#FFFFFF",
            bg="#2C2C2C",
        )
        data_type_label.pack()
        self.data_type_entry = tk.Entry(self.add_frame)
        self.data_type_entry.pack()

        create_button = tk.Button(
            self.add_frame,
            text="Create Table",
            command=self.create_table,
            fg="#FFFFFF",
            bg="#1F7AFF",
        )
        create_button.pack(pady=10)

    def create_table(self):
        table_name = self.table_name_entry.get()
        columns = self.column_entry.get().split(",")
        headings = self.heading_entry.get().split(",")
        data_types = self.data_type_entry.get().split(",")

        # Validate inputs
        if not table_name or not columns or not headings or not data_types:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Connect to the SQLite database
        conn = sqlite3.connect("bedrockdata/stock.db")
        cursor = conn.cursor()

        try:
            # Create the new table
            query = f"CREATE TABLE {table_name} ("
            for i in range(len(columns)):
                query += f"{columns[i]} {data_types[i]}"
                if i != len(columns) - 1:
                    query += ","
            query += ")"
            cursor.execute(query)

            # Insert headings into the table
            query = f"INSERT INTO {table_name} VALUES ("
            for i in range(len(headings)):
                query += f"'{headings[i]}'"
                if i != len(headings) - 1:
                    query += ","
            query += ")"
            cursor.execute(query)

            conn.commit()
            messagebox.showinfo(
                "Success", f"Table '{table_name}' created successfully."
            )
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def create_read_frame(self):
        read_title_label = tk.Label(
            self.read_frame,
            text="Read Tables",
            font=("Arial", 16, "bold"),
            fg="#FFFFFF",
            bg="#2C2C2C",
        )
        read_title_label.pack(pady=10)

        # Create a listbox to display the tables
        table_label = tk.Label(
            self.read_frame, text="Tables:", fg="#FFFFFF", bg="#2C2C2C"
        )
        table_label.pack()
        self.table_listbox = tk.Listbox(self.read_frame, bg="#1F7AFF", fg="#FFFFFF")
        self.table_listbox.pack()

        # Button to read tables
        read_button = tk.Button(
            self.read_frame,
            text="Read Tables",
            command=self.read_tables,
            fg="#FFFFFF",
            bg="#1F7AFF",
        )
        read_button.pack(pady=10)

        # Button to add row
        add_row_button = tk.Button(
            self.read_frame,
            text="Add Row",
            command=self.add_row,
            fg="#FFFFFF",
            bg="#1F7AFF",
        )
        add_row_button.pack()

    def read_tables(self):
        # Connect to the SQLite database
        conn = sqlite3.connect("bedrockdata/stock.db")
        cursor = conn.cursor()

        try:
            # Fetch table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            self.table_listbox.delete(0, tk.END)  # Clear the listbox

            # Insert table names into the listbox
            for table in tables:
                self.table_listbox.insert(tk.END, table[0])
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def add_row(self):
        selected_table = self.table_listbox.get(tk.ACTIVE)
        if not selected_table:
            messagebox.showerror("Error", "Please select a table.")
            return

        # Connect to the SQLite database
        conn = sqlite3.connect("bedrockdata/stock.db")
        cursor = conn.cursor()

        try:
            # Get the column names for the selected table
            cursor.execute(f"PRAGMA table_info({selected_table})")
            columns = cursor.fetchall()

            # Create a new window for adding rows
            row_window = tk.Toplevel(self.master)
            row_window.title("Add Row")
            row_window.geometry("400x300")
            row_window.configure(bg="#2C2C2C")

            entries = []  # List to store the entry fields

            # Create labels and entry fields for each column
            for column in columns:
                label = tk.Label(
                    row_window, text=column[1], fg="#FFFFFF", bg="#2C2C2C"
                )
                label.pack()

                entry = tk.Entry(row_window)
                entry.pack()

                entries.append(entry)

            # Function to commit the row to the selected table
            def commit_row():
                values = []
                for entry in entries:
                    values.append(entry.get())

                try:
                    # Insert the row into the selected table
                    query = f"INSERT INTO {selected_table} VALUES ("
                    for i in range(len(values)):
                        query += f"'{values[i]}'"
                        if i != len(values) - 1:
                            query += ","
                    query += ")"
                    cursor.execute(query)

                    conn.commit()
                    messagebox.showinfo("Success", "Row added successfully.")
                    row_window.destroy()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

            commit_button = tk.Button(
                row_window, text="Commit", command=commit_row, fg="#FFFFFF", bg="#1F7AFF"
            )
            commit_button.pack()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def run(self):
        self.master.mainloop()


def launch_stock_database_app():
    root = tk.Tk()
    app = StockDatabaseApp(root)
    app.run()


if __name__ == "__main__":
    launch_stock_database_app()
