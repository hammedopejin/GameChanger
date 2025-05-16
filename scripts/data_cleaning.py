import pandas as pd
import os

# Get list of CSV files from the current directory
csv_files = [file for file in os.listdir() if file.endswith(".csv")]

# Define columns that may contain extreme values
extreme_columns = ["FG%", "PPR"]

# Define columns to remove
columns_to_remove = ["Extra_0"]

# Loop through all CSV files for cleaning
for file in csv_files:
    print(f"\n🛠 Cleaning: {file}")

    try:
        # Read CSV
        df = pd.read_csv(file)

        # Remove unnecessary columns if they exist
        df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors="ignore")

        # Fill missing values with appropriate replacements
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype == "object":
                    df[col].fillna("Unknown", inplace=True)  # Fill missing strings with 'Unknown'
                else:
                    df[col].fillna(df[col].median(), inplace=True)  # Fill missing numeric values with median

        # Handle extreme values
        for col in extreme_columns:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: x if x <= 100 else 100)  # Clip extreme percentages to 100

        # Save the cleaned dataset
        cleaned_filename = f"cleaned_{file}"
        df.to_csv(cleaned_filename, index=False)
        print(f"✅ Cleaned file saved: {cleaned_filename}")

    except Exception as e:
        print(f"🚨 Error processing {file}: {str(e)}")

print("\n🎯 Data cleaning complete!")
