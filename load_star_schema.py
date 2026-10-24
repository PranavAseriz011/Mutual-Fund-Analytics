from pathlib import Path
import sqlite3
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
PROJECT_PATH = Path(__file__).resolve().parent
DB_PATH = PROJECT_PATH / "bluestock_mf.db"


def load_star_schema():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        # Read the existing source tables.
        fund_master = pd.read_sql_query(
            "SELECT * FROM fund_master", conn
        )
        nav = pd.read_sql_query(
            "SELECT * FROM nav_history", conn
        )
        transactions = pd.read_sql_query(
            "SELECT * FROM investor_transactions", conn
        )
        performance = pd.read_sql_query(
            "SELECT * FROM scheme_performance", conn
        )
        aum = pd.read_sql_query(
            "SELECT * FROM aum_by_fund_house", conn
        )

        # Normalize AMFI codes for consistent matching.
        for df in (fund_master, nav, transactions, performance):
            if "amfi_code" in df.columns:
                df["amfi_code"] = (
                    df["amfi_code"].astype("string").str.strip()
                )

        # Build a stable fund dimension.
        funds = fund_master.drop_duplicates(
            subset=["amfi_code"]
        ).copy()

        funds = funds[funds["amfi_code"].notna()]
        funds = funds[funds["amfi_code"] != ""]

        funds = funds.reset_index(drop=True)
        funds["fund_key"] = range(1, len(funds) + 1)

        dim_fund = pd.DataFrame({
            "fund_key": funds["fund_key"],
            "amfi_code": funds["amfi_code"],
            "fund_house": funds["fund_house"],
            "scheme_name": funds["scheme_name"],
            "category": funds["category"],
            "sub_category": funds["sub_category"],
            "plan": funds["plan"],
            "launch_date": funds["launch_date"],
            "benchmark": funds["benchmark"],
            "expense_ratio_pct": funds["expense_ratio_pct"],
            "exit_load_pct": funds["exit_load_pct"],
            "min_sip_amount": funds["min_sip_amount"],
            "min_lumpsum_amount": funds["min_lumpsum_amount"],
            "fund_manager": funds["fund_manager"],
            "risk_category": funds["risk_category"],
            "sebi_category_code": funds["sebi_category_code"],
        })

        fund_map = dict(zip(
            dim_fund["amfi_code"],
            dim_fund["fund_key"]
        ))

        # Collect valid dates from NAV, transactions and AUM.
        date_series = [
            pd.to_datetime(nav["date"], errors="coerce"),
            pd.to_datetime(
                transactions["transaction_date"], errors="coerce"
            ),
            pd.to_datetime(aum["date"], errors="coerce"),
        ]

        all_dates = pd.concat(
            [series.dropna() for series in date_series],
            ignore_index=True
        ).dt.normalize().drop_duplicates().sort_values()

        dim_date = pd.DataFrame({
            "full_date": all_dates.dt.strftime("%Y-%m-%d")
        })

        dim_date = dim_date.reset_index(drop=True)
        dim_date["date_key"] = (
            pd.to_datetime(dim_date["full_date"]).dt.strftime("%Y%m%d")
            .astype(int)
        )
        parsed_dates = pd.to_datetime(dim_date["full_date"])
        dim_date["year"] = parsed_dates.dt.year
        dim_date["month"] = parsed_dates.dt.month
        dim_date["quarter"] = parsed_dates.dt.quarter

        date_map = dict(zip(
            dim_date["full_date"],
            dim_date["date_key"]
        ))

        # --------------------------------------------------
        # Build NAV fact table.
        # --------------------------------------------------
        nav["date"] = pd.to_datetime(nav["date"], errors="coerce")
        nav["fund_key"] = nav["amfi_code"].map(fund_map)
        nav["date_key"] = nav["date"].dt.strftime("%Y-%m-%d").map(date_map)
        nav["nav"] = pd.to_numeric(nav["nav"], errors="coerce")

        fact_nav = nav.dropna(
            subset=["fund_key", "date_key", "nav"]
        ).copy()

        fact_nav = fact_nav[fact_nav["nav"] > 0]
        fact_nav = fact_nav.drop_duplicates(
            subset=["fund_key", "date_key"]
        )

        fact_nav = fact_nav[
            ["fund_key", "date_key", "nav"]
        ].copy()
        fact_nav.insert(0, "nav_key", range(1, len(fact_nav) + 1))

        # --------------------------------------------------
        # Build transaction fact table.
        # --------------------------------------------------
        transactions["transaction_date"] = pd.to_datetime(
            transactions["transaction_date"], errors="coerce"
        )
        transactions["fund_key"] = transactions["amfi_code"].map(fund_map)
        transactions["date_key"] = (
            transactions["transaction_date"]
            .dt.strftime("%Y-%m-%d").map(date_map)
        )
        transactions["amount_inr"] = pd.to_numeric(
            transactions["amount_inr"], errors="coerce"
        )

        fact_transactions = transactions.dropna(
            subset=["fund_key", "date_key", "amount_inr", "investor_id"]
        ).copy()

        fact_transactions = fact_transactions[
            fact_transactions["amount_inr"] > 0
        ]

        transaction_columns = [
            "investor_id", "fund_key", "date_key", "transaction_type",
            "amount_inr", "state", "city", "city_tier", "age_group",
            "gender", "annual_income_lakh", "payment_mode", "kyc_status"
        ]

        fact_transactions = fact_transactions[
            transaction_columns
        ].copy()

        fact_transactions.insert(
            0, "transaction_key",
            range(1, len(fact_transactions) + 1)
        )

        # --------------------------------------------------
        # Build performance fact table.
        # --------------------------------------------------
        performance["fund_key"] = performance["amfi_code"].map(fund_map)

        performance_columns = [
            "fund_key", "return_1yr_pct", "return_3yr_pct",
            "return_5yr_pct", "benchmark_3yr_pct", "alpha", "beta",
            "sharpe_ratio", "sortino_ratio", "std_dev_ann_pct",
            "max_drawdown_pct", "aum_crore", "expense_ratio_pct",
            "morningstar_rating", "risk_grade"
        ]

        fact_performance = performance.dropna(
            subset=["fund_key"]
        ).copy()

        fact_performance = fact_performance[
            performance_columns
        ].drop_duplicates(subset=["fund_key"])

        fact_performance = fact_performance.reset_index(drop=True)
        fact_performance.insert(
            0, "performance_key",
            range(1, len(fact_performance) + 1)
        )

        # --------------------------------------------------
        # Build AUM fact table.
        # --------------------------------------------------
        aum["date"] = pd.to_datetime(aum["date"], errors="coerce")
        aum["date_key"] = aum["date"].dt.strftime("%Y-%m-%d").map(date_map)

        aum["aum_lakh_crore"] = pd.to_numeric(
            aum["aum_lakh_crore"], errors="coerce"
        )
        aum["aum_crore"] = pd.to_numeric(
            aum["aum_crore"], errors="coerce"
        )
        aum["num_schemes"] = pd.to_numeric(
            aum["num_schemes"], errors="coerce"
        )

        fact_aum = aum.dropna(
            subset=["fund_house", "date_key"]
        ).copy()

        fact_aum = fact_aum.drop_duplicates(
            subset=["fund_house", "date_key"]
        )

        fact_aum = fact_aum[
            [
                "fund_house", "date_key", "aum_lakh_crore",
                "aum_crore", "num_schemes"
            ]
        ].copy()

        fact_aum = fact_aum.reset_index(drop=True)
        fact_aum.insert(
            0, "aum_key",
            range(1, len(fact_aum) + 1)
        )

        # --------------------------------------------------
        # Replace only star-schema tables, preserving sources.
        # --------------------------------------------------
        tables = {
            "dim_fund": dim_fund,
            "dim_date": dim_date,
            "fact_nav": fact_nav,
            "fact_transactions": fact_transactions,
            "fact_performance": fact_performance,
            "fact_aum": fact_aum,
        }

        # Check that all foreign keys will resolve before writing.
        fund_keys = set(dim_fund["fund_key"])
        date_keys = set(dim_date["date_key"])

        for name, df in tables.items():
            if "fund_key" in df.columns:
                invalid = ~df["fund_key"].isin(fund_keys)
                if invalid.any():
                    raise ValueError(
                        f"{name} contains unresolved fund keys."
                    )

            if "date_key" in df.columns:
                invalid = ~df["date_key"].isin(date_keys)
                if invalid.any():
                    raise ValueError(
                        f"{name} contains unresolved date keys."
                    )

        # Use a transaction so failures roll back the changes.
        conn.execute("BEGIN")

        for table_name in tables:
            conn.execute(f'DELETE FROM "{table_name}"')

        for table_name, df in tables.items():
            columns = list(df.columns)
            quoted_columns = ", ".join(f'"{col}"' for col in columns)
            placeholders = ", ".join("?" for _ in columns)

            insert_sql = (
                f'INSERT INTO "{table_name}" ({quoted_columns}) '
                f'VALUES ({placeholders})'
            )

            rows = [
                tuple(
                    None if pd.isna(value) else value
                    for value in row
                )
                for row in df.itertuples(index=False, name=None)
            ]

            conn.executemany(insert_sql, rows)

        # Validate referential integrity.
        violations = conn.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if violations:
            raise ValueError(
                f"Foreign-key violations found: {violations[:10]}"
            )

        conn.commit()

        print("\nSTAR-SCHEMA LOAD REPORT")
        print("-" * 35)

        for table_name, df in tables.items():
            actual_count = conn.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            ).fetchone()[0]

            print(
                f"{table_name}: {actual_count:,} rows "
                f"(prepared: {len(df):,})"
            )

        print("\nForeign-key check: PASSED")
        print("Original 10 source tables preserved.")
        print(f"Database: {DB_PATH}")


if __name__ == "__main__":
    load_star_schema()