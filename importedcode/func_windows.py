from tkinter import * 
from tkinter import ttk
from customtkinter import * 
import pandas as pd 
import numpy as np
import components as components 
import BCUTILS
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

'''
colours
background: bedrock dark gray "#2E2E2E"
hover: bedrock green "#72c05b"
foreground/accent: bedrock orange "#f37367"
'''

class input_windows:
    def import_window():
        subwin=CTkToplevel()
        subwin.title("BEDROCK: IMPORT NEW STOCK")
        subwin.geometry=("700x700")
        subwin.configure(fg_color="#2E2E2E")
        title_text=CTkLabel(subwin, text="Import New Components", font=("Berlin",50), text_color="#f37367")
        title_text.grid(row=0,column=0,columnspan= 2,padx=20, pady=20)
        cgpu_directory="temp_png/"
        psu_directory="psu_png/"
        gcpu_frame=CTkFrame(subwin,border_width=5, border_color="black")
        gcpu_frame.configure(fg_color="#2E2E2E")
        gcpu_frame.grid(row=1, column=0, padx=20,pady=20)
        #BCUTILS.cleardir(cgpu_directory)
        
        label_title=CTkLabel(gcpu_frame, text="Add Stock", font=("Berlin", 20), text_color="#f37367")
        label_title.grid(row=0,column=0, columnspan= 4,padx=20,pady=20)
        label_type = CTkLabel(gcpu_frame, text="Product Type:", font=("Berlin", 20), text_color="#f37367")
        label_type.grid(row=1, column= 1,padx=20,pady=20)
        label_brand= CTkLabel(gcpu_frame, text="Brand", font=("Berlin", 20), text_color="#f37367")
        label_brand.grid(row=2, column= 1,padx=20,pady=20)
        label_name = CTkLabel(gcpu_frame, text="Product Name:", font=("Berlin", 20), text_color="#f37367")
        label_name.grid(row=3, column= 1,padx=20,pady=20)
        label_location= CTkLabel(gcpu_frame, text="Location", font=("Berlin", 20), text_color="#f37367")
        label_location.grid(row=4, column= 1,padx=20,pady=20)
        
        label_cost=CTkLabel(gcpu_frame, text="Cost:",font=("Berlin",20), text_color="#f37367")
        label_cost.grid(row=5, column=1,padx=20,pady=20)

        entry_type=CTkEntry(gcpu_frame, width=200)
        entry_brand=CTkEntry(gcpu_frame,width=200)
        entry_name= CTkEntry(gcpu_frame,width=200)
        entry_location= CTkEntry(gcpu_frame,width=200)
        entry_cost=CTkEntry(gcpu_frame, width=200)
        
        entry_type.grid(row=1, column= 2,columnspan=3,padx=20,pady=20)
        entry_brand.grid(row=2, column= 2,columnspan=3,padx=20,pady=20)
        entry_name.grid(row=3, column= 2,columnspan=3,padx=20,pady=20)
        entry_location.grid(row=4, column=2,columnspan=3,padx=20,pady=20)
        entry_cost.grid(row=5, column=2,columnspan=3,padx=20,pady=20)
        
        
        def buttonpress_CGPU():
            check= str(entry_type.get())
            if check == "CPU":
                addtask= components.cpu(entry_brand.get(), entry_name.get(), entry_location.get())
                addtask.add_gen()
                entry_type.delete(0,END)
                entry_brand.delete(0,END)
                entry_location.delete(0,END)
                entry_name.delete(0,END)

            elif check == "GPU":
                addtask= components.gpu(entry_brand.get(), entry_name.get(), entry_cost.get(),entry_location.get())
                addtask.add_gen()
                conn=sqlite3.connect("requisites/stock.db")
                c=conn.cursor()
                c.execute("UPDATE gpu SET stock = stock + 1 WHERE name= ?",[addtask.name])
                conn.commit()
                conn.close()
                entry_type.delete(0,END)
                entry_brand.delete(0,END)
                entry_location.delete(0,END)
                entry_name.delete(0,END)
            else:
                messagebox.showerror("ERROR", "Invalid Type")
                entry_type.delete(0,END)
                entry_brand.delete(0,END)
                entry_location.delete(0,END)
                entry_name.delete(0,END)
            
        def printbuttonpress_CGPU():
            BCUTILS.getprintlist(cgpu_directory,"requisites/printlist.txt")

        submit_button= CTkButton(gcpu_frame, text="Submit",width=250, height=100, fg_color="#f37367", hover_color= "#72c05b", corner_radius=15,command=buttonpress_CGPU)
        submit_button.grid(row=6, column= 2, columnspan=2,padx=20,pady=20)
        printlist_button= CTkButton(gcpu_frame, text="Printlist",width=250, height=100, fg_color="#f37367", hover_color= "#72c05b",corner_radius=15, command=printbuttonpress_CGPU)
        printlist_button.grid(row=7, column= 2,columnspan=2,padx=20,pady=20)

        power_frame=CTkFrame(subwin,border_width=5, border_color="black")
        power_frame.configure(fg_color="#2E2E2E")
        power_frame.grid(row=1, column=1,padx=50, pady=20)
        title_label=CTkLabel(power_frame, text= "Power Supply import", font=("Berlin", 40),text_color="#f37367")

        label_power= CTkLabel(power_frame, text= "Power(W)", font=("Berlin", 20),text_color="#f37367")
        entry_power=CTkEntry(power_frame, width=150, height=28, corner_radius=15,placeholder_text="e.g. 500", placeholder_text_color= "#f37367")
        label_newstock= CTkLabel(power_frame, text= "New Units", font=("Berlin", 20),text_color="#f37367")
        entry_newstock=CTkEntry(power_frame, width=200, height=28, corner_radius=15,placeholder_text="e.g. 1, 5", placeholder_text_color= "#f37367")

        title_label.grid(row=0, column=1,padx=20,pady=20)
        label_power.grid(row=1, column=0,padx=20,pady=20)
        entry_power.grid(row=1, column=1,padx=10,pady=20)

        label_newstock.grid(row=2, column=0,pady=20)
        entry_newstock.grid(row=2, column=1,pady=20)

        def buttonpress_PSU():
            conn=sqlite3.connect("requisites/stock.db")
            c=conn.cursor()
            c.execute("UPDATE psu SET stock= stock+? WHERE power=?",(entry_newstock.get(), entry_power.get()))
            conn.commit()
            conn.close()
            entry_newstock.delete(0,END)
            entry_power.delete(0,END)
        def printbuttonpress_PSU():
            BCUTILS.getprintlist(psu_directory,"requisites/psu_printlist.txt")
        button_psu=CTkButton(power_frame, text="Submit",width=150, height=75, fg_color="#f37367", hover_color= "#72c05b", corner_radius=30,command=buttonpress_PSU)
        button_psu.grid(row=3, column=1,pady=20,padx=10)
        printlist_button= CTkButton(power_frame, text="Printlist",width=150, height=75, fg_color="#f37367", hover_color= "#72c05b",corner_radius=30, command=printbuttonpress_PSU)
        printlist_button.grid(row=4, column= 1,pady=20,padx=10)
                
        subwin.mainloop()

