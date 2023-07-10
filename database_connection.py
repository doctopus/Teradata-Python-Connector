import sqlalchemy as sa
import pandas as pd
import config


def connect_and_fetch_table(table_name, schema_name):
    # Teradata_Host = os.getenv("TERADATA_HOST")
    # Teradata_User = os.getenv("TERADATA_USER")
    # Teradata_User_Password = os.getenv("TERADATA_USER_PASSWORD")

    # Create the connection URL
    # connection_url = f"teradatasql://{Teradata_Host}/"f"?user={Teradata_User}&password={Teradata_User_Password}&logmech=LDAP"
    connection_url = f"teradatasql://{config.Teradata_Host}/"f"?user={config.Teradata_User}&password={config.Teradata_User_Password}&logmech=LDAP"

    # Connect to the Teradata database
    engine = sa.create_engine(connection_url)

    # Query the table and load data into a pandas DataFrame
    query = f"SELECT * FROM {schema_name}.{table_name}"
    df = pd.read_sql_query(query, engine)

    return df
