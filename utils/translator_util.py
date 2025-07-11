import os
import requests
from dotenv import load_dotenv
from collections import Counter
import re

load_dotenv()

API_URL = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "content-type": "application/json",
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

def translate_texts(texts, source="es", target="en"):
    translated = []
    for text in texts:
        try:
            response = requests.post(API_URL, json={
                "q": text,
                "source": source,
                "target": target
            }, headers=HEADERS, timeout=10)

            if response.status_code == 200:
                data = response.json()
                translated_text = data["data"]["translations"]["translatedText"]
                translated.append((text, translated_text))
            else:
                print(f"[Translation Error] {response.status_code} {response.reason}")
                translated.append((text, ""))
        except Exception as e:
            print(f"[Translation Error] {e}")
            translated.append((text, ""))
    return translated

def analyze_word_frequency(translated_titles):
    all_words = []
    for title in translated_titles:
        if isinstance(title, str):
            words = re.findall(r'\b\w+\b', title.lower())
            all_words.extend(words)

    word_counts = Counter(all_words)
    print("\n🔍 Repeated Words (more than 2 times):")
    for word, count in word_counts.items():
        if count > 2:
            print(f"{word}: {count}")
