# Botenio - Telegram Bot

This is a Telegram bot written in Python. It can be run in a virtual environment or on Docker.

## Requirements

- Python 3.6 or higher
- virtualenv (optional)

## Setup

1. Clone this repository
2. Create a virtual environment and activate it (optional but recommended)
3. Install the required dependencies using `pip install -r requirements.txt`
4. Add the following environment variables:
   - FROM_EMAIL
   - FROM_PWD
   - TELEGRAM_TOKEN
   - TWITTER_TOKEN
   - SHODAN_API_KEY
   - ADMIN_CHAT_ID
5. Run the bot using `python bot.py`

## Running on Docker

1. Build the Docker image using `docker build -t telegram-bot .`
2. Run the Docker container using `docker run -d --name bot -e FROM_EMAIL=<email> -e FROM_PWD=<password> -e TELEGRAM_TOKEN=<token> -e TWITTER_TOKEN=<token> -e SHODAN_API_KEY=<key> -e ADMIN_CHAT_ID=<id> telegram-bot`
3. The bot should now be running in the background. You can view its logs using `docker logs bot`

## Usage

Once the bot is running, you can interact with it using Telegram.

Note that the `ADMIN_CHAT_ID` environment variable should be set to the ID of the chat where the bot is being used. This is used to restrict certain commands to only be available in that chat.
