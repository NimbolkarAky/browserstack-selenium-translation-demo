\# BrowserStack + Selenium + Translation Automation Project



\## 🔍 Overview

This project demonstrates an end-to-end automation pipeline that:

\- Uses Selenium with BrowserStack to scrape headlines from \[El País - Opinión](https://elpais.com/opinion/)

\- Translates headlines from Spanish to English using Deep Translate API (via RapidAPI)

\- Analyzes word frequency of the translated text

\- Supports parallel testing on desktop and mobile platforms



\## ⚙️ Technologies Used

\- Python 3.11

\- Selenium 4

\- BrowserStack Automate

\- Deep Translate API (via RapidAPI)

\- `dotenv` for managing secrets

\- `csv` for data export



\## 📁 Project Structure

\- `main.py`: Entry point for parallel execution and orchestration

\- `utils/translator\_util.py`: Contains translation and analysis functions

\- `.env`: Stores API keys securely (not committed)

\- `requirements.txt`: Python dependencies



\## 🌐 Cross-Browser Coverage

\- Chrome on Windows 10

\- Firefox on Windows 10

\- Safari on macOS Monterey

\- Samsung Galaxy S21 (Android)

\- iPhone 13 (iOS)



\## 🚧 Challenges Faced

\- Handling outdated Selenium capability methods (`desired\_capabilities`)

\- Resolving `NoneType` errors due to misconfigured `bstack:options`

\- Managing API limits and avoiding 502/504 rate-limit issues

\- Ensuring thread safety during title scraping



\## ✅ Output

Translated headlines are saved to `translated\_titles.csv`, and common words occurring more than twice are printed.



\## 🔐 Environment Variables

Create a `.env` file with the following keys:



```env

RAPIDAPI\_KEY=your\_rapidapi\_key

RAPIDAPI\_HOST=deep-translate1.p.rapidapi.com

BROWSERSTACK\_USERNAME=your\_browserstack\_username

BROWSERSTACK\_ACCESS\_KEY=your\_browserstack\_key



