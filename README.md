# naira-pulse

A financial news pipeline that scrapes Nairametrics for relevant Nigerian financial news and delivers it to a Telegram channel automatically, every 10 minutes.

## What it does

naira-pulse polls the Nairametrics API on a fixed interval, filters articles by financial keywords, deduplicates against previously seen news, and sends each new article to a configured Telegram chat — with its featured image when available.

## Project structure

```
naira-pulse/
├── Procfile
├── requirements.txt
├── docs/
│   └── TELEGRAM_SETUP.md    # Guide for creating a bot and getting your chat ID
├── pipeline/
│   ├── __main__.py          # Entry point
│   ├── app.py               # Pipeline orchestrator
│   ├── scraper.py           # Fetches posts from Nairametrics API
│   ├── processor.py         # Deduplication and keyword filtering
│   ├── formatter.py         # Formats news items into Telegram messages
│   ├── telegram.py          # Telegram bot wrapper
│   ├── store.py             # Persists seen news to JSON
│   ├── filters.py           # Financial keyword list
│   └── aliases.py           # Shared type aliases
```

## Filter coverage

The pipeline filters news by keywords including but not limited to: CBN, naira, forex, inflation, interest rate, monetary policy, fintech, payment, remittance, and major Nigerian banks such as Access Bank, GTBank, Zenith Bank, UBA, First Bank, and fintechs like OPay, PalmPay, and Kuda.

## Requirements

- Python 3.10 or higher
- A Telegram bot token from BotFather
- The chat ID of the target Telegram group or channel

If you do not have these set up yet, see the [Telegram Setup Guide](docs/TELEGRAM_SETUP.md) for step-by-step instructions on creating a bot and retrieving your chat ID.

## Environment variables

| Variable | Description |
|---|---|
| `TG_NEWS_BOT_TOKEN` | Your Telegram bot token |
| `TG_CHAT_ID` | Target chat or group ID |

## Running locally

```bash

git clone https://github.com/Haashiraaa/naira-pulse.git
cd naira-pulse

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TG_NEWS_BOT_TOKEN=your_token_here
export TG_CHAT_ID=your_chat_id_here

# Run
python -m pipeline
```

## Deployment

The project is configured for Railway deployment. Connect the repository to a Railway project, set the environment variables in the Railway dashboard, and the worker process will start automatically using the Procfile.

```
worker: python -m pipeline
```

The pipeline runs on a 600 second (10 minute) interval. On failure it retries up to 3 times before stopping.

## Dependencies

- `requests` — HTTP client for API and Telegram calls
- `haashi-pkg` — Internal utility library for logging and file handling
