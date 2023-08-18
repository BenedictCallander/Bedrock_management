from customtkinter import * 
from woocommerce import API

from tkinter import * 
import pandas as pd 
import os
from datetime import datetime, timedelta
url = "https://bedrock-computers.co.uk/"
consumer_key = "ck_e63f2847761567231436732f8c753e392fd81614"
consumer_secret = "cs_d40131313ebeeb4e1bd8b8fb67e41afd487685cf"

bedrock_green= "#72c05b"
bedrock_orange= "#f37367"
bedrock_gray="#2E2E2E"

output_dir = 'orders/archive'
received_dir='orders/pending'
speedy_dir='orders/speedy'

class App(CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color=bedrock_gray)
        self.title("Order Manager")
        #self.geometry("600x850")
        self.title=CTkLabel(self, text="ORDER MANAGER", text_color= bedrock_green, font=("Berlin",30))
        self.title.grid(row=0,column=0)
        self.listframe=CTkFrame(self,width=200,height=300)
        self.listframe.grid(row=1,column=0)

        self.notesframe=CTkFrame(self, width=600, height=500)
        self.notesframe.grid(row=3,column=0,columnspan=1)



        self.buttonsframe=CTkFrame(self, width=200,height=300,fg_color=bedrock_gray)
        self.buttonsframe.grid(row=1,column=1)


        self.filelist=Listbox(self.listframe, bg=bedrock_gray, fg=bedrock_orange)

        self.get_orders_list()
        self.filelist.pack()      
        self.get_order_button=CTkButton(self.buttonsframe, text="Get Order Info", command=self.listbox_button, fg_color= bedrock_orange, text_color= bedrock_green)
        self.get_order_button.grid(row=0,column=0)

        self.info_textbox=CTkTextbox(self, fg_color= bedrock_gray,
                                    text_color=bedrock_green,width=500,height=400)
        self.info_textbox.grid(row=2,column=0,columnspan=3)

        self.manual_id=Entry(self.buttonsframe)
        self.manual_id.grid(row=1,column=0)

        self.manual_button=CTkButton(self.buttonsframe, text="Get Manual Order Info", command=self.manual_entry, fg_color= bedrock_orange, text_color= bedrock_green)
        self.manual_button.grid(row=1,column=1)


        self.notesentry=CTkEntry(self.notesframe, width=600,height=250, corner_radius=15, placeholder_text="Notes", placeholder_text_color= bedrock_gray)
        self.notesentry.pack()

        self.notespushbutton=CTkButton(self.notesframe, text="push note", fg_color=bedrock_green,command=self.order_notes)
        self.notespushbutton.pack()
    def get_orders_list(self):
        start_date = datetime.now() - timedelta(hours=48)
        start_date_formatted = start_date.strftime('%Y-%m-%dT%H:%M:%S')
        wcapi = API(url=url, consumer_key=consumer_key, consumer_secret=consumer_secret, version="wc/v3")
        params = {'after': start_date_formatted,'status': 'processing'}
        # Send the GET request to the WooCommerce API to retrieve orders
        orders = wcapi.get("orders", params=params).json()
        current_orders=[]
        for order in orders:
            current_orders.append(order['id'])
            self.filelist.insert(END,order['id'])
    def listbox_button(self):
        order_id= self.filelist.get(ACTIVE)
        self.order_id_perm=order_id
        self.fill_order_info(order_id)
    def manual_entry(self):
        order_id=self.manual_id.get()
        self.order_id_perm=order_id
        self.fill_order_info(order_id)

    def fill_order_info(self,order_id):
        self.info_textbox.delete(0.0, END)
        
                
        wcapi = API(url=url, consumer_key=consumer_key, consumer_secret=consumer_secret, version="wc/v3")
        link="orders/"+str(order_id)
        order=wcapi.get(link).json()

        line_items=order['line_items']
        


        for item in line_items:
            order_details=[]
            ship_chunk=order['shipping']
            fullname= str(ship_chunk['first_name'])+' '+ str(ship_chunk['last_name'])
            shipping_lines=order['shipping_lines']
            product_name=item['name']
            product_id = item['product_id']
            additions = item.get('meta_data', [])
            method_titles = [line.get("method_title", "") for line in shipping_lines][0]   
            method_id=[line.get("method_id","") for line in shipping_lines]


            filtered_additions = [a for a in additions if not a['key'].startswith('_')]
            filt2=[]
            for a in filtered_additions:
                value=a.get('value')
                if not (isinstance(value, str) and value.startswith(("None","No"))):
                        filt2.append(a)
            addition_text = ''.join([f"{a['key']}: {str(a['value']).split('|',1)[0].strip()}\n" for a in filt2])
                
                
                # Format the order details
            order_details.append(f"order ID: {order_id}, customer {fullname} \n \n")
            order_details.append(f"Shipping Method:  {method_titles}\n")
            order_details.append(f"Product Name: {product_name}")
            order_details.append(f"Product ID:{product_id} sss\n\n")
            order_details.append(f"Additions:\n {addition_text}")
            order_details="".join(order_details)
            self.info_textbox.insert(END, order_details)
    def order_notes(self):
        wcapi = API(url=url, consumer_key=consumer_key, consumer_secret=consumer_secret, version="wc/v3")
        notedata=self.notesentry.get()
        noteslink="orders/"+str(self.order_id_perm)+"/notes"
        notedata={"note": notedata, "customer_note": "false"}
        wcapi.post(noteslink, notedata).json()
        self.notesentry.delete(0,END)


orderman = App()
orderman.mainloop()
