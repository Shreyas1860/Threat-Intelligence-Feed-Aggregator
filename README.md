# Threat Intelligence Feed Aggregator 🛡️

A Python-based tool to automatically download, process, and store threat intelligence data from various open-source feeds. This project creates a local, queryable database of malicious indicators, such as IPs and domains, for security analysis and research.

This tool is a foundational element for many defensive security operations, allowing for quick checks against known malicious entities.



---
## ✨ Features

* **Feed Aggregation**: Pulls data from multiple open-source threat intelligence feeds.
* **Local Database**: Stores indicators in a local SQLite database for fast, offline querying.
* **Deduplication**: Automatically handles duplicate entries and updates timestamps for recurring indicators.
* **Indicator Types**: Currently supports malicious IPv4 addresses and domains.
* **Query Interface**: Includes a simple command-line tool to search the local database.

---
## 🛠️ Setup & Usage

### 1. Prerequisites
* Python 3
* The `requests` library

### 2. Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/your_username/your_repository.git](https://github.com/your_username/your_repository.git)
    cd your_repository
    ```
2.  Install the required library:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Populating the Database
Before you can query anything, you must run the aggregator to download the threat feeds and build your local database.
```bash
python3 threat_aggregator.py
