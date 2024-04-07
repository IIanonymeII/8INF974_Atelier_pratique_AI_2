import os
import pandas as pd

def concatenate_csv_files(folder_path, output_file):
    # Get a list of all CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Initialize an empty DataFrame to store concatenated data
    concatenated_data = pd.DataFrame()

    # Loop through each CSV file and concatenate its data
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        data = pd.read_csv(file_path)
        concatenated_data = pd.concat([concatenated_data, data], ignore_index=True)

    # Write the concatenated data to a new CSV file
    concatenated_data.to_csv(output_file, index=False)
    print("Concatenation complete. Output saved to", output_file)

# Set the folder path containing CSV files and the output file path
folder_path = "Data\Volley\Raw"
output_file = "Data\Volley\Raw\output.csv"

# Call the function to concatenate CSV files
concatenate_csv_files(folder_path, output_file)
