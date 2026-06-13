# PURPOSE: This file contains the function responsible for loading the PaySim dataset into a Pandas DataFrame.

import pandas as pd

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded successfully.")
        return df

    except FileNotFoundError:
        print("Error: Dataset file not found.")

    except Exception as e:
        print(f"Unexpected Error: {e}")