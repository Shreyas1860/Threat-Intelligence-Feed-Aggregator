# Filename: query_threats.py

import sqlite3
import sys

DATABASE_NAME = 'threat_intelligence.db'

def query_indicator(indicator):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM threats WHERE indicator LIKE ?", ('%' + indicator + '%',))
    results = cursor.fetchall()
    conn.close()
    
    return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 query_threats.py <indicator_to_search>")
        sys.exit(1)
        
    indicator_to_search = sys.argv[1]
    
    print(f"[*] Searching for indicator: {indicator_to_search}")
    
    results = query_indicator(indicator_to_search)
    
    if results:
        print(f"[+] Found {len(results)} match(es)!")
        for row in results:
            print("-" * 20)
            print(f"  ID: {row[0]}")
            print(f"  Indicator: {row[1]}")
            print(f"  Type: {row[2]}")
            print(f"  Source: {row[3]}")
            print(f"  First Seen: {row[4]}")
            print(f"  Last Seen: {row[5]}")
    else:
        print("[-] No matches found in the database.")

if __name__ == "__main__":
    main()
