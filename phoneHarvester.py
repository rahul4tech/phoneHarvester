import os, sys
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

# ask if user wants to compare the extracted phone numbers with other files
compare = input('Do you want to compare the extracted phone numbers with other files? (y/n) (default is y): ')

if column_name == '':
    # Set the name of the column you want to extract
    column_name = 'phone'

if compare == '':
    compare = 'y'

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
        data = pd.read_csv(file_path, encoding='ISO-8859-1')

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


if compare.lower() == 'n':
    sys.exit()


# Your existing code for merging phone numbers goes here...

# Read the merged phone numbers into a DataFrame
merged_phones = pd.read_csv(output_path)

# Set the directory containing the comparison CSV files
compare_directory = 'compare'

# set the clean directory for clean files
clean_directory = 'clean'

# Check if the compare directory exists
if not os.path.exists(compare_directory):
    print(f'Error: Compare directory "{compare_directory}" not found')
    sys.exit()

# Check if the clean directory exists and create it if it doesn't
if not os.path.exists(clean_directory):
    os.makedirs(clean_directory)

# Create a DataFrame to store the comparison results
comparison_results = pd.DataFrame(columns=['Filename', 'DuplicateCount'])

# Iterate over each file in the compare directory
for filename in os.listdir(compare_directory):
    if filename.endswith('.csv'):
        # Read the CSV file
        file_path = os.path.join(compare_directory, filename)
        compare_data = pd.read_csv(file_path, encoding='ISO-8859-1')
        # print(compare_data)

        # Check if the phone column exists in the file
        if column_name in compare_data.columns:
            # Find the intersection of phone numbers between the merged file and the current compare file
            duplicates = merged_phones.merge(compare_data[[column_name]], on=column_name)

            # Count the number of duplicates
            duplicate_count = len(duplicates)

            # Add the results to the comparison_results DataFrame
            new_row = pd.DataFrame({'Filename': [filename], 'DuplicateCount': [duplicate_count]})
            comparison_results = pd.concat([comparison_results, new_row], ignore_index=True)

            # Remove duplicates from the compare data
            compare_data_clean = compare_data[~compare_data[column_name].isin(duplicates[column_name])]

            # Save the cleaned compare data to a new file
            clean_file_path = os.path.join(clean_directory, f"clean_{filename}")
            compare_data_clean.to_csv(clean_file_path, index=False)



        else:
            print(f'Column "{column_name}" not found in file "{filename}"')

# Save the comparison results to a new CSV file
comparison_results.to_csv(specific_folderWithDate + '/comparison_results.csv', index=False)

# Print the completion message
print("\nComparison completed, results saved to", specific_folderWithDate + '/comparison_results.csv')
