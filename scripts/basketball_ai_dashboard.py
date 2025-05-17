import streamlit as st
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

# 🔍 Ensure TS% & AST_RATIO Columns Exist
if "TS%" not in df.columns:
    df["TS%"] = df["PTS"] / (2 * (df["FGA"] + (0.44 * df["FTA"])))
    df["TS%"] = df["TS%"].replace([float('inf'), -float('inf')], 0).fillna(0)
    df.loc[(df["PTS"] == 0) | (df["FGA"] + (0.44 * df["FTA"]) == 0), "TS%"] = 0
    df.loc[df["TS%"] > 1, "TS%"] = 1  # Ensures valid TS% values

if "AST_RATIO" not in df.columns:
    df["AST_RATIO"] = df["AST"] / (df["AST"] + df["TO"])
    df["AST_RATIO"] = df["AST_RATIO"].fillna(0)  # Handles NaN values

# 🔍 Feature Scaling for Predictions
features = ["FG%", "AST", "DREB", "OREB", "3P%", "EFF", "RPG", "APG", "SPG", "BPG", "PPR"]
X = df[features].dropna()
y = df.loc[X.index, "PTS"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 🌟 Train Ridge Regression Model
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)

# 🔮 Predicting Future Performance for Player
def predict_future_performance(player_name):
    player_stats = df[df["Player"].str.lower() == player_name.lower()]  # Exact match
    if player_stats.empty:
        return f"🚨 No future prediction available for '{player_name}'."

    player_features = player_stats[["FG%", "AST", "DREB", "OREB", "3P%", "EFF", "RPG", "APG", "SPG", "BPG", "PPR"]]
    player_features_scaled = scaler.transform(player_features)  # Standardizing features

    predicted_pts = ridge_model.predict(player_features_scaled)[0]  # Predict future points
    projected_fg = player_stats.iloc[0]["FG%"] * 1.05  # Assuming a slight improvement trend

    return f"""
    🔮 **Projected Performance for Next Game**  

    📊 **Expected Points:** **{predicted_pts:.2f}**  
    🎯 **Scoring Efficiency Estimate:** **{projected_fg:.2f}% FG**  
    _(Based on AI prediction & player trends)_  
    """

# 🔍 Helper Function: Generate Player Report (Exact Match Fix)
def generate_report(player_name):
    player_stats = df[df["Player"].str.lower() == player_name.lower()]  # Exact match only
    if player_stats.empty:
        return f"🚨 No data available for '{player_name}'.\n❌ **Possible reasons:**\n• Name is incorrect—please enter the full name as listed in the stats.\n• No recorded games—this player may not have played yet."

    report = f"""
    🏀 **Player Report: {player_stats.iloc[0]['Player']}**  

    ✔ **Points Scored:** {player_stats.iloc[0]["PTS"]}  
    ✔ **Field Goal %:** {player_stats.iloc[0]["FG%"]:.2f}  
    ✔ **True Shooting %:** {player_stats.iloc[0]["TS%"]:.2f}  
    ✔ **Assist Ratio:** {player_stats.iloc[0]["AST_RATIO"]:.2f}  
    ✔ **Efficiency Rating:** {player_stats.iloc[0]["EFF"]:.2f}  
    """
    return report

# 🎨 Streamlit UI Setup
st.set_page_config(page_title="GameChanger: AI Basketball Dashboard", layout="wide")

st.title("🏀 GameChanger Basketball AI Dashboard")
st.sidebar.header("Enter a Player Name:")

# ⚡ Correct session state handling
if "previous_player" not in st.session_state:
    st.session_state.previous_player = ""

player_name = st.sidebar.text_input("Player Name", "")

# 🧹 Refresh dashboard only when a valid new name is entered
if player_name.strip():  # Avoids blank screen when Enter is pressed with an empty input
    if player_name != st.session_state.previous_player:
        st.session_state.previous_player = player_name
        st.rerun()  # Corrected function for smooth UI refresh

# 📊 Generate Report if Name is Entered
if player_name:
    report = generate_report(player_name)
    st.write(report)

    # 📊 Display Player Stats Table (Compact Format)
    player_stats_display = df[df["Player"].str.lower() == player_name.lower()][["PTS", "FG%", "TS%", "AST_RATIO", "EFF", "RPG", "APG", "SPG", "BPG"]]

    if player_stats_display.empty:
        st.write(f"🚨 No data available for '{player_name}'.\n❌ **Possible reasons:**\n• Name is incorrect—please enter the full name as listed in the stats.\n• No recorded games—this player may not have played yet.")
    else:
        st.subheader(f"📊 {player_name} - Detailed Stats")
        st.write(player_stats_display)

    # 🔮 Future Prediction
    prediction = predict_future_performance(player_name)
    st.write(prediction)

# 🏀 Game Summary (Final Section)
st.subheader("🏀 Team-Wide Insights")
top_players = df.nlargest(3, "EFF")[["Player", "EFF", "PTS", "FG%", "TS%"]]

if top_players.empty:
    st.write("No top players found for this dataset.")
else:
    st.write(top_players)

st.write("AI-powered basketball insights are now live!")
