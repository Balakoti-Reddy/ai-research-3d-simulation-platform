import sqlite3
import json

DB_NAME = "research_notebook.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            spec TEXT,
            sources TEXT,
            params TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_project(title, spec, sources, params):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO projects (title, spec, sources, params)
        VALUES (?, ?, ?, ?)
    ''', (title, json.dumps(spec), json.dumps(sources), json.dumps(params)))
    conn.commit()
    conn.close()
