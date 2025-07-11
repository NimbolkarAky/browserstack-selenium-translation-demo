import os
import threading
import csv
from dotenv import load_dotenv
from selenium import webdriver
from utils.translator_util import translate_texts, analyze_word_frequency

load_dotenv()
REMOTE_URL = "https://hub-cloud.browserstack.com/wd/hub"

# Device/browser configurations
CONFIGS = [
    {
        "browser": "Chrome",
        "os": "Windows",
        "osVersion": "10",
        "device": None,
        "browserVersion": "latest",
        "name": "Chrome_Windows_Test"
    },
    {
        "browser": "Firefox",
        "os": "Windows",
        "osVersion": "10",
        "device": None,
        "browserVersion": "latest",
        "name": "Firefox_Windows_Test"
    },
    {
        "browser": "Safari",
        "os": "OS X",
        "osVersion": "Monterey",
        "device": None,
        "browserVersion": "latest",
        "name": "Safari_OSX_Test"
    },
    {
        "browser": "chrome",
        "os": "android",
        "device": "Samsung Galaxy S21",
        "realMobile": True,
        "name": "Samsung_Galaxy_S21_Test"
    },
    {
        "browser": "safari",
        "os": "ios",
        "device": "iPhone 13",
        "realMobile": True,
        "name": "iPhone_13_Test"
    }
]

def create_driver(config):
    name = config.get("name", "Test")
    browser = config.get("browser")

    if browser.lower() == "chrome":
        options = webdriver.ChromeOptions()
    elif browser.lower() == "firefox":
        options = webdriver.FirefoxOptions()
    elif browser.lower() == "safari":
        options = webdriver.SafariOptions()
    else:
        options = webdriver.ChromeOptions()

    bstack_options = {
        "os": config.get("os"),
        "osVersion": config.get("osVersion"),
        "deviceName": config.get("device"),
        "realMobile": config.get("realMobile", False),
        "sessionName": name,
        "buildName": "browserstack-build-1",
        "userName": os.getenv("BROWSERSTACK_USERNAME"),
        "accessKey": os.getenv("BROWSERSTACK_ACCESS_KEY")
    }

    bstack_options = {k: v for k, v in bstack_options.items() if v is not None}
    options.set_capability("bstack:options", bstack_options)
    options.set_capability("browserName", browser)
    options.set_capability("browserVersion", config.get("browserVersion", "latest"))

    driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
    return driver

def scrape_titles(config, titles):
    name = config.get("name")
    try:
        driver = create_driver(config)
        driver.implicitly_wait(10)
        driver.get("https://elpais.com/opinion/")
        elements = driver.find_elements("css selector", "h2")
        for el in elements[:2]:
            titles.append(el.text)
        driver.quit()
    except Exception as e:
        print(f"[Thread {name}] BrowserStack connection failed: {e}")

def save_to_csv(translated_titles):
    with open("translated_titles.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Original", "Translated"])
        for pair in translated_titles:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                writer.writerow(pair)

def main():
    all_titles = []
    threads = []

    print("\n")
    for config in CONFIGS:
        thread = threading.Thread(target=scrape_titles, args=(config, all_titles))
        threads.append(thread)
        print(f"🚀 Starting test in thread {config['name']}")
        thread.start()

    for thread in threads:
        thread.join()

    print("✅ All scraping tasks completed.")
    translated_pairs = translate_texts(all_titles[:8])  # API limit
    save_to_csv(translated_pairs)
    print("✅ Titles translated and saved to translated_titles.csv")

    if translated_pairs:
        clean_pairs = [pair for pair in translated_pairs if isinstance(pair, (list, tuple)) and len(pair) == 2]
        analyze_word_frequency([t for _, t in clean_pairs])

if __name__ == "__main__":
    main()