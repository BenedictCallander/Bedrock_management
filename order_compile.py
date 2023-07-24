import numpy as np 
import pandas as pd
import os
import sqlite3
import additions_logic
from datetime import datetime, timedelta

from woocommerce import API
#15238
'''
given order number - calculate total materials and deduct stock
'''
# WooCommerce API credentials
url = "https://bedrock-computers.co.uk/"
consumer_key = "ck_e63f2847761567231436732f8c753e392fd81614"
consumer_secret = "cs_d40131313ebeeb4e1bd8b8fb67e41afd487685cf"
# Create the directory for storing order files
output_dir = 'orders/archive'
received_dir='orders/pending'
speedy_dir='orders/speedy'

os.makedirs(output_dir, exist_ok=True)

class order_get:
    def process_orders():
        # Calculate the date and time 24 hours ago
        start_date = datetime.now() - timedelta(hours=48)

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

        # Process each order
        for order in orders:
            order_id = order['id']
            output_file = os.path.join(output_dir, f"{order_id}.txt")
            output_file_received = os.path.join(received_dir, f"{order_id}.txt")
            output_file_speedy = os.path.join(speedy_dir, f"{order_id}.txt")

            # Skip if the order file already exists
            if os.path.exists(output_file):
                continue

            line_items = order['line_items']
            order_details = []
            customer=order['shipping']
            fullname = str(customer['first_name']) + ' ' + str(customer['last_name'])
            shipping_lines = order['shipping_lines']
            
            
            method_titles = []
#10549, 'method_title': 'Speedy Delivery:
#10560, 'method_title': 'Free Shipping
            for item in line_items:
                product_name = item['name']
                product_id=item['product_id']
                additions = item.get('meta_data', [])
            
                method_titles = [line.get("method_title", "") for line in shipping_lines][0]   
                method_id=[line.get("method_id","") for line in shipping_lines]
                
                # Filter out metadata starting with '_'
                filtered_additions = [a for a in additions if not a['key'].startswith('_')]
                filt2=[]
                for a in filtered_additions:
                    value=a.get('value')
                    if not (isinstance(value, str) and value.startswith(("None","No"))):
                        filt2.append(a)
                 
                
                addition_text = ''.join([f"{a['key']}: {str(a['value']).split('|',1)[0].strip()}\n" for a in filt2])
                
                
                # Format the order details
                order_details.append(f"order ID: {order_id}, customer {fullname} \n \n ")
                order_details.append(f"Shipping Method:  {method_titles}\n")
                order_details.append(f"Product Name: {product_name}")
                order_details.append(f"Product ID:{product_id} sss \n \n ")
                order_details.append(f"Additions:\n {addition_text}")
                
            # Write the order details to the file
            with open(output_file, 'w') as file:
                file.write('\n'.join(order_details))
            with open(output_file_received, 'w') as file:
                file.write('\n'.join(order_details))
            if method_id[0] =="flat_rate":
                with open(output_file_speedy, 'w') as file:
                    file.write('\n'.join(order_details))


class order_compile:
    def compile_order(order_id):
        conn= sqlite3.connect("bedrockdata/stock.db")
        c = conn.cursor()
        fpath=f"orders/pending/{order_id}.txt"
        product_id = additions_logic.extract_product_id(fpath)

        #default components:
        product_data=pd.read_csv(f'bedrockdata/systems/{product_id}.csv')
        
        '''
        ID,CPU,gen,RAM,GPU,storage,Dtype
        13259,i7-9th,4,16,RTX 2070 Super,512,SSD
        '''
        product_cpu = str(product_data['CPU'].values[0])
        product_gpu=str(product_data['GPU'].values[0])
        ram_logic=int(product_data['gen'])
        ram_check, ram_val=additions_logic.find_ram_logic(order_id)
        ram_storage=int(product_data['RAM'])

        if ram_check =='Y':
            product_ram= ram_val
        else:
            product_ram=ram_storage
        
        base_st_check=str(product_data['Dtype'].values[0])
        if base_st_check =='SSD':
            ssd_base=int(product_data['storage'].values[0])
            hdd_base=0
        elif base_st_check == 'HDD':
            hdd_base=int(product_data['storage'].values[0])
            ssd_base=0

        hd_check, hd_add =additions_logic.find_HDD_Logic(order_id)
        if hd_check =='Y':
            hd_tot=hdd_base+hd_add
        else:
            hd_tot=hdd_base
        
        sd_check, sd_add= additions_logic.ssd_logic(order_id)
        if sd_check =="Y":
            sd_tot=ssd_base+sd_add
        else:
            sd_tot=ssd_base
        print(sd_tot)
        if hd_tot != 0:
            c.execute(f"UPDATE hdd SET stock=stock-1 WHERE Capacity = {hd_tot}")
        if sd_tot != 0:
            c.execute(f"UPDATE ssd SET stock=stock-1 WHERE Capacity = {sd_tot}")
    
        table_name = 'ddr' + str(ram_logic)
        
        if product_ram == 16:
            c.execute(f"UPDATE {table_name} SET stock=stock-2 WHERE Capacity = 8")
        elif product_ram == 8:
            c.execute(f"UPDATE {table_name} SET stock=stock-2 WHERE Capacity = 4")
        elif product_ram ==24:
            c.execute(f"UPDATE {table_name} SET stock=stock-3 WHERE Capacity = 8")
        elif product_ram==32:
            c.execute(f"UPDATE {table_name} SET stock=stock-4 WHERE Capacity = 8")
        #
        #
        #
        print(product_cpu)
        c.execute(f"UPDATE CPU SET stock=stock-1 WHERE Name=?",[product_cpu])
        c.execute(f"UPDATE GPU SET stock=stock-1 WHERE Name=?",[product_gpu])


        conn.commit()
        conn.close()

