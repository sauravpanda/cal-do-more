import os
import json


def store_data_to_file(filename, data):
    output_folder = './output/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the output file path
    output_file_path = os.path.join(output_folder, filename)

    # Write the result_list to the text file
    with open(output_file_path, 'w') as output_file:
        output_file.write(json.dumps(data))