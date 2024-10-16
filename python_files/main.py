import time
import requests
from typing import Final
import os
import asyncio
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
TWITCH_CHANNEL_ID: Final[int] = int(os.getenv("TWITCH_CHANNEL_ID"))
YOUTUBE_ROLE_ID: Final[int] = int(os.getenv("YOUTUBE_ROLE_ID"))
LAST_VIDEO_ID_FILE: Final[str] = "last_video_id.txt"
TEXT_FILES_DIR = os.path.join("..", "text_files")

# Bot setup
intents: Intents = Intents.default()
intents.message_content = True  # Needed to read messages
client: Client = Client(intents=intents)

last_video_id: str = ""

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
        await check_for_new_videos(discord_channel, YOUTUBE_ROLE_ID)
        await asyncio.sleep(600)  # Check every 10 minutes
        print("10 minutes have passed, checking for new videos again.")
        print(f'The bot actualised at : {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

# Define the send_message function
async def send_message(message: Message, user_message: str) -> None:
    response = get_response(user_message)
    await message.channel.send(response)

# Handling messages
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

    if user_message.startswith('-gc'):
        if len(user_message) < 4:
            await message.channel.send("Please provide a character name after '-gc'.")
            return
        character_name = user_message[4:].strip()
        build_response = await get_genshin_build(character_name)
        await message.channel.send(build_response)
        return

    # Check if the message starts with the prefix '!'
    if user_message.startswith('!'):
        user_message = user_message[1:]  # Retire le préfixe '!'
        response = get_response(user_message, user_id)  # Assurez-vous de passer user_id ici
        await message.channel.send(response)
        return



async def get_genshin_build(character_name: str) -> str:
    try:
        url = f'http://127.0.0.1:5000/builds/{character_name}'
        response = requests.get(url)

        if response.status_code == 200:
            build_data = response.json()

            # Assurez-vous que toutes les clés existent
            if 'top_weapons' not in build_data or 'artifacts' not in build_data or 'talents' not in build_data:
                return f"Build data for '{character_name}' is incomplete."

            build_message = f"**{character_name.capitalize()} Build**\n"
            build_message += f"**Top Weapons**: {', '.join(build_data.get('top_weapons', []))}\n"
            build_message += f"**Artifact Set**: {build_data['artifacts'].get('set_name', 'N/A')}\n"

            build_message += "**Main Stats**:\n"
            for artifact in ['flower', 'feather', 'sands', 'goblet', 'circlet']:
                main_stat = build_data['artifacts'].get(artifact, {}).get('main_stat', 'N/A')
                substats = build_data['artifacts'].get(artifact, {}).get('substats', [])
                build_message += f"  - {artifact.capitalize()}: {main_stat} (Substats: {', '.join(substats)})\n"

            build_message += "\n**Talents**:\n"
            build_message += f"{', '.join(build_data.get('talents', []))}\n"

            return build_message
        else:
            return f"Character '{character_name}' not found."
    except requests.exceptions.RequestException as req_err:
        return f"Request error: {req_err}"
    except Exception as e:
        return f"An error occurred: {e}"


# Run the bot
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()