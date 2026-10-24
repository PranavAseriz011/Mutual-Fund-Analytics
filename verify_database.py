import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent / "bluestock_mf.db"

print("Database exists:", db_path.exists())

if db_path.exists():
    with sqlite3.connect(db_path) as conn:
        tables = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' ORDER BY name"
        ).fetchall()

        print("\nDatabase tables and row counts:")

        for (table_name,) in tables:
            count = conn.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            ).fetchone()[0]

            print(f"{table_name}: {count:,} rows")