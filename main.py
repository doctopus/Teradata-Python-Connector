import database_connection
import excel_processing
import data_wrangling
import pandas as pd
import database_queryback
# import config

# Connection and fetching Caris Data
table_name = "CASE_META_CARIS_FIREHOSE"
schema_name = "DL_MAGIC_PROD"
carisData = database_connection.connect_and_fetch_table(table_name, schema_name)

# Second part: create a local database from an Excel file
excel_file_path = '~/Desktop/MRNs.xlsx' # Excel file with data in one column PAT_MRN_ID [For Local Run]
# excel_file_path = 'io/MRNs.xlsx' #This is dummy MRNs for github! [NOT REAL MRN] [For Github]

localData = excel_processing.load_mrn_ids_from_excel(excel_file_path)

# Connection and fetching Tempus Data
table_name = "CASE_META_TEMPUS"
schema_name = "DL_MAGIC_PROD"
tempusData = database_connection.connect_and_fetch_table(table_name, schema_name)

# Other required variables/constants
start_date = pd.to_datetime('2022-08-01')
end_date = pd.to_datetime('2023-05-31')

# Data wrangling and filtering
final_filtered_df = data_wrangling.perform_data_wrangling(carisData, localData, tempusData, start_date, end_date)

# Set option to show all rows of dataframe
pd.set_option('display.max_rows', None)
print(final_filtered_df)

pat_mrn_ids = final_filtered_df["PAT_MRN_ID"].tolist()
# Create the formatted string
formatted_ids = ""
for i, id_value in enumerate(pat_mrn_ids):
    formatted_ids += f"'{id_value}'"
    if i < len(pat_mrn_ids) - 1:
        formatted_ids += ",\n"
# Print the formatted string
# print("ID's of those patients:", "\n", formatted_ids)

# Output and further processing
num_rows = final_filtered_df.shape[0]
print("Number of patients in the time range:", num_rows)

# Call the execute_query function to get the results from the Teradata database and save as a CSV file
query_results = database_queryback.execute_query(final_filtered_df, "io/results.csv")

# Use the query results for further processing or output
print("Report Data:", query_results)