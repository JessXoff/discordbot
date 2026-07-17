# Daily Prayer to Inanna — Discord Bot

Posts a fresh, Claude-generated devotional prayer to a Discord channel every
day, on autopilot. No server to run — GitHub's free scheduler does the work.

## How it fits together

- `generate_prayer.py` — calls the Anthropic API with a system prompt that
  encodes your standing constraints (no descent myth, elevated liturgical
  register, rotating themes) and posts the result to Discord via webhook.
- `.github/workflows/daily-prayer.yml` — a GitHub Actions cron job that runs
  the script once a day.

## Setup

**1. Create a Discord webhook**
In your server: channel → Edit Channel → Integrations → Webhooks → New
Webhook → copy the Webhook URL.

**2. Get an Anthropic API key**
console.anthropic.com → Settings → API Keys → Create Key.

**3. Create a GitHub repo and push these files**
```
git init
git add .
git commit -m "Daily Inanna prayer bot"
git remote add origin <your-repo-url>
git push -u origin main
```

**4. Add your secrets to the repo**
Repo → Settings → Secrets and variables → Actions → New repository secret:
- `ANTHROPIC_API_KEY`
- `DISCORD_WEBHOOK_URL`

**5. Set the posting time**
Edit the `cron` line in `daily-prayer.yml`. GitHub Actions cron runs in UTC,
so convert your preferred local time. The default (`0 12 * * *`) is noon UTC.

**6. Test it**
Repo → Actions tab → "Daily Prayer to Inanna" → Run workflow. Check your
Discord channel for the post.

That's it — from here it runs itself daily with no maintenance.

## Adjusting the liturgical constraints

Everything about tone and theme lives in `SYSTEM_PROMPT` and the `THEMES`
list at the top of `generate_prayer.py`. Add themes, adjust the epithets it
draws on, or change the length/register directly there — no other code
needs to change.

## If you want more than a daily post later

If you eventually want slash commands, rotating myth excerpts, or a sacred
calendar with feast-day-specific liturgy, that calls for a persistent bot
(e.g. discord.py) hosted somewhere always-on (Railway, Fly.io, a small VPS,
or even a Raspberry Pi at home), rather than this GitHub Actions approach.
The `generate_prayer()` function here would slot straight into that bot's
background task loop — you'd swap the webhook POST for `channel.send()` and
add a `tasks.loop(hours=24)` decorator. Worth building this simple version
first and expanding once it's running the way you like.
