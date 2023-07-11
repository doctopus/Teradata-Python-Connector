import pandas as pd


def perform_data_wrangling(carisData, localData, tempusData, start_date, end_date):
    # Data wrangling operations for Caris

    # Select only the desired columns
    carisData = carisData.loc[:, ['EDV_Collection_Date', 'Caris_Collection_Date', 'PAT_MRN_ID']]

    # Convert the data type of PAT_MRN_ID column to str in both dataframes
    carisData['PAT_MRN_ID'] = carisData['PAT_MRN_ID'].astype(str)
    carisData['EDV_Collection_Date'] = pd.to_datetime(carisData['EDV_Collection_Date'])
    carisData['Caris_Collection_Date'] = pd.to_datetime(carisData['Caris_Collection_Date'])

    localData['PAT_MRN_ID'] = localData['PAT_MRN_ID'].astype(str)

    # Filter rows based on matching values in PAT_MRN_ID column
    carisData_matched = carisData[carisData['PAT_MRN_ID'].isin(localData['PAT_MRN_ID'])]

    # Filter rows based on the conditions
    caris_filtered_df = carisData_matched[
        (carisData_matched['EDV_Collection_Date'].apply(lambda x: isinstance(x, pd.Timestamp)) &
         carisData_matched['EDV_Collection_Date'].between(start_date, end_date)) |
        (~carisData_matched['EDV_Collection_Date'].apply(lambda x: isinstance(x, pd.Timestamp)) &
         carisData_matched['Caris_Collection_Date'].between(start_date, end_date))
        ]
    caris_filtered_df.loc[:, ['Vendor']] = 'Caris'
    # Data wrangling operations for Tempus-----
    # Select only the desired columns
    tempusData = tempusData.loc[:, ['EDV_Collection_Date', 'Tempus_Collection_Date', 'PAT_MRN_ID']]

    # Convert the data type of PAT_MRN_ID column to str in both dataframes
    tempusData['PAT_MRN_ID'] = tempusData['PAT_MRN_ID'].astype(str)
    tempusData['EDV_Collection_Date'] = pd.to_datetime(tempusData['EDV_Collection_Date'])
    tempusData['Tempus_Collection_Date'] = pd.to_datetime(tempusData['Tempus_Collection_Date'])

    # Filter rows based on the conditions
    tempus_filtered_df = tempusData[
        (tempusData['EDV_Collection_Date'].apply(lambda x: isinstance(x, pd.Timestamp)) &
         tempusData['EDV_Collection_Date'].between(start_date, end_date)) |
        (~tempusData['EDV_Collection_Date'].apply(lambda x: isinstance(x, pd.Timestamp)) &
         tempusData['Tempus_Collection_Date'].between(start_date, end_date))
        ]
    tempus_filtered_df.loc[:, ['Vendor']] = 'Tempus'

    final_filtered_df = pd.concat(
        [caris_filtered_df[['Vendor', 'PAT_MRN_ID']], tempus_filtered_df[['Vendor', 'PAT_MRN_ID']]])

    # Since some rows of Tempus have MRN as None, filtering those out
    final_filtered_df = final_filtered_df[final_filtered_df['PAT_MRN_ID'] != 'None']

    # Removing Duplicates in the PAT_MRN_ID Field in the combined list
    final_filtered_df.drop_duplicates(subset='PAT_MRN_ID', inplace=True)

    # Reset the index of the final dataframe
    final_filtered_df.reset_index(drop=True, inplace=True)

    return final_filtered_df
