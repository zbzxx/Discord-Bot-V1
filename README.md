
# Discord-Bot-V1

Discord-Bot-V1 is a multifunctional Discord bot that provides various utilities and fun features for Genshin Impact players, YouTube enthusiasts, and general Discord users. The bot offers optimal builds for Genshin Impact characters, sends notifications when a YouTube video is published, includes a simple points-based game, and features a password generator.

## Features

- **Genshin Impact Character Build**: Retrieves and displays the optimal build for a selected Genshin Impact character, including recommended artifacts, weapons, and stats.
- **YouTube Notifications**: Sends a notification to a channel whenever a new video is published on a specific YouTube channel.
- **Points-Based Game**: A simple game where users can accumulate points through interaction with the bot.
- **Password Generator**: Generates a strong password on request, helping users create secure passwords.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/zbzxx/Discord-Bot-V1.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Discord-Bot-V1
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables. Add your bot token and any necessary API keys in a `.env` file:
   ```
   DISCORD_TOKEN=your-discord-token
   YOUTUBE_API_KEY=your-youtube-api-key
   ```

5. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

### Genshin Impact Character Build Command
To retrieve the optimal build for a Genshin Impact character, use the following command:
```
-gc [character name]
```

### YouTube Notifications
The bot will automatically notify a designated channel when a new video is posted on a specified YouTube channel. Configure the channel and YouTube channel ID in the bot's settings.

### Points-Based Game
Users can participate in a simple game to earn points. Commands include:
- `!points`: Check your current points.
- `!play`: Participate in the game and earn points.

### Password Generator
Generate a strong password using the following command:
```
!password
```

## Dependencies

- `discord.py`: For interacting with the Discord API.
- `requests`: For API requests to external services like YouTube.
- `dotenv`: To manage environment variables.
- `genshin.py`: To retrieve Genshin Impact character build data.
  
## Future Development

- Additional mini-games with more complex mechanics.
- Support for more Genshin Impact characters and builds.
- Enhanced YouTube integration with channel-specific settings.

## Contributing

Feel free to fork the repository and submit pull requests. All contributions are welcome!

## License

This project is licensed under the MIT License.
