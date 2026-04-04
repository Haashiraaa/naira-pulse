# Telegram Setup Guide

This guide covers how to create a Telegram bot and retrieve the chat ID needed to run naira-pulse.

---

## Part 1 - Creating a Telegram bot

**Step 1.** Open Telegram and search for `@BotFather`.

**Step 2.** Start a chat with BotFather and send the command:
```
/newbot
```

**Step 3.** BotFather will ask for a name for your bot. This is the display name that appears in chats. Enter anything you like, for example:
```
Naira Pulse News
```

**Step 4.** BotFather will then ask for a username. This must be unique across all of Telegram and must end in `bot`. For example:
```
nairapulse_bot
```

**Step 5.** BotFather will respond with your bot token. It looks like this:
```
123456789:AAGf0OpcWpryF6P3uHqQFsa7JmTr10quEBo
```

Copy this token and store it somewhere safe. This is your `TG_NEWS_BOT_TOKEN` environment variable. Do not share it publicly or commit it to version control.

---

## Part 2 - Getting your chat ID

The chat ID tells the bot where to send messages. The process differs slightly depending on whether you are sending to a private chat or a group.

### Option A - Private chat (just yourself)

**Step 1.** Search for your bot by its username on Telegram and start a chat with it.

**Step 2.** Send any message to the bot, for example:
```
/start
```

**Step 3.** Open this URL in your browser, replacing `YOUR_BOT_TOKEN` with your actual token:
```
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

**Step 4.** Look for the `"chat"` object in the JSON response. Your chat ID is the number next to `"id"`:
```json
"chat": {
    "id": 123456789,
    ...
}
```

This number is your `TG_CHAT_ID`.

---

### Option B - Group chat (recommended for teams)

**Step 1.** Create a Telegram group and add your team members.

**Step 2.** Add your bot to the group by opening the group, tapping the group name, selecting Add Members, and searching for your bot username.

**Step 3.** Make the bot an administrator of the group so it has permission to post messages. Go to group settings, tap Administrators, tap Add Administrator, and select your bot.

**Step 4.** Send any message in the group, for example:
```
/start
```

**Step 5.** Open this URL in your browser:
```
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

**Step 6.** Find the `"chat"` object in the response. For groups, the ID will be a negative number:
```json
"chat": {
    "id": -1001234567890,
    ...
}
```

This negative number is your `TG_CHAT_ID`. Make sure to include the minus sign when setting the environment variable.

---

## Part 3 - Setting environment variables

Once you have both values, set them as environment variables before running the pipeline.

### Locally

```bash
export TG_NEWS_BOT_TOKEN=your_token_here
export TG_CHAT_ID=your_chat_id_here
```

### On Railway

1. Open your Railway project
2. Select your worker service
3. Go to the Variables tab
4. Add `TG_NEWS_BOT_TOKEN` and `TG_CHAT_ID` with their respective values

---

## Troubleshooting

**getUpdates returns an empty result**
This means the bot has not received any messages yet. Send a message in the chat or group and refresh the URL.

**Bot is not sending messages to the group**
Make sure the bot has been added as an administrator with permission to post messages. Bots cannot send messages to groups unless they are a member with posting rights.

**Bot token was exposed**
If your token is ever shared publicly, revoke it immediately. Open BotFather, send `/mybots`, select your bot, tap API Token, then tap Revoke. Update the new token in your environment variables.
