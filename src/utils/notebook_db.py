import sqlite3
import json
from datetime import datetime

DB_PATH = "src/notebook.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            spec_json TEXT,
            sources_json TEXT,
            params_json TEXT,
            updated_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_project(title: str, spec: dict, sources: list, params: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM projects WHERE title = ?', (title,))
    row = cursor.fetchone()
    now = datetime.now().isoformat()
    
    if row:
        cursor.execute('''
            UPDATE projects 
            SET spec_json = ?, sources_json = ?, params_json = ?, updated_at = ?
            WHERE title = ?
        ''', (json.dumps(spec), json.dumps(sources), json.dumps(params), now, title))
    else:
        cursor.execute('''
            INSERT INTO projects (title, spec_json, sources_json, params_json, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, json.dumps(spec), json.dumps(sources), json.dumps(params), now))
        
    conn.commit()
    conn.close()

def load_project(title: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT spec_json, sources_json, params_json FROM projects WHERE title = ?', (title,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "spec": json.loads(row[0]),
            "sources": json.loads(row[1]),
            "params": json.loads(row[2])
        }
    return None
