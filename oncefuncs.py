import pandas as pd 
import sqlite3
import numpy as np
conn = sqlite3.connect('bedrockdata/stock.db')

powers=np.arange(250,1000,50)
prices=[1]*len(powers)
stock=[1]*len(powers)
print(powers)
print(prices)
print(stock)


df=pd.DataFrame({"power":powers,"price":prices, "stock":stock})
df.to_sql('PSU', conn, if_exists='replace', index=False)

'''


generations = ['4th', '5th', '6th', '7th', '8th', '9th']
models = ['i3', 'i5', 'i7']

# Generate combinations of generations and models
cpu_list = [(model, generation) for generation in generations for model in models]

# Create dummy values for price and stock
dummy_price = [0] * len(cpu_list)
dummy_stock = [0] * len(cpu_list)

# Create the dataframe
df = pd.DataFrame(cpu_list, columns=['Model', 'Generation'])
df['Price'] = dummy_price
df['Stock'] = dummy_stock

# Combine name and generation columns
df['Name'] = df['Model'] + '-' + df['Generation']

# Remove the 'Model' column
df.drop('Model', axis=1, inplace=True)

# Reorder the columns
df = df[['Name', 'Price', 'Stock']]

# Display the dataframe
print(df)

'''


