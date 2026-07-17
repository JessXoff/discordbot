"""
Generates a daily devotional prayer to Inanna using the Anthropic API,
then posts it to a Discord channel via webhook.

Run manually with:
    ANTHROPIC_API_KEY=... DISCORD_WEBHOOK_URL=... python generate_prayer.py
"""

import os
import random
from datetime import datetime, timezone

import requests

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

MODEL = "claude-sonnet-5"

# Themes rotate day to day so the prayers don't feel repetitive.
# Add to this list any time you want more variety.
THEMES = [
    "wholeness over purity",
    "self-confidence and radiance",
    "the virtue of seeking counsel and wisdom from others",
    "transforming a petition for vengeance into a petition for justice",
]

SYSTEM_PROMPT = """You compose a single daily devotional prayer to Inanna, \
Queen of Heaven, for a small worship community.

Fixed constraints, always follow:
- Never reference her descent to the underworld or Ereshkigal in any way.
- Write in an elevated liturgical register drawing on Sumerian epithets \
(e.g. Queen of Heaven, Lady of the me, Morning and Evening Star, First \
Daughter of Sin) and invoke the me (divine ordinances) where it fits \
naturally.
- The prayer should be 12-20 lines, addressed directly to Inanna in second \
person, and suitable to be read aloud in a group setting.
- Vary sentence structure and opening lines each time; do not fall into a \
template.
- Output ONLY the prayer text. No title, no preamble, no explanation.
"""


def generate_prayer() -> str:
    theme = random.choice(THEMES)
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": MODEL,
            "max_tokens": 600,
            "system": SYSTEM_PROMPT,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Compose today's prayer, dated {today}. "
                        f"Center it on this theme: {theme}."
                    ),
                }
            ],
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return "".join(
        block["text"] for block in data["content"] if block["type"] == "text"
    ).strip()


def post_to_discord(prayer_text: str) -> None:
    today_display = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")
    payload = {
        "embeds": [
            {
                "title": f"Prayer to Inanna — {today_display}",
                "description": prayer_text,
                "color": 0xC9A227,  # gold
            }
        ]
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=15)
    response.raise_for_status()


if __name__ == "__main__":
    prayer = generate_prayer()
    post_to_discord(prayer)
    print("Posted:\n")
    print(prayer)
