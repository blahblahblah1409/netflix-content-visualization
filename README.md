# 🎬 Netflix Content Visualization

A beginner-friendly Data Science project that analyzes and visualizes **Netflix Movies & TV Shows** data using Python, Pandas, Matplotlib, and Seaborn.

---

## 📁 Project Structure

```
netflix_project/
├── data/
│   └── netflix_titles.csv        # Dataset (6,000 titles)
├── visualizations/               # Output charts (PNG)
│   ├── 01_overview_dashboard.png
│   ├── 02_genre_analysis.png
│   ├── 03_content_trends.png
│   ├── 04_ratings_deep_dive.png
│   ├── 05_country_analysis.png
│   ├── 06_duration_analysis.png
│   └── 07_summary_dashboard.png
├── generate_data.py              # Creates synthetic Netflix-style dataset
├── netflix_eda.py                # Main EDA + visualization script
├── requirements.txt
└── README.md
```

---

## 🔧 Setup & Installation

```bash
# 1. Clone / download the project
# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the dataset
python generate_data.py

# 4. Run the full analysis
python netflix_eda.py
```

---

## 📊 Visualizations Produced

| # | Chart | What It Shows |
|---|-------|---------------|
| 1 | **Overview Dashboard** | Content type donut, yearly additions, top countries, rating bar |
| 2 | **Genre Analysis** | Top 15 genres + Movies vs TV Shows per genre |
| 3 | **Content Trends** | Area chart, release-year histogram, genre lines, monthly heatmap |
| 4 | **Ratings Deep Dive** | Pie chart, grouped bars by type, stacked yearly trend |
| 5 | **Country Analysis** | Bubble chart of top 15 countries + content-type ratio bar |
| 6 | **Duration Analysis** | Movie runtime histogram, season distribution, violin plot |
| 7 | **Summary Dashboard** | KPI cards + all key charts in one view |

---

## 🛠️ Tech Stack

| Library    | Purpose                           |
|------------|-----------------------------------|
| `pandas`   | Data loading, cleaning, grouping  |
| `numpy`    | Numerical operations              |
| `matplotlib` | Core charting engine            |
| `seaborn`  | Statistical plots (violin, heatmap)|

---

## 🧹 Data Cleaning Steps

1. **Null Handling** — `director` (~9.6%) and `cast` (~5.8%) have intentional missing values (real-world data simulation)
2. **Date Parsing** — Extracted `year_added` and `month_added` from the `date_added` string column
3. **Duration Split** — Movies → `duration_min` (integer); TV Shows → `duration_seasons` (integer)
4. **Genre Explosion** — `listed_in` contains comma-separated genres; each is split and counted individually

---

## 📈 Key Findings

- **70.6%** of content is Movies; **29.4%** is TV Shows
- **United States** dominates content, followed by India and United Kingdom
- **TV-MA** is the most common rating across all titles
- Content additions peaked around **2019–2020**
- **Documentaries**, **Dramas**, and **Comedies** are the top three genres
- Average movie runtime is approximately **120 minutes**

---

## 🚀 Extending the Project

Ideas to take it further:
- Use the **real Netflix dataset** from [Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)
- Add **NLP sentiment analysis** on the description column
- Build an **interactive dashboard** with Plotly or Streamlit
- Train a **recommendation model** using content metadata
- Perform **time-series forecasting** on content addition trends

---


