def perform_data_wrangling(magicData, localData, start_date, end_date):
    # Data wrangling operations

    # Select only the desired columns
    magicData = magicData.loc[:, ['EDV_Collection_Date', 'Caris_Collection_Date', 'PAT_MRN_ID']]

    # Convert the data type of PAT_MRN_ID column to str in both dataframes
    magicData['PAT_MRN_ID'] = magicData['PAT_MRN_ID'].astype(str)
    localData['PAT_MRN_ID'] = localData['PAT_MRN_ID'].astype(str)

    # Filter rows based on matching values in PAT_MRN_ID column
    filtered_df = magicData[magicData['PAT_MRN_ID'].isin(localData['PAT_MRN_ID'])]

    # Filter rows based on the conditions
    final_filtered_df = filtered_df[(filtered_df['EDV_Collection_Date'].between(start_date, end_date)) |
                                    ((filtered_df['EDV_Collection_Date'].isnull() |
                                      filtered_df['EDV_Collection_Date'].isna() |
                                      filtered_df['EDV_Collection_Date'] == 'None') &
                                     filtered_df['Caris_Collection_Date'].between(start_date, end_date))]

    return final_filtered_df
