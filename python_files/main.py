import time
from http.client import responses

import discord
from typing import Final
import os
import requests
import asyncio
from aiohttp.helpers import TOKEN
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response, user_games
from youtube_videos import check_for_new_videos

# Load token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
YOUTUBE_API_KEY: Final[str] = os.getenv("YOUTUBE_API_KEY")
CHANNEL_IDS: Final[list[str]] = os.getenv("YOUTUBE_CHANNEL_IDS").split(',')
DISCORD_CHANNEL_ID: Final[int] = int(os.getenv("DISCORD_CHANNEL_ID"))
LAST_VIDEO_ID_FILE: Final[str] = "last_video_id.txt"
TEXT_FILES_DIR = os.path.join("..", "text_files")

# Bot setup
intents: Intents = Intents.default()
intents.message_content = True  # Needed to read messages
client: Client = Client(intents=intents)

last_video_id: str = None

# Create the directory if it doesn't exist
if not os.path.exists(TEXT_FILES_DIR):
    os.makedirs(TEXT_FILES_DIR)

# Handling the startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')
    print(f'Start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

    # Get the Discord channel to send notifications to
    discord_channel = client.get_channel(DISCORD_CHANNEL_ID)

    # Check for new videos periodically
    while True:
        await check_for_new_videos(discord_channel)
        await asyncio.sleep(600)  # Check every 10 minutes
        print("10 minutes have passed, checking for new videos again.")
        print(f'The bot actualised at : {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

# Define the send_message function
async def send_message(message: Message, user_message: str) -> None:
    response = get_response(user_message)
    await message.channel.send(response)

# Handling messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    user_message: str = message.content
    user_id: str = str(message.author.id)

    # Check if the user is currently playing a game
    if user_id in user_games:
        await send_message(message, user_message)
        return

    # Check if the message starts with the prefix '!'
    if not user_message.startswith('!'):
        return

    # Remove the prefix '!' from the message
    user_message = user_message[1:]

    username: str = str(message.author)
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Run the bot
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()