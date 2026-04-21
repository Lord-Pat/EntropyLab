import sqlite3
import json
from datetime import datetime
from domain.key import Key
from domain.nist_result import NistResult
from domain.shannon_result import ShannonResult
from config import DB_PATH
from domain.autocorrelation_result import AutocorrelationResult
from domain.maurer_result import MaurerResult

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
            CREATE TABLE IF NOT EXISTS nist_results (
                result_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                algorithm_version TEXT NOT NULL,
                sample_size INTEGER NOT NULL,
                p_values TEXT NOT NULL,
                passed_tests TEXT NOT NULL,
                notes TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shannon_results (
                result_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                algorithm_version TEXT NOT NULL,
                sample_size INTEGER NOT NULL,
                shannon REAL NOT NULL,
                notes TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS autocorrelation_results (
                result_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                algorithm_version TEXT NOT NULL,
                sample_size INTEGER NOT NULL,
                lag1_correlation REAL NOT NULL,
                lag1_p REAL NOT NULL,
                lag8_correlation REAL NOT NULL,
                lag8_p REAL NOT NULL,
                notes TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS maurer_results (
                result_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                algorithm_version TEXT NOT NULL,
                sample_size INTEGER NOT NULL,
                fn REAL NOT NULL,
                p_value REAL NOT NULL,
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

    def save_nist_result(self, result):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO nist_results
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

    def get_all_nist_results(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT result_id, timestamp, algorithm_version, sample_size, p_values, passed_tests, notes FROM nist_results ORDER BY timestamp")
        rows = cursor.fetchall()
        return [NistResult(
            result_id=r[0],
            timestamp=datetime.fromisoformat(r[1]),
            algorithm_version=r[2],
            sample_size=r[3],
            p_values=json.loads(r[4]),
            passed_tests=json.loads(r[5]),
            notes=r[6]
        ) for r in rows]

    def save_shannon_result(self, result):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO shannon_results
            (result_id, timestamp, algorithm_version, sample_size, shannon, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            result.result_id,
            result.timestamp.isoformat(),
            result.algorithm_version,
            result.sample_size,
            result.shannon,
            result.notes
        ))
        self.conn.commit()

    def get_all_shannon_results(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT result_id, timestamp, algorithm_version, sample_size, shannon, notes FROM shannon_results ORDER BY timestamp")
        rows = cursor.fetchall()
        return [ShannonResult(
            result_id=r[0],
            timestamp=datetime.fromisoformat(r[1]),
            algorithm_version=r[2],
            sample_size=r[3],
            shannon=r[4],
            notes=r[5]
        ) for r in rows]
    
    def save_autocorrelation_result(self, result):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO autocorrelation_results
            (result_id, timestamp, algorithm_version, sample_size, lag1_correlation, lag1_p, lag8_correlation, lag8_p, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.result_id,
            result.timestamp.isoformat(),
            result.algorithm_version,
            result.sample_size,
            result.lag1_correlation,
            result.lag1_p,
            result.lag8_correlation,
            result.lag8_p,
            result.notes
        ))
        self.conn.commit()

    def get_all_autocorrelation_results(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT result_id, timestamp, algorithm_version, sample_size, lag1_correlation, lag1_p, lag8_correlation, lag8_p, notes FROM autocorrelation_results ORDER BY timestamp")
        rows = cursor.fetchall()
        return [AutocorrelationResult(
            result_id=r[0],
            timestamp=datetime.fromisoformat(r[1]),
            algorithm_version=r[2],
            sample_size=r[3],
            lag1_correlation=r[4],
            lag1_p=r[5],
            lag8_correlation=r[6],
            lag8_p=r[7],
            notes=r[8]
        ) for r in rows]

    def save_maurer_result(self, result):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO maurer_results
            (result_id, timestamp, algorithm_version, sample_size, fn, p_value, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            result.result_id,
            result.timestamp.isoformat(),
            result.algorithm_version,
            result.sample_size,
            result.fn,
            result.p_value,
            result.notes
        ))
        self.conn.commit()

    def get_all_maurer_results(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT result_id, timestamp, algorithm_version, sample_size, fn, p_value, notes FROM maurer_results ORDER BY timestamp")
        rows = cursor.fetchall()
        return [MaurerResult(
            result_id=r[0],
            timestamp=datetime.fromisoformat(r[1]),
            algorithm_version=r[2],
            sample_size=r[3],
            fn=r[4],
            p_value=r[5],
            notes=r[6]
        ) for r in rows]

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