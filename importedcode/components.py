import numpy as np
import pandas as pd
import qrcode
import uuid

'''
dataframe convention: {"TYPE": , "BRAND": , "NAME": , "ID":, "Cost": , "Location":}
'''

class gpu:
    def __init__(self, brand, name,cost,location):
        self.brand=brand
        self.name=name
        self.id=uuid.uuid4()
        self.cost=cost
        self.type="GPU"
        self.location= location
        #return (self.brand, self.name, self.id)
    def add_gen(self):
        '''
        Generate QR code
        '''
        data = f'Type: {self.type}\nName: {self.name}'
        qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr_code.add_data(data)
        qr_code.make(fit=True)
        image = qr_code.make_image(fill_color="black", back_color="white")
        fname=f'temp_png/{self.type}_{self.name}.png'
        image.save(fname)
        '''
        add to dataframe
        '''
        dfin=pd.read_csv("requisites/gpu.csv")
        add=pd.DataFrame({"TYPE": str(self.type), "BRAND":str(self.brand) , "NAME": str(self.name), "ID": self.id,"Cost": self.cost , "Location": str(self.location)},index=[0])
        dflist=[dfin,add]
        dfout=pd.concat(dflist, axis='rows', ignore_index=True)
        dfout.to_csv("requisites/gpu.csv", index=False)

class cpu:
    def __init__(self, brand, name, location):
        self.brand=brand
        self.name=name
        self.location=location
        self.type="CPU"
        self.location=location
        self.id=uuid.uuid4()
    def add_gen(self):
        '''
        Generate QR CODE
        '''
        data = f'TYPE: {self.type}\nName: {self.name} \nID: {self.id}\nLocation: {self.location}'
        qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr_code.add_data(data)
        qr_code.make(fit=True)
        image = qr_code.make_image(fill_color="black", back_color="white")
        fname=f'temp_png/{self.type}_{self.name}.png'
        image.save(fname)
        '''
        add to document
        '''
        dfin=pd.read_csv("requisites/cpu.csv")
        add=pd.DataFrame({"TYPE": str(self.type), "BRAND":str(self.brand) , "NAME": str(self.name), "ID": self.id,"Location": str(self.location)},index=[0])
        dflist=[dfin,add]
        dfout=pd.concat(dflist, axis='rows', ignore_index=True)
        dfout.to_csv("requisites/cpu.csv", index=False)

class psu:
    def __init__(self,power, location):
        self.power=power
        self.location=location
    def add_gen(self):
        data=f'POWER{self.power}\nLocation{self.location}'
        qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr_code.add_data(data)
        qr_code.make(fit=True)
        image = qr_code.make_image(fill_color="black", back_color="white")
        fname=f'psu_png/{self.power}W.png'
        image.save(fname)
    