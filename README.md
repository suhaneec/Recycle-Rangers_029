# 🛡️ **Crime Analysis Dashboard**

🌐 **Live App**: [Explore the Dashboard]((https://sc-crimeanalysis.streamlit.app/))

---

## 📊 **About the Project**
This project analyzes crime rates across various states and districts using the provided dataset, `crime_by_districts.csv`. It aims to uncover trends and patterns in crime occurrences, enabling data-driven decision-making and policy formulation.

---

## 🛠️ **Key Features**
- **Yearly Crime Trends**: 
  - Analyze overall trends in crime rates across states and districts over time.
  - 📈 **Visualization**: Line charts displaying total crimes and trends by type (e.g., Murder, Assault on women).
  
- **Top States by Crime Rate**:
  - Identify states with the highest crime rates in different categories.
  - 📊 **Visualization**: Bar charts with filters for crime types.

- **District-Level Crime Distribution**:
  - Explore granular-level crime data to identify local hotspots.
  - 🗺️ **Visualization**: Interactive maps or heatmaps.

- **Yearly Comparison of Specific Crime Types**:
  - Compare trends for specific crimes (e.g., assault, abduction) over the years.
  - 📉 **Visualization**: Multi-line charts for comparative analysis.

- **Impact of Legislation**:
  - Investigate crime trends related to the Protection of Civil Rights (PCR) and Prevention of Atrocities (POA) Acts.
  - 📊 **Visualization**: Line or bar charts to observe the impact.

- **High-Risk Areas for Women**:
  - Highlight states/districts with high rates of crimes against women.
  - 🔴 **Visualization**: Bar charts and heatmaps focusing on crimes affecting women.

---

## 📂 **About the Dataset**
The dataset `crime_by_districts.csv` includes crime data segmented by state and district, with key columns such as:
- **State/UT**: The name of the state/union territory.
- **Year**: The year the data was recorded.
- **District**: The district name for granular data.
- **Crime Types**: Categories of crime (e.g., Murder, Assault, Kidnapping).
- **Crime Count/Rate**: Specific counts or rates for each crime type.

**Dataset Summary**:
- **Rows**: 9,841  
- **Columns**: 13  
- **Key Columns**: `STATE/UT`, `Year`, `District`, and various crime types (e.g., Murder, Assault on women, Kidnapping).

---

## 🚀 **How to Run Locally**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/suhaneec/Recycle-Rangers_029/tree/main
   cd crime-analysis-dashboard


2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the App**:
   ```bash
   streamlit run app.py
   ```

---

## 📈 **Insights and Visualizations**
This dashboard provides the following insights:
1. **Yearly Crime Trends**: Overall and by crime type, with district and state-level comparisons.
2. **Top Crime States/Districts**: Focus on regions with the highest crime rates.
3. **Crime Categories**: Identify the most common crime types in each state or district.
4. **Crimes Against Women**: Highlight high-risk areas for targeted interventions.

---

## ❤️ **Contributing**
Contributions are welcome! Fork the repository, create a new branch, and submit your pull request with improvements or new features.

---

✨ **Let’s use data to make informed decisions and create safer communities!** ✨
```
