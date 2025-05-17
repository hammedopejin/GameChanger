# 🏀 GameChanger Basketball AI Dashboard  

##  Overview  
GameChanger is an AI-powered basketball analytics tool that helps coaches assess player performance, track stats, and **predict future performance** using machine learning. The dashboard provides **player-specific insights** based on past game data, helping coaches **make data-driven decisions**.

---

## 📊 **Data Acquisition**
### 📥 Dataset Used  
- **File Name:** `final_final_cleaned_peg_city_basketball_stats.csv`  
- **Source:** [Peg City Ball](https://pegcityball.info) _(Scraped using Selenium)_  
- **Size:** ~10,000 rows (Player-specific game logs).  
- **Features:** Includes shooting accuracy, assists, rebounds, steals, blocks, efficiency, and game-by-game breakdown.  

### 🛠 **Web Scraping Process**
We **extracted player performance data** from Peg City Ball using **Selenium**, a powerful web automation tool.

✔ **Why Selenium?**  
Selenium allowed us to **dynamically interact with Peg City Ball’s website**, extracting structured player data directly from game logs.

✔ **Steps Followed:**  
1️⃣ **Initialized a Selenium WebDriver** → Automated navigation through player stats pages.  
2️⃣ **Extracted HTML Elements** → Scraped key statistics from structured tables.  
3️⃣ **Stored Data in CSV** → Formatted for analysis & model training.  
4️⃣ **Performed Data Cleaning** → Removed duplicates, fixed missing values, and ensured data consistency.  

✔ **Post-Scraping Data Handling:**  
- Processed scraped stats into **structured columns** for AI modeling.  
- **Feature Engineering:** Added calculated metrics like **True Shooting %** and **Assist Ratio**.  
- Stored final dataset in `final_final_cleaned_peg_city_basketball_stats.csv`.  

---

## 🔎 **Exploratory Data Analysis (EDA)**
EDA was performed to clean and understand the dataset:
- **Missing values handled** → Filled NaNs for TS% & AST_RATIO.  
- **Outliers examined** → Extreme efficiency ratings adjusted.  
- **Feature Engineering** → Added calculated metrics for **True Shooting %** and **Assist Ratio**.  
- **Correlation Analysis** → Identified strongest predictors of scoring efficiency.  

### 📊 Key Metrics in EDA:
| Metric | Description |
|--------|------------|
| **TS% (True Shooting %)** | Measures scoring efficiency considering FG & FTs. |
| **AST_RATIO (Assist Ratio)** | Evaluates passing efficiency based on assists & turnovers. |
| **EFF (Efficiency Rating)** | Overall player impact on the court. |

---

## 📦 **Libraries Used**
This project utilizes the following Python libraries:
- **Selenium** → Web scraping automation.  
- **Streamlit** → Interactive web-based dashboard.  
- **Pandas** → Data handling & manipulation.  
- **Matplotlib & Seaborn** → Visualizations & statistical plotting.  
- **Scikit-Learn** → Machine learning predictions (Ridge Regression).  

---

## 🔮 **Machine Learning Model**
### **Model Used:** **Ridge Regression**
- Predicts **future player performance** based on game trends.  
- **Feature Scaling** applied using `StandardScaler`.  
- **Training Data Split:** 80% train / 20% test.  

### **Performance Metrics:**
- **MAE (Mean Absolute Error):** Evaluates prediction accuracy.  
- **R² Score:** Measures model reliability (trend capture).  

---

## 🏀 **Features in Dashboard**
✔ **Player Report:** Instant performance breakdown.  
✔ **Detailed Stats Table:** Game-by-game analytics.  
✔ **Future Performance Prediction:** AI forecasts next game stats.  
✔ **Team Insights:** Highlights top players based on efficiency.  

---

##  **How to Run the Project**
### **🔧 Installation & Setup**
```bash
# Clone the repository  
git clone https://github.com/hammedopejin/GameChanger.git
cd GameChanger  

# Install dependencies  
pip install -r requirements.txt  

# Run the Streamlit App  
streamlit run basketball_ai_dashboard.py  

✔ **The dashboard will launch in your browser!**   
✔ **Player insights, future predictions, and team analytics—all ready to go!**  

---

## 📬 Feedback & Contributions  
If you have ideas for improvement or want to contribute:  
1️⃣ **Fork the repository**  
2️⃣ **Submit a pull request with your changes**  
3️⃣ **Open issues for feature requests**  

---

## 📜 License  
This project is licensed under the **MIT License**. Feel free to use, modify, and improve!  

 **GameChanger is built to empower coaches & players with AI-driven insights.**  
 **Run it, test it, and let’s make basketball analytics smarter!**  
