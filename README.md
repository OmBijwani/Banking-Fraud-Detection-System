# Banking Fraud Detection System

## Overview

A rule-based Banking Fraud Detection System built using Python, Pandas, NumPy, Matplotlib, and SQLite. The project analyzes banking transactions, identifies suspicious activities using predefined fraud rules, and generates reports and visualizations.

## Features

- Data loading and cleaning
- SQLite database integration
- SQL-based transaction analytics
- Rule-based fraud detection
- Fraud reporting
- Data visualization

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- SQLite

## Project Structure

```text
Banking-Fraud-Detection-System/

├── data/
├── database/
├── output/
├── src/
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Fraud Detection Rules

Transactions are flagged as suspicious if:

- Amount > 200,000
- Sender balance is 0 before transaction
- Sender balance becomes 0 after transaction
- CASH_OUT transaction amount > 150,000

## Installation

```bash
git clone <repository-url>
cd Banking-Fraud-Detection-System

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

## Running the Project

```bash
python main.py
```

## Outputs

The project generates:

- Fraud transaction report (`fraud_transactions.csv`)
- Summary report (`reports.txt`)
- Transaction visualizations (`.png` files)

## Learning Outcomes

- Data Cleaning with Pandas
- Data Analysis with NumPy
- SQLite Database Management
- Rule-Based Fraud Detection
- Data Visualization with Matplotlib