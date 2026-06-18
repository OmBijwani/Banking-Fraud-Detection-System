import pandas as pd
import os

def detect_fraud(df, output_path="output/fraud_transactions.csv"):
    """
    Phase 5: Fraud Detection
    Flags transactions as suspicious based on 4 defined rules:
    - Rule 1: amount > 200000
    - Rule 2: oldbalanceOrg == 0
    - Rule 3: newbalanceOrig == 0
    - Rule 4: type == "CASH_OUT" AND amount > 150000
    """
    print("\n" + "="*50)
    print("PHASE 5: FRAUD DETECTION")
    print("="*50)
    
    # 1. Create fraud_flag column
    print("Initializing fraud_flag column...")
    df['fraud_flag'] = 0
    
    # 2. Mark suspicious transactions based on rules
    print("Applying fraud detection rules...")
    
    rule1 = df['amount'] > 200000
    rule2 = df['oldbalanceOrg'] == 0
    rule3 = df['newbalanceOrig'] == 0
    rule4 = (df['type'] == 'CASH_OUT') & (df['amount'] > 150000)
    
    # Flag transactions if ANY of the rules are satisfied
    df.loc[rule1 | rule2 | rule3 | rule4, 'fraud_flag'] = 1
    
    # Print rule-specific statistics
    print(f"- Matches Rule 1 (amount > 200k): {rule1.sum():,}")
    print(f"- Matches Rule 2 (oldbalanceOrg == 0): {rule2.sum():,}")
    print(f"- Matches Rule 3 (newbalanceOrig == 0): {rule3.sum():,}")
    print(f"- Matches Rule 4 (CASH_OUT & amount > 150k): {rule4.sum():,}")
    
    # 3. Extract fraud transactions
    fraud_df = df[df['fraud_flag'] == 1]
    total_tx = len(df)
    total_fraud = len(fraud_df)
    print(f"\nSummary:")
    print(f"- Total Flagged Suspicious Transactions: {total_fraud:,} out of {total_tx:,} ({total_fraud/total_tx*100:.2f}%)")
    
    # 4. Save results
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"\nSaving flagged transactions to: {output_path}...")
    fraud_df.to_csv(output_path, index=False)
    print("Results saved successfully.")
    
    print("="*50)
    return df

if __name__ == "__main__":
    from load_data import load_data
    from clean_data import clean_data
    df = load_data()
    df = clean_data(df)
    df = detect_fraud(df)
