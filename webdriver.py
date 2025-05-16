import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Safari WebDriver
driver = webdriver.Safari()

# List of URLs to scrape (Removed broken playoff link)
urls = [
    "https://pegcityball.info/2024-25-regular-season-statistics/",
    "https://pegcityball.info/2023-24-regular-season-statistics/",
    "https://pegcityball.info/summer-statistics/",
    "https://pegcityball.info/2024-spring-statistics/",
    "https://pegcityball.info",
    "https://pegcityball.info/standings-2024-summer-league/",
    "https://pegcityball.info/2024-spring-standings/",
    "https://pegcityball.info/2023-summer-standings/"
]

# Define standard headers for consistency across all datasets
standard_headers = [
    "Player", "GP", "FT", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", 
    "DREB", "OREB", "AST", "STL", "TO", "BLK", "PTS", "RPG", "APG", "SPG", "BPG", "EFF", "PPR"
]

for url in urls:
    # Load page
    driver.get(url)

    try:
        # Wait for the table to be present before proceeding
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Process table data
        data = []
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")  # Get each cell in the row
            row_data = [col.text.strip() for col in columns]  # Extract text from each cell
            if row_data:  # Avoid empty rows
                data.append(row_data)

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Ensure header detection is correct
        if not df.empty and all(col.isalpha() for col in df.iloc[0]):
            extracted_headers = df.iloc[0]  # Assume first row contains headers
            df = df[1:]  # Remove header row from data
        else:
            extracted_headers = standard_headers[:df.shape[1]]  # Use default headers

        # Assign headers dynamically, adjusting for column mismatches
        expected_columns = df.shape[1]
        if expected_columns > len(standard_headers):
            extra_headers = [f"Extra_{i}" for i in range(expected_columns - len(standard_headers))]
            df.columns = standard_headers + extra_headers  # Expand headers list
        else:
            df.columns = extracted_headers[:expected_columns]  # Standard assignment

        # Add missing columns from standard list
        for missing in standard_headers:
            if missing not in df.columns:
                df[missing] = None  # Add empty column

        # Remove extra columns if they exist
        extra_columns = [col for col in df.columns if col not in standard_headers]
        df.drop(columns=extra_columns, errors="ignore", inplace=True)

        # Create a clean filename from the URL
        filename = url.split("/")[-2] if url.split("/")[-2] else "peg_city_general"
        filename = filename.replace("-", "_") + "_stats.csv"
        df.to_csv(filename, index=False)

        print(f"✅ Saved: {filename}")  # Confirm output

    except Exception as e:
        print(f"🚨 Skipping {url} - Error: {str(e)}")  # Shows full error details

# Close browser
driver.quit()
