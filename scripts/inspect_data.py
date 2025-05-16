import pandas as pd
import os

# Get list of CSV files from the current directory
csv_files = [file for file in os.listdir() if file.endswith(".csv")]

# Define standard headers for consistency check
standard_headers = [
    "Player", "GP", "FT", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", 
    "DREB", "OREB", "AST", "STL", "TO", "BLK", "PTS", "RPG", "APG", "SPG", "BPG", "EFF", "PPR"
]

# Inspect each CSV file
for file in csv_files:
    print(f"\n🔍 Inspecting: {file}")

    try:
        # Read CSV
        df = pd.read_csv(file)

        # Print first few rows
        print(df.head())

        # Check if headers match standard headers
        missing_headers = [col for col in standard_headers if col not in df.columns]
        extra_headers = [col for col in df.columns if col not in standard_headers]

        # Print header mismatches
        if missing_headers:
            print(f"⚠️ Missing headers: {missing_headers}")
        if extra_headers:
            print(f"⚠️ Extra headers found: {extra_headers}")

    except Exception as e:
        print(f"🚨 Error reading {file}: {str(e)}")

print("\n✅ Inspection complete!")
