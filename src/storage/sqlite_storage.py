import sqlite3
from pathlib import Path
from typing import Iterable, Any
from dataclasses import dataclass

@dataclass
class AQIRecord:
    city: str
    aqi: float
    pm25: float
    pm10: float
    co: float
    no2: float
    so2: float
    o3: float
    timestamp: str

class SQLiteStorage:
    """SQLite persistence layer for AQI data."""
    
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._init_db()  # Initialize database on object creation

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def _init_db(self) -> None:
        """Creates the necessary tables if they do not exist."""
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS aqi_readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    aqi REAL,
                    pm25 REAL,
                    pm10 REAL,
                    co REAL,
                    no2 REAL,
                    so2 REAL,
                    o3 REAL,
                    timestamp TEXT NOT NULL
                );
                """
            )

    def insert_many(self, records: Iterable[AQIRecord]) -> int:
        """Inserts multiple records into the aqi_readings table."""
        rows = [
            (r.city, r.aqi, r.pm25, r.pm10, r.co, r.no2, r.so2, r.o3, r.timestamp)
            for r in records
        ]
        if not rows:
            return 0

        with self._connect() as conn:
            cur = conn.executemany(
                """
                INSERT INTO aqi_readings
                (city, aqi, pm25, pm10, co, no2, so2, o3, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, 
                rows
            )
            return cur.rowcount

    def fetch_latest_per_city(self) -> list[dict[str, Any]]:
        """Fetch the latest AQI readings per city from the database."""
        q = """
        SELECT t1.city, t1.aqi, t1.pm25, t1.pm10, t1.co, t1.no2, t1.so2, t1.o3, t1.timestamp
        FROM aqi_readings t1
        JOIN (
            SELECT city, MAX(timestamp) AS max_ts
            FROM aqi_readings
            GROUP BY city
        ) t2
        ON t1.city = t2.city AND t1.timestamp = t2.max_ts
        ORDER BY t1.city;
        """
        with self._connect() as conn:
            cur = conn.execute(q)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
