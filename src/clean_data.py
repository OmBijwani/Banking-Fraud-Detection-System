import pandas as pd

def check_missing_values(df):
    """
    Checks for missing values in the DataFrame.
    Returns the count of missing values per column.
    """
    missing_report = df.isnull().sum()
    print("\nMissing Values Report:")
    for col, count in missing_report.items():
        print(f"- {col}: {count} missing value(s)")
    return missing_report

def check_duplicates(df):
    """
    Checks for duplicate rows in the DataFrame.
    Returns the total duplicate count.
    """
    duplicate_count = df.duplicated().sum()
    print(f"\nDuplicate Records Report:")
    print(f"- Total Duplicate Rows: {duplicate_count}")
    return duplicate_count

def check_negative_amounts(df):
    """
    Checks for negative transaction amounts.
    Returns the total count of rows with negative amount.
    """
    # Verify amount column is present
    if 'amount' in df.columns:
        negative_count = (df['amount'] < 0).sum()
    else:
        negative_count = 0
    print(f"\nTransaction Amount Validation:")
    print(f"- Rows with negative amounts: {negative_count}")
    return negative_count

def clean_data(df):
    """
    Phase 2: Data Cleaning
    Executes checks, cleans duplicate records, and returns the cleaned DataFrame.
    """
    print("\n" + "="*50)
    print("PHASE 2: DATA CLEANING")
    print("="*50)
    
    # 1. Missing values report
    check_missing_values(df)
    
    # 2. Duplicate records report
    dup_count = check_duplicates(df)
    
    # 3. Negative amount check
    check_negative_amounts(df)
    
    # 4. Verify data types
    print("\nData Type Verification:")
    print(df.dtypes)
    
    # 5. Remove duplicates if found
    if dup_count > 0:
        print(f"\nRemoving {dup_count} duplicate records...")
        df = df.drop_duplicates().reset_index(drop=True)
        print("Duplicates removed successfully.")
    else:
        print("\nNo duplicates found. No cleaning needed.")
        
    print("\nData Quality Report: All checks completed successfully.")
    print("="*50)
    return df

if __name__ == "__main__":
    # Test execution
    from load_data import load_data
    df = load_data()
    clean_data(df)
