from dotenv import load_dotenv
import os

load_dotenv()

Teradata_Host = os.getenv("TERADATA_HOST")
Teradata_User = os.getenv("TERADATA_USER")
Teradata_User_Password = os.getenv("TERADATA_USER_PASSWORD")

# Other configuration variables/constants
