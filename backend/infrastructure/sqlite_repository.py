import sqlite3
from datetime import datetime
from domain.key import Key
from domain.analysis_result import AnalysisResult
from config import DB_PATH

class SQLiteRepository:

    def __init__(self):
        self.db_path = DB_PATH
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()
        print("Base de datos conectada: " + self.db_path)

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keys (
                key_id TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                algorithm_version TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                result_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                algorithm_version TEXT NOT NULL,
                sample_size INTEGER NOT NULL,
                p_values TEXT NOT NULL,
                passed_tests TEXT NOT NULL,
                notes TEXT
            )
        """)
        self.conn.commit()

    def save_key(self, key):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO keys (key_id, value, timestamp, algorithm_version)
            VALUES (?, ?, ?, ?)
        """, (
            key.key_id,
            key.value,
            key.timestamp.isoformat(),
            key.algorithm_version
        ))
        self.conn.commit()

    def get_all_keys(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT key_id, value, timestamp, algorithm_version FROM keys")
        rows = cursor.fetchall()
        keys = []
        for row in rows:
            keys.append(Key(
                key_id=row[0],
                value=row[1],
                timestamp=datetime.fromisoformat(row[2]),
                algorithm_version=row[3]
            ))
        return keys

    def save_result(self, result):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO analysis_results 
            (result_id, timestamp, algorithm_version, sample_size, p_values, passed_tests, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            result.result_id,
            result.timestamp.isoformat(),
            result.algorithm_version,
            result.sample_size,
            str(result.p_values),
            str(result.passed_tests),
            result.notes
        ))
        self.conn.commit()

    def clear_keys(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM keys")
        self.conn.commit()
        print("Claves eliminadas.")    

    def release(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Base de datos cerrada.")