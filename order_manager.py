import os
import shutil
from customtkinter import *
from tkinter import *

# Color configurations
bg_color = "#2E2E2E"
text_color = "#f37367"

class DirectoryFrame(Frame):
    def __init__(self, master, directory, title, btn_text=None, btn_command=None):
        super().__init__(master, bg=bg_color)
        self.directory = directory

        self.title = Label(self, text=title, bg=bg_color, fg=text_color)
        self.title.grid(row=0, column=0, sticky="nsew")

        self.file_list = Listbox(self, bg=bg_color, fg=text_color)
        self.file_content = Text(self, bg=bg_color, fg=text_color)

        self.file_content.grid(row=0, column=1, rowspan=3, sticky="nsew")

        self.populate_files()

        self.file_list.bind('<<ListboxSelect>>', self.show_content)
        self.file_list.grid(row=1, column=0, sticky="nsew")

        if btn_text and btn_command:
            self.button = CTkButton(self, text=btn_text, command=btn_command, fg_color=text_color)
            self.button.grid(row=2, column=0, sticky="nsew")

    def populate_files(self):
        files = os.listdir(self.directory)
        self.file_list.delete(0, END)
        for file in files:
            if file.endswith('.txt'):
                self.file_list.insert(END, file)

    def show_content(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            with open(os.path.join(self.directory, data), 'r') as file:
                content = file.read()
                self.file_content.delete(1.0, END)
                self.file_content.insert(END, content)

    def get_selected_file(self):
        return self.file_list.get(ACTIVE)

    def remove_selected_file(self):
        selection = self.file_list.curselection()
        if selection:
            self.file_list.delete(selection)

    def clear_content(self):
        self.file_content.delete(1.0, END)

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.config(bg=bg_color)

        self.pending_frame = DirectoryFrame(root, "orders/pending", "Pending", "Accept", self.accept_file)
        self.received_frame = DirectoryFrame(root, "orders/received", "Received", "Processing", self.process_file)
        self.processing_frame = DirectoryFrame(root, "orders/processing", "Processing", "Complete", self.complete_file)

        self.pending_frame.grid(row=0, column=0, sticky="nsew")
        self.received_frame.grid(row=0, column=1, sticky="nsew")
        self.processing_frame.grid(row=0, column=2, sticky="nsew")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def accept_file(self):
        file_name = self.pending_frame.get_selected_file()
        shutil.move(os.path.join(self.pending_frame.directory, file_name), self.received_frame.directory)
        self.pending_frame.remove_selected_file()
        self.pending_frame.clear_content()
        self.received_frame.populate_files()

    def process_file(self):
        file_name = self.received_frame.get_selected_file()
        shutil.move(os.path.join(self.received_frame.directory, file_name), self.processing_frame.directory)
        self.received_frame.remove_selected_file()
        self.received_frame.clear_content()
        self.processing_frame.populate_files()

    def complete_file(self):
        file_name = self.processing_frame.get_selected_file()
        shutil.move(os.path.join(self.processing_frame.directory, file_name), "orders/complete")
        self.processing_frame.remove_selected_file()
        self.processing_frame.clear_content()

def main():
    root = Toplevel()
    root.iconbitmap("datafiles/icon.ico")
    root.title("BEDROCK: Order Manager")
    app = FileManager(root)
    root.mainloop()

