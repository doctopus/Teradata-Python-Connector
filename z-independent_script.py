# This independent script only produces result for Caris Data.
# This is Proof of Concept only; Don't use for final reporting.
# The main.py script combines tempus and caris. Use Main Script.
import sqlalchemy as sa
import pandas as pd


# Define the date range as a datetime.date object
start_date = pd.to_datetime('2022-08-01').date()
end_date = pd.to_datetime('2023-05-31').date()


def main():
    # Connection details
    Teradata_Host = "tdprod1.ccf.org"
    Teradata_User = "beherat2"
    Teradata_User_Password = "Dev@nodejs01"

    # Create the connection URL
    connection_url = f"teradatasql://{Teradata_Host}/"f"?user={Teradata_User}&password={Teradata_User_Password}&logmech=LDAP"

    # Connect to the Teradata database
    engine = sa.create_engine(connection_url)

    # Table and schema details
    table_name = "CASE_META_CARIS_FIREHOSE"
    schema_name = "DL_MAGIC_PROD"

    # Query the table and load data into a pandas DataFrame
    query = f"SELECT * FROM {schema_name}.{table_name}"
    CASE_META_CARIS_FIREHOSE = pd.read_sql_query(query, engine)

    MRN_IDs = pd.read_excel('~/Desktop/MRNs.xlsx')

    # print(MRN_IDs.head())

    # Select only the desired columns
    CASE_META_CARIS_FIREHOSE = CASE_META_CARIS_FIREHOSE.loc[:,
                               ['EDV_Collection_Date', 'Caris_Collection_Date', 'PAT_MRN_ID']]

    # Print the updated dataframe to verify the modification
    print(CASE_META_CARIS_FIREHOSE.head())

    # Convert the data type of PAT_MRN_ID column to str in both dataframes
    CASE_META_CARIS_FIREHOSE['PAT_MRN_ID'] = CASE_META_CARIS_FIREHOSE['PAT_MRN_ID'].astype(str)
    MRN_IDs['PAT_MRN_ID'] = MRN_IDs['PAT_MRN_ID'].astype(str)

    # Filter rows based on matching values in PAT_MRN_ID column
    filtered_df = CASE_META_CARIS_FIREHOSE[CASE_META_CARIS_FIREHOSE['PAT_MRN_ID'].isin(MRN_IDs['PAT_MRN_ID'])]

    # Filter rows based on the conditions
    final_filtered_df = filtered_df[(filtered_df['EDV_Collection_Date'].between(start_date, end_date)) |
                                    ((filtered_df['EDV_Collection_Date'].isnull() |
                                      filtered_df['EDV_Collection_Date'].isna() |
                                      filtered_df['EDV_Collection_Date'] == 'None') &
                                     filtered_df['Caris_Collection_Date'].between(start_date, end_date))]

    # Print the filtered dataframe
    print(final_filtered_df.head())
    num_rows = final_filtered_df.shape[0]
    print("Number of patients in the time range:", num_rows)
    pat_mrn_ids = final_filtered_df["PAT_MRN_ID"].tolist()
    # Create the formatted string
    formatted_ids = ""
    for i, id_value in enumerate(pat_mrn_ids):
        formatted_ids += f"'{id_value}'"
        if i < len(pat_mrn_ids) - 1:
            formatted_ids += ",\n"

    # Print the formatted string
    print(formatted_ids)

    # Write the SQL query with placeholders for the PAT_MRN_IDs
    query = f"""
        SELECT
            PAT_RACE_DESC, PAT_ETHNIC_GROUP_DESC, count(*)
        FROM
            IHAA_EDV.BK_PATIENT
        WHERE
            PAT_MRN_ID IN ({formatted_ids})
        GROUP BY
            PAT_GENDER_DESC, PAT_RACE_DESC, PAT_ETHNIC_GROUP_DESC
        """

    # Execute the query and load the results into a pandas DataFrame
    results = pd.read_sql_query(query, engine)

    # Return the results DataFrame (optional)
    print("Report Data:", "\n", results)


if __name__ == "__main__":
    main()
