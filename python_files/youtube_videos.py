import os
import requests
import discord
from typing import Final

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Define constants
YOUTUBE_API_KEY: Final[str] = os.getenv("YOUTUBE_API_KEY")
CHANNEL_IDS: Final[list[str]] = os.getenv("YOUTUBE_CHANNEL_IDS").split(',')
TEXT_FILES_DIR: Final[str] = os.path.join("..", "text_files")

# Ensure the text_files directory exists
if not os.path.exists(TEXT_FILES_DIR):
    os.makedirs(TEXT_FILES_DIR)

# Save the last video ID to a file using the channel name
def save_last_video_id(channel_name: str, video_id: str) -> None:
    file_path = os.path.join(TEXT_FILES_DIR, f"{channel_name}_last_video_id.txt")
    with open(file_path, 'w') as file:
        file.write(f"{video_id}\n")

# Read the last video ID from a file using the channel name
def read_last_video_id(channel_name: str) -> str:
    file_path = os.path.join(TEXT_FILES_DIR, f"{channel_name}_last_video_id.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.readline().strip()  # Read only the first line which contains the video ID
    return None

# Get the latest video ID and channel name
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

# Check for new videos and send notifications
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