class view_window:
    def view():
        viewsubwin=CTkToplevel()
        viewsubwin.configure(fg_color="#2E2E2E")
        viewsubwin.geometry("1280x720")
        
        
        tabview=CTkTabview(master=viewsubwin, width=1200, height=600)
        tabview.pack(padx=20,pady=20)
        tab1=tabview.add("CPU")
        tab2=tabview.add("GPU")
        tab3=tabview.add("PSU")
        tab4=tabview.add("Graphics")
        tabview.configure(fg_color="#f37367",
                          border_color='black',
                          segmented_button_fg_color="#2E2E2E",
                          segmented_button_unselected_color="#fcba03",
                          segmented_button_selected_color="#72c05b")
        
        tabs=[tab1,tab2,tab3,tab4]
        for tab in tabs:
            tab.configure(fg_color="#2E2E2E")
        
        

        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",background="#2a2d2e",foreground="white",rowheight=25,fieldbackground="#343638",bordercolor="#343638",borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat")
        style.map("Treeview.Heading",background=[('active', '#3484F0')])

        #
        #GPU
        #
        gpu_title_label=CTkLabel(tab2, text="GPU STOCK", font=("Berlin",20), text_color="#f37367")
        gpu_title_label.grid(row=0, column=0, padx=20, pady=20)
        #
        #read data
        #
        df_gpu= pd.read_csv("requisites/gpu.csv")
        gpu_list_brand= list(df_gpu['BRAND'])
        gpu_list_name=list(df_gpu['NAME'])
        gpu_list_loc=list(df_gpu['Location'])
        gpu_list_cost=list(df_gpu['Cost'])
        gpu_list_id=list(df_gpu['ID'])
        #
        #plot tree
        #
        gpu_headings = ("Brand", "Name", "Location", "Cost", "ID")
        gpu_tree = ttk.Treeview(tab2, columns=gpu_headings, show='headings')
        gpu_tree.grid(row=1, column=0, padx=20, pady=20)
        for heading in gpu_headings:
            gpu_tree.heading(heading, text=heading)
        for brand, name,location,cost,id in zip(gpu_list_brand, gpu_list_name,gpu_list_loc,gpu_list_cost,gpu_list_id):
            gpu_tree.insert('', 'end', values=(brand, name, location,cost,id))

        #
        #
        #

        #
        #CPU
        #

        df_cpu= pd.read_csv("requisites/cpu.csv")
        cpu_list_brand= list(df_cpu['BRAND'])
        cpu_list_name=list(df_cpu['NAME'])
        cpu_list_id=list(df_cpu['ID'])
        cpu_list_loc=list(df_cpu['Location'])

        cpu_title_label=CTkLabel(tab1, text="CPU STOCK", font=("Berlin",20), text_color="#f37367")
        cpu_title_label.grid(row=0, column=0, padx=20, pady=20)

        cpu_headings= ("Brand","Name","Location", "ID")
        cpu_tree=ttk.Treeview(tab1,columns=cpu_headings, show='headings')
        cpu_tree.grid(row=1, column=0,pady=20,padx=20)
        for heading in cpu_headings:
            cpu_tree.heading(heading, text=heading)
        
        for brand,name,location, id in zip(cpu_list_brand, cpu_list_name,cpu_list_loc, cpu_list_id):
            cpu_tree.insert('', 'end', values=(brand,name,location,id))

        #
        #
        #
        def sort_column(tree, col, reverse):
            data = [(tree.set(child, col), child) for child in tree.get_children("")]
            data.sort(key=lambda x: int(x[0]), reverse=reverse)
            for index, (value, child) in enumerate(data):
                tree.move(child, "", index)
            tree.heading(col, command=lambda: sort_column(tree, col, not reverse))
        
        #
        #psu_
        #
        conn=sqlite3.connect("requisites/stock.db")
        c = conn.cursor()
        c.execute('SELECT * from psu')
        datapsu = c.fetchall()
        psu_title_label=CTkLabel(tab3, text="PSU STOCK", font=("Berlin",20), text_color="#f37367")
        psu_title_label.grid(row=0, column=0, padx=20, pady=20)
        psu_headings = ("Power", "Price", "Stock")
        psu_tree = ttk.Treeview(tab3, columns=psu_headings, show='headings')
        psu_tree.grid(row=1, column=0,padx=20,pady=20)

        for heading in psu_headings:
            psu_tree.heading(heading, text=heading, command=lambda col=heading: sort_column(psu_tree, col, False))
        for i, (power, price, stock) in enumerate(datapsu):
            psu_tree.insert('', 'end', values=(power, price, stock))

            sum=0
        power,price,stock= zip(*datapsu)

        for i in range(len(power)):
            value=price[i]*stock[i]
            sum=sum+value
        total=CTkLabel(tab3,text=f'Total Value: £{sum}',font=("Berlin", 20),text_color="#f37367")
        total.grid(row=3, column=0,padx=20,pady=20)

        plot_title= CTkLabel(tab3, text="PSU Stock History", text_color="#f37367", font=("Berlin", 30))
        plot_title.grid(row=0,column=5,padx=20,pady=20)
        fpath="requisites/temp_psu.png"
        plot_image=CTkImage(light_image=Image.open(fpath),size=(500,300))
        img_label=CTkLabel(tab3, image=plot_image, text='')
        img_label.grid(row=1,column=5,padx=20,pady=20)

        conn.commit()
        conn.close()
        
        
        
        
        
        tree = ttk.Treeview(tab4)
        columns = ['GPU', 'VRAM', 'Power Consumption', 'Cost', 'Stock Level']

        # Set the column headings in the Treeview
        tree['columns'] = columns
        tree.heading('#0', text='Index', anchor='w')
        for col in columns:
            tree.heading(col, text=col, anchor='w')

        # Connect to the SQLite database
        conn = sqlite3.connect('requisites/stock.db')

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Execute a SELECT query to fetch the data from the "graphics" table
        cursor.execute("SELECT * FROM graphics")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Insert the fetched data into the Treeview
        for i, row in enumerate(rows):
            tree.insert('', 'end', text=i+1, values=row)

        # Pack the Treeview widget
        tree.pack()
        
        viewsubwin.mainloop()
        
