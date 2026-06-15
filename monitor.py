import os
import json
import requests
from playwright.sync_api import sync_playwright

URL = "https://zealy.io/cw/bastard/questboard"

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

QUEST_FILE = "known_quests.json"

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    text = page.locator("body").inner_text()

    browser.close()

lines = [line.strip() for line in text.split("\n")]
lines = [line for line in lines if len(line) > 8]

quests = []

for line in lines:
    if (
        "Xp" not in line
        and "Home" not in line
        and "Leaderboard" not in line
        and "Connect to Zealy" not in line
        and "Daily Challenge" not in line
        and line not in quests
    ):
        quests.append(line)

try:
    with open(QUEST_FILE, "r") as f:
        old_quests = json.load(f)
except:
    old_quests = []

new_quests = [q for q in quests if q not in old_quests]

if old_quests:
    for quest in new_quests:
        send_telegram(
            f"🆕 New Bastard Quest Detected!\n\n{quest}\n\n{URL}"
        )

with open(QUEST_FILE, "w") as f:
    json.dump(quests, f, indent=2)
