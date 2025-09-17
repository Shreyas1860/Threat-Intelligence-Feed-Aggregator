# Filename: threat_aggregator.py

import sqlite3
import requests
import datetime

DATABASE_NAME = 'threat_intelligence.db'
THREAT_FEEDS = {
    "abuse.ch_feodotracker_ips": {
        "url": "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
        "type": "ipv4"
    },
    "abuse.ch_urlhaus_domains": {
        "url": "https://urlhaus.abuse.ch/downloads/text_online/",
        "type": "domain"
    }
}

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY,
            indicator TEXT UNIQUE,
            type TEXT,
            source TEXT,
            first_seen TEXT,
            last_seen TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def fetch_feed(source_name, url):
    try:
        print(f"[*] Fetching data from {source_name}...")
        headers = {'User-Agent': 'ThreatAggregator/1.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        indicators = [line for line in lines if line.strip() and not line.startswith('#')]
        
        print(f"[+] Found {len(indicators)} indicators from {source_name}.")
        return indicators
        
    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching feed {source_name}: {e}")
        return []

def update_database(indicators, source_name, indicator_type):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    new_indicators_count = 0
    now = datetime.datetime.now().isoformat()

    for indicator in indicators:
        cursor.execute("SELECT id FROM threats WHERE indicator = ?", (indicator,))
        result = cursor.fetchone()
        
        if result:
            cursor.execute("UPDATE threats SET last_seen = ? WHERE indicator = ?", (now, indicator))
        else:
            cursor.execute(
                "INSERT INTO threats (indicator, type, source, first_seen, last_seen) VALUES (?, ?, ?, ?, ?)",
                (indicator, indicator_type, source_name, now, now)
            )
            new_indicators_count += 1
            
    conn.commit()
    conn.close()
    print(f"[+] Database updated for {source_name}. Added {new_indicators_count} new indicators.")

def main():
    init_db()
    for name, feed_info in THREAT_FEEDS.items():
        indicators = fetch_feed(name, feed_info['url'])
        if indicators:
            update_database(indicators, name, feed_info['type'])

if __name__ == "__main__":
    main()
