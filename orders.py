import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from woocommerce import API
from customtkinter import *
# WooCommerce API credentials
url = "https://bedrock-computers.co.uk/"
consumer_key = "ck_e63f2847761567231436732f8c753e392fd81614"
consumer_secret = "cs_d40131313ebeeb4e1bd8b8fb67e41afd487685cf"
'''
colours
background: bedrock dark gray "#2E2E2E"
hover: bedrock green "#72c05b"
foreground/accent: bedrock orange "#f37367"
'''
def fetch_orders():
    # Calculate the date and time 24 hours ago
    start_date = datetime.now() - timedelta(hours=72)

    # Format the start date as required by the WooCommerce API
    start_date_formatted = start_date.strftime('%Y-%m-%dT%H:%M:%S')

    # Initialize the API object
    wcapi = API(url=url, consumer_key=consumer_key, consumer_secret=consumer_secret, version="wc/v3")

    # Prepare the query parameters
    params = {
        'after': start_date_formatted,
        'status': 'processing'
    }

    # Send the GET request to the WooCommerce API to retrieve orders
    orders = wcapi.get("orders", params=params).json()

    # Create a new Tkinter Toplevel frame for displaying the orders
    orderwin = CTkToplevel()
    orderwin.geometry("1280x720")
    orderwin.title("Order Details")
    orderwin.configure(fg_color="#2E2E2E")
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",background="#2a2d2e",foreground="white",rowheight=25,fieldbackground="#343638",bordercolor="#343638",borderwidth=0)
    style.map('Treeview', background=[('selected', '#22559b')])
    style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat")
    style.map("Treeview.Heading",background=[('active', '#3484F0')])
    # Create a Treeview widget for displaying the order data
    tree = ttk.Treeview(orderwin)
    tree['columns'] = ('product', 'additions')
    tree.column('product', width=400)
    tree.column('additions', width=500)
    tree.heading('product', text='Product Name')
    tree.heading('additions', text='Additions')

    # Insert order data into the Treeview
    for order in orders:
        order_id = order['id']
        line_items = order['line_items']
        for item in line_items:
            product_name = item['name']
            additions = item.get('meta_data', [])

            addition_text = ', '.join([f"{a['key']}: {a['value']}" for a in additions if not a['key'].startswith('_')])

            tree.insert('', 'end', text=order_id, values=(product_name, addition_text))

    # Pack the Treeview widget
    tree.pack(fill='both', expand=True)
    orderwin.mainloop()
