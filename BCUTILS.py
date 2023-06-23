import os
import sqlite3
import pandas as pd 
from datetime import datetime
import matplotlib.pyplot as plt
def cleardir(dir):
    for filename in os.listdir(dir):
        file_path=os.path.join(dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
def getprintlist(directory, output_file):
    filenames = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            filenames.append(filename)

    with open(output_file, 'w') as file:
        file.write('\n'.join(filenames))



class backup:
    def create_backup():
        # Connect to the original database
        conn_orig = sqlite3.connect('bedrockdata/stock.db')
        c_orig = conn_orig.cursor()

        # Connect to the backup database
        conn_backup = sqlite3.connect('bedrockdata/stock_backup.db')
        c_backup = conn_backup.cursor()

        # Fetch all table names in the database
        table_query = "SELECT name FROM sqlite_master WHERE type='table';"
        c_orig.execute(table_query)
        tables = c_orig.fetchall()

        # For each table in the database, fetch the last column and append
        for table in tables:
            table = table[0]  # extract table name from tuple
            query = f"PRAGMA table_info({table});"
            c_orig.execute(query)
            columns = c_orig.fetchall()

            # Get the last column name
            last_col_name = columns[-1][1]

            # Fetch the entire table from the original database
            df_orig = pd.read_sql_query(f"SELECT * FROM {table}", conn_orig)

            # Fetch the entire table from the backup database
            df_backup = pd.read_sql_query(f"SELECT * FROM {table}", conn_backup)

            # Append the last column of the original table to the backup table with a new name (current datetime)
            df_backup[str(datetime.now().strftime("%Y-%m-%d %H:%M"))] = df_orig[last_col_name]

            # Write the updated dataframe back to the backup database
            df_backup.to_sql(table, conn_backup, if_exists='replace', index=False)

        # Close the connections to the databases
        conn_orig.close()
        conn_backup.close()

def plot_psu():
    conn=sqlite3.connect("bedrockdata/stock_backup.db")
    df=pd.read_sql_query("SELECT * FROM psu",con=conn)
    df2=df.copy()
    df = df.transpose()
    new_header = list(df2['power'])
    df = df[2:]
    df.columns = new_header
        
    # Plot the evolution of each stock item
    df.plot(marker='o',figsize=(10,5))
    plt.xlabel('Time')
    plt.ylabel('Stock')
    plt.title('Stock Evolution')
    plt.xticks(rotation=45, ha="right")
    plt.legend(loc='upper right')
    fpath="bedrockdata/temp_psu.png"
    plt.savefig(fpath,bbox_inches='tight')
    conn.commit()
    conn.close()
