import sqlite3
import os
import pandas as pd

def create_database(df, db_path="database/banking.db", table_name="transactions"):
    """
    Phase 3: SQLite Database Creation and Storage
    Saves the cleaned DataFrame into an SQLite database.
    """
    print("\n" + "="*50)
    print("PHASE 3: SQLITE DATABASE")
    print("="*50)
    
    # 1. Create database directory if it doesn't exist
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        
    print(f"Creating database connection to: {db_path}")
    conn = sqlite3.connect(db_path)
    
    try:
        print(f"Storing DataFrame in SQL table: '{table_name}'...")
        # Write the dataframe in chunks to prevent memory overhead
        df.to_sql(table_name, conn, if_exists='replace', index=False, chunksize=200000)
        print("Data Inserted Successfully.")
        
        # Verify inserted row count
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        print(f"Verification: Inserted Row Count in '{table_name}' table = {row_count}")
        
        # Create search indexes on account ID fields
        print("Creating indexes on 'nameOrig' and 'nameDest' for optimized search queries...")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_nameOrig ON {table_name}(nameOrig);")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_nameDest ON {table_name}(nameDest);")
        
        # Output confirmation message
        print("\nDatabase Created and Indexed.")
        print("Table Created.")
        
    except Exception as e:
        print(f"Error during SQLite operations: {e}")
        raise e
    finally:
        conn.close()
        print("SQLite connection closed.")
        
    print("="*50)

if __name__ == "__main__":
    from load_data import load_data
    from clean_data import clean_data
    df = load_data()
    df = clean_data(df)
    create_database(df)
