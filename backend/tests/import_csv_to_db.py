import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import csv
import sqlite3
from config import DB_PATH

CSV_DIR = os.path.join(os.path.dirname(__file__), '..', 'exports')
VERSIONES = ["0.1.0", "0.2.0", "0.3.0", "0.4.0"]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executescript("""
    CREATE TABLE IF NOT EXISTS keys (
        key_id INTEGER PRIMARY KEY AUTOINCREMENT,
        value TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        algorithm_version TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS nist_results (
        result_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        algorithm_version TEXT NOT NULL,
        sample_size INTEGER NOT NULL,
        p_values TEXT NOT NULL,
        passed_tests TEXT NOT NULL,
        notes TEXT
    );
    CREATE TABLE IF NOT EXISTS shannon_results (
        result_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        algorithm_version TEXT NOT NULL,
        sample_size INTEGER NOT NULL,
        shannon REAL NOT NULL,
        notes TEXT
    );
""")
conn.commit()

for version in VERSIONES:
    filename = f"claves_{version}.csv"
    filepath = os.path.join(CSV_DIR, filename)

    if not os.path.exists(filepath):
        print(f"  [SKIP] {filename} — no encontrado")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filas = list(reader)

    print(f"  Importando {len(filas)} claves de {filename}...")

    cursor.executemany(
        "INSERT INTO keys (value, timestamp, algorithm_version) VALUES (?, datetime('now'), ?)",
        [(fila["value"], version) for fila in filas]
    )
    conn.commit()
    print(f"  ✓ {len(filas)} claves importadas para versión {version}")

conn.close()
print("\nImportación completada.")