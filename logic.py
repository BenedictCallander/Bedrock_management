import numpy as np 
import pandas as pd 
import sqlite3
'''
'''


def shipping_class():
    r'''
    INPUTS: Order data
    
    PROCESS: checks weight and calculates necessary shiping class
    
    OUTPUTS: relevant shipping method
    
    '''
    

def item_location():
    r'''
    INPUTS: Item type/info
    
    PROCESS; checks storage dictionary to find location
    
    OUTPUTS: Item Location 
    
    '''


def ram_sticks(capacity):
    r'''
    INPUT: RAM CAPACITY OF ORDER
    ram logic: Assume 2 slots on board; configurations as such 
    will include further logic to implement manual change to 4 slot config in future
    
    OUTPUT(Number of 4GB Sticks, Number of 8GB Sticks)
    '''
    if capacity == 8:
        no_4 = 2
        no_8=0
    elif capacity==16:
        no_4=4 
        no_8=2
    elif capacity==12:
        no_4=1
        no_8=1
    return (no_4, no_8)

'''
lists
'''

def get_cpu_list():
    cpu_list = [
    "Intel Core i3-4XXX","Intel Core i5-4XXX","Intel Core i7-4XXX","Intel Core i3-5XXX",
    "Intel Core i5-5XXX","Intel Core i7-5XXX","Intel Core i3-6XXX","Intel Core i5-6XXX",
    "Intel Core i7-6XXX","Intel Core i3-7XXX","Intel Core i5-7XXX","Intel Core i7-7XXX",
    "Intel Core i3-8XXX","Intel Core i5-8XXX","Intel Core i7-8XXX","Intel Core i9-8XXX",
    "Intel Core i3-9XXX","Intel Core i5-9XXX","Intel Core i7-9XXX","Intel Core i9-9XXX",
    "Intel Core i3-10XXX","Intel Core i5-10XXX","Intel Core i7-10XXX","Intel Core i9-10XXX",
    "Intel Core i3-11XXX","Intel Core i5-11XXX","Intel Core i7-11XXX","Intel Core i9-11XXX",
    "Intel Core i3-12XXX","Intel Core i5-12XXX","Intel Core i7-12XXX","Intel Core i9-12XXX"
    ]
    return cpu_list


def get_cpus():

    intel_cpus = [
        # 4th Generation
        "i7-4770", "i5-4670", "i5-4570", "i3-4370",
        "i7-4790", "i5-4690", "i5-4590", "i3-4390",
        
        # 5th Generation
        "i7-5775C", "i5-5675C", "i5-5575R", "i3-5375C",
        
        # 6th Generation
        "i7-6700", "i5-6600", "i5-6500", "i3-6300",
        "i7-6700K", "i5-6600K", "i5-6500T",
        
        # 7th Generation
        "i7-7700", "i5-7600", "i5-7500", "i3-7300",
        "i7-7700K", "i5-7600K", "i5-7500T",
        
        # 8th Generation
        "i7-8700", "i5-8600", "i5-8500", "i3-8300",
        "i7-8700K", "i5-8600K", "i5-8500T",
        
        # 9th Generation
        "i7-9700", "i5-9600", "i5-9500", "i3-9300",
        "i7-9700K", "i5-9600K", "i5-9500T",
        
        # 10th Generation
        "i7-10700", "i5-10600", "i5-10500", "i3-10300",
        "i7-10700K", "i5-10600K", "i5-10500T",
        
        # 11th Generation
        "i7-11700", "i5-11600", "i5-11500", "i3-11300",
        "i7-11700K", "i5-11600K", "i5-11500T",
        
        # 12th Generation (Alder Lake)
        "i7-12700", "i5-12600", "i5-12500", "i3-12300",
        "i7-12700K", "i5-12600K", "i5-12500T"
    ]

    power_consumption = [
        # 4th Generation
        84, 84, 84, 54,
        84, 84, 84, 54,
        
        # 5th Generation
        65, 65, 65, 65,
        
        # 6th Generation
        65, 65, 65, 47,
        91, 91, 35,
        
        # 7th Generation
        65, 65, 65, 51,
        91, 91, 35,
        
        # 8th Generation
        65, 65, 65, 62,
        95, 95, 35,
        
        # 9th Generation
        65, 65, 65, 62,
        95, 95, 35,
        
        # 10th Generation
        65, 65, 65, 65,
        95, 95, 35,
        
        # 11th Generation
        65, 65, 65, 65,
        125, 125, 35,
        
        # 12th Generation (Alder Lake)
        125, 125, 125, 125,
        125, 125, 35
    ]

    dummy_price = [999.99] * len(intel_cpus)
    dummy_stock = [10] * len(intel_cpus)

    data = {
        'name': intel_cpus,
        'Power Consumption (W)': power_consumption,
        'Price': dummy_price,
        'Stock': dummy_stock
    }

    df = pd.DataFrame(data)
    conn = sqlite3.connect('bedrockdata/stock.db')

# Commit the DataFrame to a new table named "graphics"
    df.to_sql('CPU', conn, if_exists='replace', index=False)

# Close the database connection
    conn.close()


def get_gpus():
    
    gpu_names = [
        'GTX 750 Ti','GTX 760','GTX 770','GTX 780','GTX 780 Ti','GTX 950',
        'GTX 960','GTX 970','GTX 980','GTX 980 Ti','GTX 1050 Ti','GTX 1060',
        'GTX 1070','GTX 1070 Ti','GTX 1080','GTX 1080 Ti','GTX 1650','GTX 1660',
        'GTX 1660 Super','GTX 1660 Ti','RTX 2060','RTX 2060 Super','RTX 2070',
        'RTX 2070 Super','RTX 2080','RTX 2080 Super','RTX 2080 Ti','RTX 3060',
        'RTX 3060 Ti','RTX 3070','RTX 3070 Ti','RTX 3080','RTX 3080 Ti','RTX 3090']

    gpu_vram = [2, 2, 2, 3, 3, 2, 2, 4, 4, 6, 4, 3, 8, 8, 8, 11, 4, 6, 6, 6, 6, 8, 8, 8, 8, 11, 12, 8, 8, 8, 8, 10, 12, 24]

    power_consumption = [150, 170, 230, 250, 250, 75, 120, 145, 165, 250, 75, 120, 150, 180, 180, 250, 75, 120, 125, 120,
                        160, 175, 185, 215, 215, 260, 320, 200, 220, 240, 260, 320, 350, 350]

    cost = [150, 200, 250, 300, 350, 150, 200, 300, 350, 450, 200, 250, 350, 400, 500, 700, 200, 250, 300, 300, 350, 400,
            500, 600, 800, 1000, 350, 450, 500, 600, 800, 1000, 1500,2000]

    stock_levels = [1] * len(gpu_names)  # Set stock level to 1 for all GPUs
    print(len(gpu_names))
    print(len(gpu_vram))
    print(len(power_consumption))
    print(len(cost))
    # Create a DataFrame using the combined information
    data = {
        'name': gpu_names,
        'VRAM': gpu_vram,
        'Power Consumption': power_consumption,
        'Cost': cost,
        'Stock': stock_levels
    }

    df = pd.DataFrame(data)
    conn = sqlite3.connect('bedrockdata/stock.db')

# Commit the DataFrame to a new table named "graphics"
    df.to_sql('GPU', conn, if_exists='replace', index=False)

# Close the database connection
    conn.close()


def order_contents(orderin, id, cpu, ram, gpu, storage):
    datastring=orderin
    
    data={"ID":id, "CPU": cpu, "RAM":ram, "GPU": gpu, "storage":storage}
    
    return data


get_gpus()