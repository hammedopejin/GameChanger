import pandas as pd
import os

# Get list of CSV files from the current directory
csv_files = [file for file in os.listdir() if file.endswith(".csv")]

# Loop through all CSV files for EDA
for file in csv_files:
    print(f"\n🔍 Analyzing: {file}")

    try:
        # Read CSV
        df = pd.read_csv(file)

        # Display basic information
        print("\n📊 Data Overview:")
        print(df.info())

        # Display missing values
        print("\n⚠️ Missing Values:")
        print(df.isnull().sum())

        # Display summary statistics
        print("\n📈 Summary Statistics:")
        print(df.describe())

    except Exception as e:
        print(f"🚨 Error processing {file}: {str(e)}")

print("\n✅ EDA complete!")
