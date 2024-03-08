import os
import pandas as pd

# Set the directory containing the CSV files
directory = 'files'

# Set the output directory for the combined file
output_dir = 'output'

# Check if the output directory exists and create it if it doesn't
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ask column name to extract default is phone
column_name = input('Enter column name to extract (default is phone): ')

if column_name == '':
    # Set the name of the column you want to extract
    column_name = 'phone'

specific_folderWithDate = 'output/' + pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M-%S')

if not os.path.exists(specific_folderWithDate):
    os.makedirs(specific_folderWithDate)

# Create an empty DataFrame to store the extracted data
combined_data = pd.DataFrame()

# Get a sorted list of all CSV filenames in the directory
filenames = sorted([f for f in os.listdir(directory) if f.endswith('.csv')])

# which files currently processing
fileOrders = []


# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        print("Please wait, processing file: ", filename)
        # Read the CSV file
        file_path = os.path.join(directory, filename)
        data = pd.read_csv(file_path)

        # Check if the desired column exists in the file
        if column_name in data.columns:
            fileOrders.append(filename+ ' - ' + 'Success')
            # Extract the column and add it to the combined DataFrame
            combined_data = pd.concat([combined_data, data[[column_name]]], ignore_index=True)
        else:
            fileOrders.append(filename + ' - ' + 'Failed, Column not found')
            print(f'Column "{column_name}" not found in file "{filename}"')

# Save the combined DataFrame to a new CSV file
filename_with_date = 'mergedPhone.csv'
output_path = os.path.join(specific_folderWithDate, filename_with_date)
combined_data.to_csv(output_path, index=False)

# write fileOrders to a file
with open(specific_folderWithDate + '/fileOrders.txt', 'w') as f:
    for item in fileOrders:
        f.write("%s\n" % item)



# print process completed at the end with the output directory and file name and date time
print("\nProcess completed, combined data saved to", output_path, "at", pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'))
