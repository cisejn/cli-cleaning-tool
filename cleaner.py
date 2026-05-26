import argparse
import sys
import os
import pandas as pd
from datetime import datetime


def load_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    original_rows = len(df)
    original_cols = list(df.columns)

    # Trim whitespace from string columns (pandas 2.x compatible)
    for col in df.columns:
        if df[col].dtype == "object" or str(df[col].dtype) == "string":
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # Track missing values before cleaning
    missing_before = df.isnull().sum().to_dict()

    # Remove fully empty rows
    df = df.dropna(how="all")
    empty_rows_removed = original_rows - len(df)

    # Remove duplicate rows
    before_dedup = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before_dedup - len(df)

    # Reset index
    df = df.reset_index(drop=True)

    stats = {
        "original_rows": original_rows,
        "original_cols": len(original_cols),
        "columns": original_cols,
        "empty_rows_removed": empty_rows_removed,
        "duplicates_removed": duplicates_removed,
        "final_rows": len(df),
        "missing_values": missing_before,
        "missing_total": sum(missing_before.values()),
    }

    return df, stats


def print_report(stats: dict, output_path: str):
    print("\n" + "=" * 50)
    print(" CSV CLEANER REPORT")
    print("=" * 50)
    print(f"  Timestamp     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Output file   : {output_path}")
    print("-" * 50)
    print(f"  Original rows : {stats['original_rows']}")
    print(f"  Columns       : {stats['original_cols']}  →  {stats['columns']}")
    print(f"  Duplicates    : {stats['duplicates_removed']} rows removed")
    print(f"  Empty rows    : {stats['empty_rows_removed']} rows removed")
    print(f"  Final rows    : {stats['final_rows']}")
    print("-" * 50)
    print("  Missing values (before cleaning):")
    any_missing = False
    for col, count in stats["missing_values"].items():
        if count > 0:
            print(f"    • {col}: {count} missing")
            any_missing = True
    if not any_missing:
        print("No missing values found!")
    print("=" * 50 + "\n")


def save_report(stats: dict, output_path: str, report_path: str):
    with open(report_path, "w") as f:
        f.write("CSV CLEANER REPORT\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Output file: {output_path}\n\n")
        f.write(f"Original rows: {stats['original_rows']}\n")
        f.write(f"Columns ({stats['original_cols']}): {', '.join(stats['columns'])}\n")
        f.write(f"Duplicates removed: {stats['duplicates_removed']}\n")
        f.write(f"Empty rows removed: {stats['empty_rows_removed']}\n")
        f.write(f"Final rows: {stats['final_rows']}\n\n")
        f.write("Missing values (before cleaning):\n")
        for col, count in stats["missing_values"].items():
            f.write(f"  {col}: {count}\n")
    print(f"Report saved to: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="csv-cleaner-cli — Clean and summarize CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cleaner.py data.csv
  python cleaner.py data.csv --output clean_data.csv
  python cleaner.py data.csv --output clean_data.csv --save-report
        """,
    )
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument(
        "--output", "-o", help="Output file path (default: cleaned_<input>.csv)"
    )
    parser.add_argument(
        "--save-report", action="store_true", help="Save a text report alongside output"
    )

    args = parser.parse_args()

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        base = os.path.splitext(os.path.basename(args.input))[0]
        output_path = f"cleaned_{base}.csv"

    print(f"\nLoading: {args.input}")
    df = load_csv(args.input)

    print("Cleaning...")
    cleaned_df, stats = clean(df)

    cleaned_df.to_csv(output_path, index=False)
    print(f"Saved to: {output_path}")

    print_report(stats, output_path)

    if args.save_report:
        report_path = output_path.replace(".csv", "_report.txt")
        save_report(stats, output_path, report_path)


if __name__ == "__main__":
    main()
