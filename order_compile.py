import numpy as np 
import pandas as pd
import os



'''
compile a list of downloaded orders.
Get from API and write text file with list -> keep on file during processing and received,
to archived orders when completed
'''
def receivedtotext():
    directory = 'orders/received'
    output_file = 'orders/received.txt'

    # Collect all filenames in the directory
    filenames = os.listdir(directory)

    # Create a list to store the file names
    file_names_list = []

    # Iterate over the filenames and extract the file names
    for filename in filenames:
        # Append the file name to the list
        file_names_list.append(filename)

    # Write the file names to the output file
    with open(output_file, 'w') as file:
        # Write each file name on a new line
        for file_name in file_names_list:
            file.write(file_name + '\n')