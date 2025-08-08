# Dashboard Project: Vehicle Registration Data (Investor View)

## Setup Instructions

1. **Install dependencies:**
   - Python 3.8+
   - Install required packages:
     ```bash
     pip install streamlit pandas openpyxl
     ```

2. **Run the dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```

3. **Upload Data:**
   - Use the sidebar to upload a Vahan Dashboard data file (CSV or Excel).
   - The file should have columns: `date`, `vehicle_category`, `manufacturer`, `registrations` (case-insensitive).

## Data Assumptions
- The uploaded data contains at least: `date`, `vehicle_category`, `manufacturer`, `registrations`.
- Dates are in a standard format (YYYY-MM-DD preferred).
- Data is at least monthly granularity.

## Feature Roadmap
- [x] YoY and QoQ growth by category and manufacturer
- [x] Date range, category, and manufacturer filters
- [x] Trend graphs and % change
- [ ] Automated data scraping from Vahan Dashboard
- [ ] Export graphs/tables
- [ ] More advanced investor analytics

## Data Collection/Scraping
- If data is not directly downloadable, use Python (e.g., `requests`, `BeautifulSoup`) to scrape the Vahan Dashboard. Document the script and steps in a separate file.

## Video Walkthrough
- Record a short (max 5 min) screen recording explaining:
  - What you built
  - How to use the dashboard
  - Key investor insights
- Upload to YouTube (unlisted) or Google Drive and share the link in your submission.

---

For questions or improvements, see the `Feature Roadmap` above or open an issue.
