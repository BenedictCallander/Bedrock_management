from tkinter import * 
from tkinter import ttk
from customtkinter import * 
import pandas as pd 
#import numpy as np
#import components as components 
#import BCUTILS
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
class add_product:
    def product_window():
        prodwin=CTkToplevel()
        prodwin.configure(fg_color="#2E2E2E")
        options_in= pd.read_csv("bedrockdata/products.csv")
        names=list(options_in['Name'])
        product_ids=list(options_in['ID'])
        
        maintitle=CTkLabel(prodwin, text="Add Product", font=("Berlin",30), text_color="#f37367")
        maintitle.grid(row=0, column=1, columnspan=3,padx=20,pady=20)
        
        menu=CTkOptionMenu(prodwin, width=300, height=40, corner_radius=20, values=names)
        menu.grid(row=1, column=1,padx=20,pady=20)
        
        entry_CPU=CTkEntry(prodwin, width=200,placeholder_text="CPU")
        entry_GPU=CTkEntry(prodwin, width=200, placeholder_text="GPU")
        entry_ram=CTkEntry(prodwin, width=200,placeholder_text="RAM")
        entry_storage=CTkEntry(prodwin, width=200,placeholder_text="Storage")
        ramvar=StringVar(value="3")
        ramgen=CTkSegmentedButton(prodwin, variable=ramvar,values=['3','4'])
        storvar=StringVar(value="HDD")
        stortyp=CTkSegmentedButton(prodwin,variable=storvar, values=['HDD','SSD'])
        
        entry_CPU.grid(row=2,column=1,padx=20,pady=20)
        entry_GPU.grid(row=3, column=1,padx=20,pady=20)
        entry_ram.grid(row=4, column=1,padx=20,pady=20)
        ramgen.grid(row=4, column=2,pady=20)
        entry_storage.grid(row=5, column=1,padx=20,pady=20)
        stortyp.grid(row=5, column=2,pady=20)
        
        def addsystem():
            sysname=menu.get()
            sysinfo=options_in[options_in['Name'].isin([sysname])]
            prod_id=int(sysinfo['ID'])
            cpu_info=entry_CPU.get()
            gpu_info=entry_GPU.get()
            ram_gen=int(ramgen.get())
            raminfo=int(entry_ram.get())
            stor_cap=int(entry_storage.get())
            stor_type=stortyp.get()
            sys_info={"ID":prod_id, "CPU": cpu_info,"gen": ram_gen, "RAM":raminfo , "GPU": gpu_info, "storage":stor_cap, "Dtype":stor_type}
            data=pd.DataFrame(sys_info, index=[0])
            data.to_csv(f"bedrockdata/systems/{prod_id}.csv", index=False)
            
            entry_CPU.delete(0,END)
            entry_GPU.delete(0,END)
            entry_ram.delete(0,END)
            entry_storage.delete(0,END)
        
        addbutton=CTkButton(prodwin, text="submit:", command=addsystem, width=200, height=100, corner_radius=40, fg_color="#f37367")
        addbutton.grid(row=6, column=1, columnspan=2, padx=20, pady=20)
        
        '''
        data={"ID":id, "CPU": cpu,"gen": gen, "RAM":ram , "GPU": gpu, "storage":storage, "Dtype":store_type}
        '''
    
        prodwin.mainloop()
