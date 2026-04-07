import sqlite3
import json
from datetime import datetime
from domain.key import Key
from domain.analysis_result import AnalysisResult
from config import DB_PATH

class SQLiteRepository:

    def __init__(self):
        self.db_path = DB_PATH
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._create_tables()
        print("Base de datos conectada: " + self.db_path)

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keys (
                key_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            INSERT INTO keys (value, timestamp, algorithm_version)
            VALUES (?, ?, ?)
        """, (
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
                value=row[1],
                timestamp=datetime.fromisoformat(row[2]),
                algorithm_version=row[3],
                key_id=row[0]
            ))
        return keys

    def get_keys_by_version(self, version):
        """Devuelve solo las claves de una versión concreta del algoritmo."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT key_id, value, timestamp, algorithm_version FROM keys WHERE algorithm_version = ?",
            (version,)
        )
        rows = cursor.fetchall()
        keys = []
        for row in rows:
            keys.append(Key(
                value=row[1],
                timestamp=datetime.fromisoformat(row[2]),
                algorithm_version=row[3],
                key_id=row[0]
            ))
        return keys

    def count_keys_by_version(self, version):
        """Cuántas claves hay acumuladas de una versión concreta."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM keys WHERE algorithm_version = ?",
            (version,)
        )
        return cursor.fetchone()[0]

    def delete_keys_by_version(self, version):
        """Borra solo las claves de una versión concreta. No toca el resto."""
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM keys WHERE algorithm_version = ?",
            (version,)
        )
        self.conn.commit()
        print(f"Claves de versión {version} eliminadas.")

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
            json.dumps(result.p_values),
            json.dumps(result.passed_tests),
            result.notes
        ))
        self.conn.commit()

    def get_all_results(self):
        """Historial completo de análisis — todas las versiones."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT result_id, timestamp, algorithm_version, sample_size, p_values, passed_tests, notes FROM analysis_results ORDER BY timestamp"
        )
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append(AnalysisResult(
                result_id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                algorithm_version=row[2],
                sample_size=row[3],
                p_values=json.loads(row[4]),
                passed_tests=json.loads(row[5]),
                notes=row[6]
            ))
        return results

    def clear_keys(self):
        """Borra TODAS las claves. Solo para tests."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM keys")
        self.conn.commit()
        print("Claves eliminadas.")

    def release(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Base de datos cerrada.")