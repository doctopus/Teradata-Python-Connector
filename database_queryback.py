import sqlalchemy as sa
import pandas as pd
import config

def execute_query(df, output_file):
    # Create the connection URL
    connection_url = f"teradatasql://{config.Teradata_Host}/"f"?user={config.Teradata_User}&password={config.Teradata_User_Password}&logmech=LDAP"

    # Connect to the Teradata database
    engine = sa.create_engine(connection_url)

    # Get the unique PAT_MRN_IDs from the filtered DataFrame
    pat_mrn_ids = df["PAT_MRN_ID"].tolist()

    # Convert the PAT_MRN_IDs to a string with comma-separated and quoted values
    pat_mrn_ids_str = ",".join(f"'{x}'" for x in pat_mrn_ids)

    # Write the SQL query with placeholders for the PAT_MRN_IDs
    query = f"""
    SELECT
        PAT_RACE_DESC, PAT_ETHNIC_GROUP_DESC, count(*)
    FROM
        IHAA_EDV.BK_PATIENT
    WHERE
        PAT_MRN_ID IN ({pat_mrn_ids_str})
    GROUP BY
        PAT_GENDER_DESC, PAT_RACE_DESC, PAT_ETHNIC_GROUP_DESC
    """

    # Execute the query and load the results into a pandas DataFrame
    results = pd.read_sql_query(query, engine)

    # Save the results as a CSV file with headers
    results.to_csv(output_file, index=False)

    # Return the results DataFrame (optional)
    return results
