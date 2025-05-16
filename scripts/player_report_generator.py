import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# 📥 Load Dataset
file_path = "data/processed/final_final_cleaned_peg_city_basketball_stats.csv"  # Adjust if needed
df = pd.read_csv(file_path)

# 🛠 Verify Column Names
print("\n📊 Available Columns in Dataset:\n", df.columns)

# 🚨 Adjust Efficiency Calculation Based on Available Columns
if "REB" in df.columns:
    df["EFF"] = (df["PTS"] + df["REB"] + df["AST"] + df["STL"] + df["BLK"]) - (df["FGA"] - df["FGM"]) - (df["FTA"] - df["FTM"]) - df["TO"]
elif "DREB" in df.columns and "OREB" in df.columns:
    df["EFF"] = (df["PTS"] + df["DREB"] + df["OREB"] + df["AST"] + df["STL"] + df["BLK"]) - (df["FGA"] - df["FGM"]) - (df["FTA"] - df["FTM"]) - df["TO"]
else:
    print("\n🚨 ERROR: Rebound columns missing—EFF calculation adjusted.")
    df["EFF"] = (df["PTS"] + df["AST"] + df["STL"] + df["BLK"]) - (df["FGA"] - df["FGM"]) - (df["FTA"] - df["FTM"]) - df["TO"]

# 🔍 Identify Outliers (IQR Method)
numeric_cols = df.select_dtypes(include=["number"]).columns
Q1 = df[numeric_cols].quantile(0.25)
Q3 = df[numeric_cols].quantile(0.75)
IQR = Q3 - Q1
outliers = ((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).sum()
print("\n🚨 Outlier Count per Column:\n", outliers)

# 📊 Visualization of Extreme Players in PTS
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x="PTS")
plt.title("Distribution of Points (PTS)")
plt.show()

# 🔮 Predictive Model: FG% -> PTS (Can Shooting Efficiency Predict Scoring?)
X = df[["FG%"]]  # Feature
y = df["PTS"]  # Target

# Split Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# 📈 Evaluate Model Performance
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"\n🔮 Model Performance:\nMean Absolute Error: {mae:.2f}, R-squared: {r2:.2f}")

# 📝 AI-Generated Player Report
def generate_report(player_name):
    player_stats = df[df["Player"] == player_name]
    if player_stats.empty:
        return f"🚨 No data found for {player_name}."

    report = f"""
    🏀 **Player Report: {player_name}** 🏀
    ✔ **Points Scored:** {player_stats["PTS"].values[0]}
    ✔ **Field Goal %:** {player_stats["FG%"].values[0]:.2f}
    ✔ **Efficiency Rating:** {player_stats["EFF"].values[0]:.2f}
    """
    return report

# Example Usage
player_name = "Justin Duff"  # Replace with actual names from your dataset
print(generate_report(player_name))
