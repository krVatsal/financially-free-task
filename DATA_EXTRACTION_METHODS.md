# Data Extraction Methods for Vahan Dashboard

This document summarizes the approaches attempted to extract vehicle registration data from the Vahan Dashboard, and the challenges encountered with each method.

## 1. Scrapy (Initial Attempt)
- **Tool:** [Scrapy](https://scrapy.org/)
- **Reason for Choice:** Scrapy is a powerful Python framework for web scraping, especially for static or lightly dynamic sites.
- **Outcome:**
  - The Vahan Dashboard is a JavaScript-heavy website.
  - Scrapy could not render or interact with the dynamic content loaded via JavaScript.
  - As a result, the required data tables and dropdowns were not accessible in the HTML responses.
- **Status:** ❌ Not feasible for this site.

## 2. Selenium (Second Attempt)
- **Tool:** [Selenium](https://www.selenium.dev/)
- **Reason for Choice:** Selenium automates browsers and can interact with JavaScript-heavy websites, simulating real user actions.
- **Outcome:**
  - Selenium was able to load the Vahan Dashboard and interact with some elements.
  - However, a bug in the Vahan Sewa website caused the vehicle type dropdown to reset to "Four Wheeler" every time the page was refreshed or a new selection was made.
  - This made it impossible to reliably extract data for other vehicle types (e.g., Three Wheeler, Two Wheeler) in an automated fashion.
- **Status:** ❌ Not feasible due to site-specific bug.

## 3. Manual Extraction (Final Approach)
- **Method:** Manually copied and cleaned data from the Vahan Dashboard for each vehicle type and year.
- **Reason for Choice:** Automation was not possible due to the above limitations.
- **Outcome:**
  - Data for Four Wheeler, Three Wheeler, and Two Wheeler was manually extracted and formatted into CSV files for use in the dashboard.
- **Status:** ✅ Successful (manual process)

---

**Summary:**
- Automated scraping was not possible due to a combination of JavaScript-heavy content and a dropdown reset bug on the Vahan Sewa website.
- Manual extraction was used to ensure data completeness and accuracy for the dashboard.
