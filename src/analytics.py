import sqlite3
import pandas as pd
import os

def run_sql_analytics(db_path="database/banking.db"):
    """
    Phase 4: SQL Analytics
    Runs specific SQL queries on the sqlite table.
    """
    print("\n" + "="*50)
    print("PHASE 4: SQL ANALYTICS")
    print("="*50)
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at: {db_path}")
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Executing analytics queries on 'transactions' table...")
        
        # 1. Total Transactions
        cursor.execute("SELECT COUNT(*) FROM transactions")
        total_tx = cursor.fetchone()[0]
        
        # 2. Total Transaction Amount
        cursor.execute("SELECT SUM(amount) FROM transactions")
        total_amount = cursor.fetchone()[0]
        
        # 3. Average Transaction Amount
        cursor.execute("SELECT AVG(amount) FROM transactions")
        avg_amount = cursor.fetchone()[0]
        
        # 4. Transaction Type Distribution
        cursor.execute("""
            SELECT type, COUNT(*), SUM(amount), AVG(amount) 
            FROM transactions 
            GROUP BY type
            ORDER BY COUNT(*) DESC
        """)
        type_dist = cursor.fetchall()
        
        # 5. Top 10 Largest Transactions
        cursor.execute("""
            SELECT step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest
            FROM transactions 
            ORDER BY amount DESC 
            LIMIT 10
        """)
        top_10 = cursor.fetchall()
        
        # Output reports
        print("\n=== Analytics Summary ===")
        print(f"Total Transactions: {total_tx:,}")
        print(f"Total Transaction Amount: {total_amount:,.2f}")
        print(f"Average Transaction Amount: {avg_amount:,.2f}")
        
        print("\n=== Transaction Statistics (Type Distribution) ===")
        print(f"{'Type':<12} | {'Count':<12} | {'Total Amount':<20} | {'Avg Amount':<15}")
        print("-" * 68)
        for row in type_dist:
            t_name, count, t_sum, t_avg = row
            print(f"{t_name:<12} | {count:<12,} | {t_sum:<20,.2f} | {t_avg:<15,.2f}")
            
        print("\n=== Top 10 Largest Transactions ===")
        print(f"{'Step':<5} | {'Type':<10} | {'Amount':<15} | {'From':<12} | {'To':<12}")
        print("-" * 62)
        for row in top_10:
            step, t_type, amt, orig, old_orig, new_orig, dest, old_dest, new_dest = row
            print(f"{step:<5} | {t_type:<10} | {amt:<15,.2f} | {orig:<12} | {dest:<12}")
            
    except Exception as e:
        print(f"Error executing SQL queries: {e}")
        raise e
    finally:
        conn.close()
        
    print("="*50)


def generate_fraud_report(df, report_path="output/reports.txt"):
    """
    Phase 6: Fraud Analytics
    Generates a text report of fraud statistics and saves it to a file.
    """
    print("\n" + "="*50)
    print("PHASE 6: FRAUD ANALYTICS")
    print("="*50)
    
    if 'fraud_flag' not in df.columns:
        raise ValueError("DataFrame does not contain the 'fraud_flag' column. Run fraud detection first.")
        
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    # Calculate statistics
    total_tx = len(df)
    fraud_tx = int(df['fraud_flag'].sum())
    fraud_pct = (fraud_tx / total_tx) * 100 if total_tx > 0 else 0.0
    
    # Fraud by transaction type
    fraud_df = df[df['fraud_flag'] == 1]
    if not fraud_df.empty:
        fraud_by_type = fraud_df['type'].value_counts()
        most_common_type = fraud_by_type.index[0]
    else:
        fraud_by_type = pd.Series(dtype=int)
        most_common_type = "NONE"
        
    # Print statistics
    print(f"Total Transactions: {total_tx:,}")
    print(f"Fraud Transactions: {fraud_tx:,}")
    print(f"Fraud Percentage: {fraud_pct:.2f}%")
    print(f"Most Common Fraud Type: {most_common_type}")
    
    print("\nFraud Transactions by Type:")
    if not fraud_df.empty:
        for t_type, count in fraud_by_type.items():
            print(f"- {t_type}: {count:,}")
    else:
        print("- None")
        
    # Generate the formatted report text matching the example template
    report_content = f"""BANKING FRAUD REPORT

Total Transactions: {total_tx}
Fraud Transactions: {fraud_tx}
Fraud Percentage: {fraud_pct:.2f}%
Most Common Fraud Type: {most_common_type}
"""
    
    with open(report_path, 'w') as f:
        f.write(report_content)
        
    print(f"\nReport saved successfully to: {report_path}")
    print("="*50)


if __name__ == "__main__":
    # Test execution for SQL analytics (if database exists)
    try:
        run_sql_analytics()
    except Exception as e:
        print(f"Could not run SQL analytics check: {e}")
