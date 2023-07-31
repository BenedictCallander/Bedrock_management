from tkinter import * 
from tkinter import ttk
from customtkinter import * 
import pandas as pd 
from tkinter import messagebox
import sqlite3

'''
colours
background: bedrock dark gray "#2E2E2E"
hover: bedrock green "#72c05b"
foreground/accent: bedrock orange "#f37367"
'''

class system:
    def __init__(self,brand, name, cpu, gpu, ram, storage):
        self.brand=brand
        self.name=name
        self.cpu=cpu
        self.gpu=gpu
        self.ram=ram
        self.storage=dict(storage)