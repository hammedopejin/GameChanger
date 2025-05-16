import pandas as pd
import os

# Get list of cleaned CSV files from the processed data directory
data_dir = "data/processed"
csv_files = [file for file in os.listdir(data_dir) if file.endswith(".csv")]

# Define columns that need missing value imputation
fill_missing_values = ["PTS", "RPG", "APG", "SPG", "BPG", "EFF", "FTA", "FT%", "DREB", "OREB", "AST", "STL", "TO", "BLK"]

# Define columns to validate extreme values
validate_outliers = ["FG%", "PPR"]

# Define threshold to cap outliers
ppr_threshold = 30

# Loop through all cleaned CSV files for final processing
for file in csv_files:
    print(f"\n🛠 Finalizing Cleanup: {file}")

    try:
        # Read CSV
        file_path = f"{data_dir}/{file}"
        df = pd.read_csv(file_path)

        # Fill missing values
        for col in fill_missing_values:
            if col in df.columns and df[col].isnull().sum() > 0:
                if df[col].dtype == "object":
                    df[col].fillna("Unknown", inplace=True)  # Fill missing categorical values
                else:
                    df[col].fillna(df[col].median(), inplace=True)  # Fill missing numeric values with median

        # Validate and cap outlier values
        if "PPR" in df.columns:
            df["PPR"] = df["PPR"].apply(lambda x: min(x, ppr_threshold))

        # Fix low FG% values
        if "FG%" in df.columns:
            df["FG%"] = df["FG%"].apply(lambda x: max(x, 10))  # Ensures valid FG%

        # Save the finalized dataset
        finalized_filename = f"final_{file}"
        df.to_csv(f"{data_dir}/{finalized_filename}", index=False)
        print(f"✅ Finalized file saved: {finalized_filename}")

    except Exception as e:
        print(f"🚨 Error processing {file}: {str(e)}")

print("\n🎯 Final data cleaning complete!")
