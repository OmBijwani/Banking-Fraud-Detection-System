import os
import sys
import time
import http.server
import socketserver
import urllib.parse
import json
import sqlite3
import mimetypes
from src.load_data import load_data
from src.clean_data import clean_data
from src.database import create_database
from src.analytics import run_sql_analytics, generate_fraud_report
from src.fraud_detection import detect_fraud
from src.visualization import create_visualizations

PORT = 8000
DB_PATH = "database/banking.db"

def init_database_indexes():
    """Create indexes on search columns to enable instant search queries."""
    if not os.path.exists(DB_PATH):
        print(f"Warning: Database file not found at {DB_PATH}. Run pipeline first.")
        return

    print("Checking database indexes...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Check if indexes exist
        cursor.execute("PRAGMA index_list(transactions)")
        indexes = cursor.fetchall()
        index_names = [idx[1] for idx in indexes]
        
        has_orig = "idx_transactions_nameOrig" in index_names
        has_dest = "idx_transactions_nameDest" in index_names
        has_type = "idx_transactions_type" in index_names
        has_amount = "idx_transactions_amount" in index_names
        
        if not (has_orig and has_dest and has_type and has_amount):
            print("Optimizing database: Creating search indexes on 6+ million records...")
            print("This is a one-time operation and may take 10-20 seconds. Please wait...")
            
            if not has_orig:
                print("- Indexing nameOrig...")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_nameOrig ON transactions(nameOrig);")
            if not has_dest:
                print("- Indexing nameDest...")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_nameDest ON transactions(nameDest);")
            if not has_type:
                print("- Indexing type...")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);")
            if not has_amount:
                print("- Indexing amount...")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_amount ON transactions(amount);")
            
            conn.commit()
            print("Database optimization complete! Instant search enabled.")
        else:
            print("Database indexes verified. Instant search is active.")
    except Exception as e:
        print(f"Error checking/creating database indexes: {e}")
    finally:
        conn.close()

class DashboardRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow CORS for ease of use
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # Parse the URL path
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/api/search":
            self.handle_api_search(parsed_url.query)
        else:
            # Fallback to serving static files
            if path == "/":
                self.path = "/index.html"
            super().do_GET()

    def handle_api_search(self, query_string):
        params = urllib.parse.parse_qs(query_string)
        q = params.get('q', [''])[0].strip()
        
        if not q or len(q) < 2:
            self.send_json_response({"results": [], "query": q, "message": "Search query too short. Enter at least 2 characters."})
            return

        if not os.path.exists(DB_PATH):
            self.send_json_response({"results": [], "query": q, "error": "Database not found. Please run main.py first."})
            return

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # Enable case-sensitive LIKE searches so SQLite can translate them into efficient range scans
            cursor.execute("PRAGMA case_sensitive_like = ON;")
            
            q_clean = q.upper()
            conditions = []
            query_params = []
            
            # Smart parser: selectively query columns to fully leverage database indexes
            if q_clean.startswith('C') or q_clean.startswith('M'):
                conditions.append("nameOrig LIKE ?")
                conditions.append("nameDest LIKE ?")
                query_params.extend([q_clean + "%", q_clean + "%"])
            elif q_clean in ["TRANSFER", "CASH_OUT", "CASH_IN", "PAYMENT", "DEBIT"]:
                conditions.append("type = ?")
                query_params.append(q_clean)
            else:
                # Check if it could be a transaction amount
                try:
                    val = float(q_clean)
                    conditions.append("amount = ?")
                    query_params.append(val)
                except ValueError:
                    # Fallback to general prefix search
                    conditions.append("nameOrig LIKE ?")
                    conditions.append("nameDest LIKE ?")
                    query_params.extend([q_clean + "%", q_clean + "%"])
            
            sql_query = f"""
                SELECT step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, 
                       nameDest, oldbalanceDest, newbalanceDest, isFraud
                FROM transactions
                WHERE {" OR ".join(conditions)}
                LIMIT 50
            """
            
            cursor.execute(sql_query, query_params)
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    "step": row["step"],
                    "type": row["type"],
                    "amount": row["amount"],
                    "nameOrig": row["nameOrig"],
                    "oldbalanceOrg": row["oldbalanceOrg"],
                    "newbalanceOrig": row["newbalanceOrig"],
                    "nameDest": row["nameDest"],
                    "oldbalanceDest": row["oldbalanceDest"],
                    "newbalanceDest": row["newbalanceDest"],
                    "isFraud": row["isFraud"]
                })
                
            self.send_json_response({
                "results": results,
                "query": q,
                "count": len(results)
            })
            
        except Exception as e:
            self.send_json_response({
                "results": [],
                "query": q,
                "error": f"Database search error: {str(e)}"
            }, status=500)
        finally:
            conn.close()

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        response_bytes = json.dumps(data).encode('utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

def run_server():
    # Make sure MIME types are correctly registered for CSS and JS
    mimetypes.init()
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('text/html', '.html')
    mimetypes.add_type('application/javascript', '.js')

    init_database_indexes()
    
    handler = DashboardRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"\n=======================================================")
        print(f"Banking Fraud Detection Dashboard Server Started!")
        print(f"Open your browser and navigate to: http://localhost:{PORT}")
        print(f"Press Ctrl+C to stop the server.")
        print(f"=======================================================\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

def main():
    print("="*60)
    print("STARTING BANKING FRAUD DETECTION SYSTEM PIPELINE")
    print("="*60)
    
    start_time = time.time()
    
    # Define paths
    csv_path = "data/transactions.csv"
    fraud_csv_path = "output/fraud_transactions.csv"
    report_path = "output/reports.txt"
    output_dir = "output"
    
    # Phase 1: Load Data
    df = load_data(csv_path)
    
    # Phase 2: Clean Data
    df = clean_data(df)
    
    # Phase 3: Create SQLite Database
    create_database(df, db_path=DB_PATH)
    
    # Phase 4: Run SQL Analytics
    run_sql_analytics(db_path=DB_PATH)
    
    # Phase 5: Detect Fraud
    df = detect_fraud(df, output_path=fraud_csv_path)
    
    # Phase 6: Generate Report (Fraud Analytics)
    generate_fraud_report(df, report_path=report_path)
    
    # Phase 7: Create Visualizations
    create_visualizations(df, output_dir=output_dir)
    
    end_time = time.time()
    elapsed = end_time - start_time
    print("\n" + "="*60)
    print(f"PIPELINE COMPLETED SUCCESSFULLY in {elapsed:.2f} seconds!")
    print(f"All outputs generated in '{output_dir}/' folder.")
    print("="*60)
    
    # Automatically launch dashboard server at the end of pipeline execution
    print("\nStarting the Dashboard Web Server...")
    run_server()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        run_server()
    else:
        main()
