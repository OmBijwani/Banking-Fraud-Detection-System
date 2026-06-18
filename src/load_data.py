import pandas as pd
import os

def load_data(file_path="data/transactions.csv"):
    """
    Phase 1: Data Loading
    Loads banking transaction dataset and displays basic information.
    """
    print("\n" + "="*50)
    print("PHASE 1: DATA LOADING")
    print("="*50)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")
        
    print(f"Reading dataset from: {file_path}...")
    df = pd.read_csv(file_path)
    
    # Display shape
    rows, cols = df.shape
    print(f"\nDataset Shape:")
    print(f"- Total Rows: {rows}")
    print(f"- Total Columns: {cols}")
    
    # Display column names
    print(f"\nColumn Names:")
    print(list(df.columns))
    
    # Display first 5 rows
    print(f"\nDataset Preview (First 5 rows):")
    print(df.head())
    
    # Display data types
    print(f"\nData Types:")
    print(df.dtypes)
    
    print("="*50)
    return df

if __name__ == "__main__":
    load_data()
