import pandas as pd 
import sqlite3


class cpu:
    def __init__(self, model, generation,price_per_unit):
        self.model=model
        self.generation=generation
        self.price=price_per_unit

    