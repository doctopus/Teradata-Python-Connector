import pandas as pd

def load_mrn_ids_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df
