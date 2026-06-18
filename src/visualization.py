import matplotlib
matplotlib.use('Agg')  # Headless backend to prevent GUI display errors in scripts
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def create_visualizations(df, output_dir="output"):
    """
    Phase 7: Visualization
    Generates and saves four required analytics charts.
    """
    print("\n" + "="*50)
    print("PHASE 7: VISUALIZATION")
    print("="*50)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Modern theme styling setup
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = '#333333'
    plt.rcParams['axes.labelcolor'] = '#333333'
    plt.rcParams['xtick.color'] = '#333333'
    plt.rcParams['ytick.color'] = '#333333'
    
    # Define cohesive, harmonize color palette
    colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']
    
    # 1. Transaction Type Distribution -> Bar Chart
    print("Generating Chart 1: Transaction Type Distribution...")
    plt.figure(figsize=(8, 5))
    type_counts = df['type'].value_counts()
    
    bars = plt.bar(type_counts.index, type_counts.values, color='#3498db', edgecolor='#2980b9', width=0.6)
    plt.title('Transaction Count by Type', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Transaction Type', fontsize=12, labelpad=10)
    plt.ylabel('Number of Transactions', fontsize=12, labelpad=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Annotate bar heights
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height + (height * 0.01), f'{height:,}', ha='center', va='bottom', fontsize=9)
        
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "transaction_types.png")
    plt.savefig(chart1_path, dpi=150)
    plt.close()
    print(f"- Saved: {chart1_path}")
    
    # 2. Fraud vs Normal Transactions -> Pie Chart
    print("Generating Chart 2: Fraud vs Normal Transactions...")
    plt.figure(figsize=(6, 6))
    if 'fraud_flag' in df.columns:
        fraud_counts = df['fraud_flag'].value_counts()
    else:
        # Fallback to isFraud if fraud_flag not detected yet
        fraud_counts = df['isFraud'].value_counts()
        
    labels = ['Normal', 'Suspicious'] if 0 in fraud_counts.index else ['Suspicious', 'Normal']
    sizes = [fraud_counts.get(0, 0), fraud_counts.get(1, 0)]
    
    # Swap elements if sizes ordering differs
    if fraud_counts.index[0] == 1:
        labels = ['Suspicious', 'Normal']
        sizes = [fraud_counts.get(1, 0), fraud_counts.get(0, 0)]
        
    pie_colors = ['#2ecc71', '#e74c3c']
    plt.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=140, colors=pie_colors, 
            textprops={'fontsize': 11, 'weight': 'bold'}, explode=(0, 0.1) if sizes[1] > 0 else (0, 0))
    plt.title('Distribution of Suspicious vs Normal Transactions', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "fraud_vs_normal.png")
    plt.savefig(chart2_path, dpi=150)
    plt.close()
    print(f"- Saved: {chart2_path}")
    
    # 3. Transaction Amount Distribution -> Histogram
    print("Generating Chart 3: Transaction Amount Distribution...")
    plt.figure(figsize=(8, 5))
    
    # Plot using a log scale on the x-axis to accommodate transaction amount range (up to 90M)
    # Filter amounts > 0 for log log-scale hist
    amounts = df[df['amount'] > 0]['amount']
    
    # Generate log space bins
    bins = np.logspace(np.log10(amounts.min()), np.log10(amounts.max()), 50)
    
    plt.hist(amounts, bins=bins, color='#9b59b6', edgecolor='#8e44ad', alpha=0.85)
    plt.gca().set_xscale("log")
    plt.title('Distribution of Transaction Amounts (Log Scale)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Transaction Amount ($) - Log Scale', fontsize=12, labelpad=10)
    plt.ylabel('Frequency (Count)', fontsize=12, labelpad=10)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "amount_distribution.png")
    plt.savefig(chart3_path, dpi=150)
    plt.close()
    print(f"- Saved: {chart3_path}")
    
    # 4. Fraud By Transaction Type -> Bar Chart
    print("Generating Chart 4: Fraud By Transaction Type...")
    plt.figure(figsize=(8, 5))
    
    flag_col = 'fraud_flag' if 'fraud_flag' in df.columns else 'isFraud'
    fraud_df = df[df[flag_col] == 1]
    
    if not fraud_df.empty:
        fraud_by_type = fraud_df['type'].value_counts()
        bars = plt.bar(fraud_by_type.index, fraud_by_type.values, color='#e74c3c', edgecolor='#c0392b', width=0.5)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.title('Suspicious Transactions by Type', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Transaction Type', fontsize=12, labelpad=10)
        plt.ylabel('Number of Suspicious Transactions', fontsize=12, labelpad=10)
        
        # Add count labels above bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, height + (height * 0.01), f'{height:,}', ha='center', va='bottom', fontsize=10)
    else:
        plt.text(0.5, 0.5, 'No fraud transactions detected', ha='center', va='center', fontsize=14, color='gray')
        plt.title('Suspicious Transactions by Type', fontsize=14, fontweight='bold', pad=15)
        
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "fraud_by_type.png")
    plt.savefig(chart4_path, dpi=150)
    plt.close()
    print(f"- Saved: {chart4_path}")
    
    print("All visualizations created successfully.")
    print("="*50)

if __name__ == "__main__":
    from load_data import load_data
    from clean_data import clean_data
    from fraud_detection import detect_fraud
    df = load_data()
    df = clean_data(df)
    df = detect_fraud(df)
    create_visualizations(df)
