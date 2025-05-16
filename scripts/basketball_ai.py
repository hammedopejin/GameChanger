import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

# 📥 Load Dataset
file_path = "data/processed/final_final_cleaned_peg_city_basketball_stats.csv"
df = pd.read_csv(file_path)

# 🔍 Verify Columns
print("\n📊 Available Columns:\n", df.columns)

# 🚀 Advanced Player Metrics
df["TS%"] = df["PTS"] / (2 * (df["FGA"] + (0.44 * df["FTA"])))  # Correct TS% Formula
df["TS%"] = df["TS%"].replace([float('inf'), -float('inf')], 0).fillna(0)  # Handle divide errors
df.loc[(df["PTS"] == 0) | (df["FGA"] + (0.44 * df["FTA"]) == 0), "TS%"] = 0  # Prevent divide-by-zero errors
df.loc[df["TS%"] > 1, "TS%"] = 1  # Ensure TS% does not exceed 100%
df["AST_RATIO"] = df["AST"] / (df["AST"] + df["TO"])  # Assist-to-Turnover Ratio

# 📈 Adjust Efficiency Calculation
df["EFF"] = (df["PTS"] + df["DREB"] + df["OREB"] + df["AST"] + df["STL"] + df["BLK"]) - (df["FGA"] - df["FGM"]) - (df["FTA"] - df["FTM"]) - df["TO"]

# 🔄 Outlier Analysis
numeric_cols = df.select_dtypes(include=["number"]).columns
Q1, Q3 = df[numeric_cols].quantile(0.25), df[numeric_cols].quantile(0.75)
IQR = Q3 - Q1
outliers = ((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).sum()
print("\n🚨 Outlier Count:\n", outliers)

# 🏀 Sanity Check on TS% Values
print("\n📊 TS% Sanity Check:\n", df[["Player", "PTS", "FGA", "FTA", "TS%"]].head(15))

# 📊 Visualize Scoring Trends
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x="PTS")
plt.title("Points Distribution")
plt.show()

# 🔮 Predictive Model: Multi-Feature Ridge Regression
features = ["FG%", "AST", "DREB", "OREB", "3P%", "EFF", "RPG", "APG", "SPG", "BPG", "PPR"]
X = df[features].dropna()
y = df.loc[X.index, "PTS"]

# 🔍 Feature Scaling for Better Model Accuracy
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 🌟 Optimized Ridge Regression Model
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)

# Predictions & Evaluation
y_pred_ridge = ridge_model.predict(X_test)
mae_ridge = mean_absolute_error(y_test, y_pred_ridge)
r2_ridge = r2_score(y_test, y_pred_ridge)

print(f"\n🔥 Ridge Regression Performance:\nMAE: {mae_ridge:.2f}, R²: {r2_ridge:.2f}")

# 🏀 Generate Player Report
def generate_report(player_name):
    player_stats = df[df["Player"] == player_name]
    if player_stats.empty:
        return f"🚨 No data found for {player_name}."

    report = f"""
    🏀 **Player Report: {player_name}** 🏀
    ✔ **Points Scored:** {player_stats["PTS"].values[0]}
    ✔ **Field Goal %:** {player_stats["FG%"].values[0]:.2f}
    ✔ **True Shooting %:** {player_stats["TS%"].values[0]:.2f}
    ✔ **Assist Ratio:** {player_stats["AST_RATIO"].values[0]:.2f}
    ✔ **Efficiency Rating:** {player_stats["EFF"].values[0]:.2f}
    """
    return report

# 🔥 Example Usage:
player_name = "Justin Duff"  # Replace with actual player names from dataset
print(generate_report(player_name))
