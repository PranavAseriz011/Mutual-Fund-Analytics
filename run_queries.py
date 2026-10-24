import sqlite3
from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parent
DB_PATH = PROJECT_PATH / "bluestock_mf.db"
SQL_PATH = PROJECT_PATH / "sql" / "queries.sql"

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DB_PATH}")

if not SQL_PATH.exists():
    raise FileNotFoundError(f"SQL file not found: {SQL_PATH}")

sql_text = SQL_PATH.read_text(encoding="utf-8")

# Split the file into individual SQL statements.
statements = [
    statement.strip()
    for statement in sql_text.split(";")
    if statement.strip()
]

print(f"Found {len(statements)} SQL statements.\n")

with sqlite3.connect(DB_PATH) as conn:
    for number, statement in enumerate(statements, start=1):
        print("=" * 60)
        print(f"QUERY {number}")

        try:
            cursor = conn.execute(statement)

            if cursor.description:
                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchmany(5)

                print("Columns:", columns)
                print("First 5 rows:")

                for row in rows:
                    print(row)

                print("Status: PASSED")
            else:
                print("Status: EXECUTED")

        except sqlite3.Error as error:
            print("Status: FAILED")
            print("Error:", error)

print("\nQuery testing complete.")