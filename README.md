
# Financially Free Task: Vehicle Registration Investor Dashboard

**Live Demo:** [Streamlit Deployed App](https://krvatsal-financially-free-task-dashboardapp-es8fca.streamlit.app/)

## Project Overview

This project provides a professional, investor-focused dashboard for analyzing India's vehicle registration data (from the Vahan Dashboard). It enables deep-dive analytics into Four Wheeler, Three Wheeler, and Two Wheeler segments, with advanced growth metrics, filtering, and visualizations tailored for market research and investment analysis.

**Key Features:**
- Unified dashboard for Four, Three, and Two Wheeler data
- Year-over-Year (YoY) and Quarter-over-Quarter (QoQ) growth analytics
- Dynamic filters for year and vehicle class
- Cumulative (Till date) handling for accurate investor metrics
- Interactive charts (trend, share, growth, pivot tables)
- Downloadable filtered data
- Extensible for new vehicle types and metrics

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/krVatsal/financially-free-task.git
cd financially-free-task
```

### 2. Install dependencies (recommended: Poetry)
If you don't have Poetry:
```bash
pip install poetry
```
Then install all dependencies:
```bash
poetry install
```

Or, using pip (not recommended for development):
```bash
pip install -r requirements.txt
```

### 3. Prepare the database
The dashboard uses SQLite for fast analytics. To load the data:
```bash
cd dashboard
python db_utils.py
```
This will import all CSVs (four_wheeler_data.csv, three_wheeler_data.csv, two_wheeler_data.csv) into `vehicle_data.db`.

### 4. Run the dashboard
```bash
streamlit run dashboard/app.py
```
Or, if using Poetry:
```bash
poetry run streamlit run dashboard/app.py
```


## Data Assumptions
- Data is stored in CSVs: `four_wheeler_data.csv`, `three_wheeler_data.csv`, `two_wheeler_data.csv` (in the `dashboard/` folder)
- Each file must have columns: `Year`, `Vehicle Class`, and segment-specific columns (e.g., `2WIC`, `2WN`, `2WT`, `TOTAL` for two-wheelers)
- The dashboard expects the column names to match exactly (case-sensitive)
- The 'Year' column can include 'Till date' for cumulative data, which is handled specially in analytics
- Data should be annual (one row per vehicle class per year)
- No missing values in key columns (`Year`, `Vehicle Class`, `TOTAL`)

## Feature Roadmap
- [x] Unified dashboard for Four, Three, and Two Wheeler data
- [x] YoY and QoQ growth analytics
- [x] Dynamic filters for year and vehicle class
- [x] Cumulative (Till date) handling
- [x] Interactive charts and pivot tables
- [x] Downloadable filtered data
- [x] SQLite backend for fast analytics
- [ ] Automated data scraping from Vahan Dashboard
- [ ] More advanced investor analytics (e.g., risk metrics, market share trends)
- [ ] User authentication for private dashboards

## Extending the Dashboard
- To add a new vehicle type, add a new CSV in the same format and update the `table_map` in `app.py`
- Metrics and visuals are dynamic and will adapt to new vehicle types

## Deployed App
You can try the dashboard live here: [Streamlit Deployed App](https://krvatsal-financially-free-task-dashboardapp-es8fca.streamlit.app/)

---

For questions, improvements, or feature requests, please open an issue.
