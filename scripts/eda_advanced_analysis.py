import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# 📥 Load Dataset
file_path = "data/processed/final_final_cleaned_peg_city_basketball_cleaned.csv"  # Adjust path if needed
df = pd.read_csv(file_path)

# 🛠 Convert Only Numeric Columns (Prevents String Errors)
numeric_cols = df.select_dtypes(include=["number"]).columns
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

# 🔍 Identify Outliers (IQR Method)
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

# 🏆 Top Players by Efficiency (Fixing Missing Player Names)
df["Player"] = df["Player"].fillna("Unknown")  # Fill missing names

top_players = df.sort_values(by="EFF", ascending=False).head(10)
print("\n🏆 Top Efficient Players:\n", top_players[["Player", "PTS", "FG%", "EFF"]])
