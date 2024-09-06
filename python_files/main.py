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

# Load token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
YOUTUBE_API_KEY: Final[str] = os.getenv("YOUTUBE_API_KEY")
CHANNEL_IDS: Final[list[str]] = os.getenv("YOUTUBE_CHANNEL_IDS").split(',')
DISCORD_CHANNEL_ID: Final[int] = int(os.getenv("DISCORD_CHANNEL_ID"))
LAST_VIDEO_ID_FILE: Final[str] = "last_video_id.txt"
TEXT_FILES_DIR = os.path.join("..", "text_file")

# Bot setup
intents: Intents = Intents.default()
intents.message_content = True  # Needed to read messages
client: Client = Client(intents=intents)

last_video_id: str = None

# Create the directory if it doesn't exist
if not os.path.exists(TEXT_FILES_DIR):
    os.makedirs(TEXT_FILES_DIR)

# Save the last video ID to a file using the channel name
def save_last_video_id(channel_name: str, video_id: str) -> None:
    file_path = os.path.join(TEXT_FILES_DIR, f"{channel_name}_{LAST_VIDEO_ID_FILE}")
    with open(file_path, 'w') as file:
        file.write(f"{video_id}\n")

# Read the last video ID from a file using the channel name
def read_last_video_id(channel_name: str) -> str:
    file_path = os.path.join(TEXT_FILES_DIR, f"{channel_name}_{LAST_VIDEO_ID_FILE}")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.readline().strip()  # Read only the first line which contains the video ID
    return None

# Update the get_latest_video_id function to return the video ID and channel name
def get_latest_video_id(channel_id: str) -> tuple[str, str]:
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            video_id = data['items'][0]['id'].get('videoId')
            channel_name = data['items'][0]['snippet']['channelTitle']
            return video_id, channel_name
    return None, None

# Modify the check_for_new_videos function to use the channel name for file operations
async def check_for_new_videos(discord_channel: discord.TextChannel) -> None:
    for channel_id in CHANNEL_IDS:
        # Get the latest video ID and channel name
        latest_video_id, channel_name = get_latest_video_id(channel_id)

        # Read the last video ID using the channel name
        last_video_id = read_last_video_id(channel_name)

        # If there's a new video, send a notification
        if latest_video_id and latest_video_id != last_video_id:
            save_last_video_id(channel_name, latest_video_id)  # Update the last video ID in the file
            video_url = f"https://www.youtube.com/watch?v={latest_video_id}"
            await discord_channel.send(f"New video published on channel {channel_name}: {video_url}")

# Message event
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty because intents were not enabled')
        return

    is_private = user_message.startswith('?')
    if is_private:
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message, str(message.author.id))
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(f"Error: {e}")

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
        await asyncio.sleep(600)  # Check every 5 minutes
        print("10 minutes have passed, checking for new videos again.")
        print(f'The bot actualised at : {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

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