class adjustment_windows:
    def pricewindow():
        win=CTkToplevel()
        win.geometry=("1280x720")
        win.configure(fg_color="#2E2E2E")


        ramframe=CTkFrame(win)
        powerframe=CTkFrame(win)
        cpuframe=CTkFrame(win)
        gpuframe=CTkFrame(win)

        ramframe.grid(row=0, column=0,padx=20, pady=20); ramframe.configure(fg_color="#2E2E2E")
        powerframe.grid(row=0, column=1,padx=20, pady=20); powerframe.configure(fg_color="#2E2E2E")
        gpuframe.grid(row=0, column=2,padx=20, pady=20); gpuframe.configure(fg_color="#2E2E2E")
        
        
        '''
        ram ENTRIES
        '''

        title_ram= CTkLabel(ramframe, text= "RAM", text_color="#f37367", font=("Arial", 30))
        

        text_ram_generation = CTkLabel(ramframe, text="RAM GENERATION:", text_color="#f37367")
        entry_ram_generation=CTkEntry(ramframe, width=200, height=28, corner_radius=15,
        placeholder_text="GENERATION", placeholder_text_color= "#f37367")
        
        
        text_ram_capacity = CTkLabel(ramframe, text="RAM CAPACITY:", text_color="#f37367")
        entry_ram_capacity=CTkEntry(ramframe, width=200, height=28, corner_radius=15,
        placeholder_text="CAPACITY", placeholder_text_color= "#f37367")
        
        text_ram_cost= CTkLabel(ramframe, text="RAM COST:", text_color="#f37367")
        entry_ram_cost=CTkEntry(ramframe, width=200, height=28, corner_radius=15,
        placeholder_text="COST", placeholder_text_color= "#f37367")


        title_ram.grid(row=0, column=1,padx=20, pady=20)
        
        text_ram_generation.grid(row=1, column=0,padx=20, pady=20)
        text_ram_capacity.grid(row=2, column=0,padx=20, pady=20)

        entry_ram_generation.grid(row=1, column=1,padx=20, pady=20)
        entry_ram_capacity.grid(row=2, column=1,padx=20, pady=20)


        text_ram_cost.grid(row=3, column=0,padx=20, pady=20)
        entry_ram_cost.grid(row=3, column=1,padx=20, pady=20)

        def do_ram():
            conn= sqlite3.connect("requisites/stock.db")
            c=conn.cursor()
            c.execute("UPDATE ram SET price= ? WHERE gen=? AND capacity=?",
            (entry_ram_cost.get(), entry_ram_generation.get(),entry_ram_capacity.get()))
            conn.commit()
            conn.close()
            entry_ram_capacity.delete(0,END)
            entry_ram_cost.delete(0,END)
            entry_ram_generation.delete(0,END)
        

        button_ram= CTkButton(ramframe, width= 150, height=40, corner_radius=15, text= "Commit change", command= do_ram)
        button_ram.grid(row=4, column=0, columnspan=2,padx=20, pady=20)
        

        '''
        PSU Entries
        '''

        title_PSU = CTkLabel(powerframe, text="PSU", text_color="#f37367", font=("Arial", 30))


        text_PSU_power=CTkLabel(powerframe, text="PSU POWER", text_color="#f37367", font=("Arial", 20))
        text_PSU_price=CTkLabel(powerframe, text="PSU COST", text_color="#f37367", font=("Arial", 20))


        entry_PSU_power= CTkEntry(powerframe, width=200, height=28, corner_radius=15)
        entry_PSU_cost= CTkEntry(powerframe, width=200, height=28, corner_radius=15)

        title_PSU.grid(row=0, column=1,padx=20, pady=20)

        text_PSU_power.grid(row=1, column=0,padx=20, pady=20)
        text_PSU_price.grid(row=2, column=0,padx=20, pady=20)

        entry_PSU_power.grid(row=1, column=1,padx=20, pady=20)
        entry_PSU_cost.grid(row=2, column=1,padx=20, pady=20)
        def dopower():
            conn=sqlite3.connect("requisites/stock.db")
            c= conn.cursor()
            c.execute("UPDATE psu SET price=? WHERE power=?", (entry_PSU_cost.get(), entry_PSU_power.get()))
            conn.commit()
            conn.close()
            entry_PSU_cost.delete(0,END)
            entry_PSU_power.delete(0,END)

        button_power= CTkButton(powerframe, width= 150, height=40, corner_radius=15, text= "Commit change", command= dopower)
        button_power.grid(row=3, column=0, columnspan=2,padx=20, pady=20)

        '''
        GPU Entries
        '''

        title_GPU= CTkLabel(gpuframe, text= "GPU",text_color="#f37367", font=("Arial", 30) )

        text_GPU_brand= CTkLabel(gpuframe, text="BRAND", text_color="#f37367", font=("Arial", 20))
        text_GPU_name= CTkLabel(gpuframe, text= "NAME", text_color="#f37367", font=("Arial", 20))
        text_GPU_cost= CTkLabel(gpuframe, text="COST", text_color="#f37367", font=("Arial", 20))


        entry_GPU_brand=CTkEntry(gpuframe, width=200, height=28, corner_radius=15)
        entry_GPU_name=CTkEntry(gpuframe, width=200, height=28, corner_radius=15)
        entry_GPU_cost=CTkEntry(gpuframe, width=200, height=28, corner_radius=15)

        title_GPU.grid(row=0, column=1,padx=20, pady=20)
        text_GPU_brand.grid(row=1, column=0,padx=20, pady=20)
        text_GPU_name.grid(row=2, column=0,padx=20, pady=20)
        text_GPU_cost.grid(row=3, column=0,padx=20, pady=20)
        entry_GPU_brand.grid(row=1, column=1,padx=20, pady=20)
        entry_GPU_name.grid(row=2, column=1,padx=20, pady=20)
        entry_GPU_cost.grid(row=3, column=1,padx=20, pady=20)

        def do_gpu():
            conn=sqlite3.connect("requisites/stock.db")
            c=conn.cursor()
            c.execute("UPDATE gpu SET price=? WHERE brand=? AND name=? ",
            (entry_GPU_cost.get(),entry_GPU_brand.get(), entry_GPU_name.get())
            )
            conn.commit()
            conn.close()

            entry_GPU_brand.delete(0,END)
            entry_GPU_cost.delete(0,END)
            entry_GPU_name.delete(0,END)

        button_GPU = CTkButton(gpuframe, width= 150, height=40, corner_radius=15, text= "Commit change", command= do_gpu)
        button_GPU.grid(row=4, column=0, columnspan=2,padx=20, pady=20)
        win.mainloop()
