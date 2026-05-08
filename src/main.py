import json
import csv
import os
from collections import Counter
from datetime import datetime
import mysql.connector
from mysql.connector import Error

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_data(data):
    cleaned = []
    for row in data:
        user_id = row.get("user_id")
        message = row.get("message")
        
        # Check user_id
        if user_id is None or str(user_id).strip() == "":
            continue
            
        # Check message
        if message is None or str(message).strip() == "":
            continue
            
        row["message"] = str(message).strip()
        cleaned.append(row)
        
    return cleaned

def classify_messages(data):
    # Order of categories defines priority in case of conflict.
    # First match wins. We're looking for simple substring matches as per assignment.
    
    categories = {
        "grant_search": ["grant", "funding", "deadline", "scholarship"],
        "report_request": ["report", "file", "send again", "document"],
        "general_question": ["how", "what", "can you", "where", "why"]
    }
    
    for row in data:
        msg_lower = row["message"].lower()
        assigned_category = "unknown"
        
        for cat, keywords in categories.items():
            if any(kw in msg_lower for kw in keywords):
                assigned_category = cat
                break # Conflict resolution: First match wins
                
        row["category"] = assigned_category
        
    return data

def save_to_csv(data, filepath):
    if not data:
        return
    keys = ["user_id", "message", "created_at", "channel", "category"]
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)

def save_summary_report(data, filepath):
    total_valid = len(data)
    cat_counts = Counter(row["category"] for row in data)
    channel_counts = Counter(row.get("channel", "unknown") for row in data)
    user_counts = Counter(row["user_id"] for row in data)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=== Summary Report ===\n\n")
        f.write(f"Total valid messages: {total_valid}\n\n")
        
        f.write("--- Count per Category ---\n")
        for k, v in cat_counts.most_common():
            f.write(f"{k}: {v}\n")
            
        f.write("\n--- Count per Channel ---\n")
        for k, v in channel_counts.most_common():
            f.write(f"{k}: {v}\n")
            
        f.write("\n--- Count per User ---\n")
        for k, v in user_counts.most_common():
            f.write(f"{k}: {v}\n")

def insert_to_mysql(data):

    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "3306")
    db_name = os.environ.get("DB_NAME", "test_db") 
    db_user = os.environ.get("DB_USER", "root")
    db_password = os.environ.get("DB_PASSWORD", "")
    
    # We need to create the table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS classified_messages (
        id           INT AUTO_INCREMENT PRIMARY KEY,
        user_id      VARCHAR(50)  NOT NULL,
        message      TEXT         NOT NULL,
        created_at   TIMESTAMP    NOT NULL,
        channel      VARCHAR(50)  NOT NULL,
        category     VARCHAR(50)  NOT NULL,
        processed_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    insert_query = """
    INSERT INTO classified_messages (user_id, message, created_at, channel, category)
    VALUES (%s, %s, %s, %s, %s)
    """

    try:
        connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            
            records_to_insert = [
                (r["user_id"], r["message"], r["created_at"], r.get("channel", "unknown"), r["category"])
                for r in data
            ]
            
            cursor.executemany(insert_query, records_to_insert)
            connection.commit()
            print(f"Successfully inserted {cursor.rowcount} records into MySQL table 'classified_messages'.")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'messages.json')
    csv_out_path = os.path.join(base_dir, 'output', 'classified_messages.csv')
    report_out_path = os.path.join(base_dir, 'output', 'summary_report.txt')
    
    if not os.path.exists(data_path):
        print(f"File not found: {data_path}")
        return
        
    print("Loading data...")
    raw_data = load_data(data_path)
    
    print("Cleaning data...")
    cleaned_data = clean_data(raw_data)
    
    print("Classifying messages...")
    classified_data = classify_messages(cleaned_data)
    
    print("Saving to CSV...")
    save_to_csv(classified_data, csv_out_path)
    
    print("Saving summary report...")
    save_summary_report(classified_data, report_out_path)
    
    # Try inserting to database
    try:
        from dotenv import load_dotenv
        env_path = os.path.join(base_dir, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
    except ImportError:
        pass
        
    print("Attempting to insert to MySQL...")
    insert_to_mysql(classified_data)
    print("Process complete.")

if __name__ == "__main__":
    main()
