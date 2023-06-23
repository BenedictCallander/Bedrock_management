import requests
from datetime import datetime, timedelta
from woocommerce import API
def extract_product_id(file_path):
    with open(file_path, 'r') as file:
        content=file.read()
        #Product ID:8370
        start_index = content.find("Product ID:")
        if start_index == -1:
            return None

        end_index = content.find(" sss", start_index)
        if end_index == -1:
            return None

        # Extract the number from the text string
        number_text = content[start_index + len("Product ID:"):end_index]
        number = int(number_text)

        return number

def extract_hdd_space(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        # Search for the specific text string
        start_index = content.find("Extra HDD space: +")
        if start_index == -1:
            return None

        end_index = content.find("GB (£15.00)", start_index)
        if end_index == -1:
            return None

        # Extract the number from the text string
        number_text = content[start_index + len("Extra HDD space: +"):end_index]
        number = int(number_text)

        return number
  

def find_HDD_Logic(order_id):
    fpath=f"orders/pending/{order_id}.txt"
    hard_addition=extract_hdd_space(fpath)
    if hard_addition is not None:
        stor_cond="Y"
        addition_storage=hard_addition
        return stor_cond, addition_storage
    else:
        stor_cond="N"
        return stor_cond,None
           

def extract_ram_space(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        # Search for the specific text string
        start_index = content.find("Memory:")
        if start_index == -1:
            return None

        end_index = content.find("GB (£", start_index)
        if end_index == -1:
            return None

        # Extract the number from the text string
        number_text = content[start_index + len("Memory:"):end_index]
        number = int(number_text)

        return number
    
def find_ram_logic(order_id):
    fpath=f"orders/pending/{order_id}.txt"
    ram=extract_ram_space(fpath)
    if ram is not None:
        ram_cond="Y"
        ram_value=ram
        return ram_cond,ram_value
    else:
        ram_cond="N"
        return ram_cond, None
    
def extract_ssd_size(fpath):
    with open(fpath, 'r') as file:
        content = file.read()

        # Search for the specific text string
        start_index = content.find("Solid state size: ")
        if start_index == -1:
            return None

        end_index = content.find("GB SSD", start_index)
        if end_index == -1:
            return None

        # Extract the number from the text string
        number_text = content[start_index + len("Solid state size:"):end_index]
        number = int(number_text)

        return number

def ssd_logic(order_id):
    fpath=f"orders/pending/{order_id}.txt"
    ssd_storage=extract_ssd_size(fpath)
    if ssd_storage is not None:
        ssd_condition="Y"
        return ssd_condition, ssd_storage
    else:
        ssd_condition="N"
        return ssd_condition, None
    