# Melody: Discord Music Bot

## Project Overview

Melody is a Discord music bot designed to enhance the social experience within Discord servers by providing a user-friendly and versatile music playback platform. This bot offers a wide range of features, including music playback from various sources (YouTube, Spotify, SoundCloud), voice channel integration, search and selection, queue management, customization options, and moderation tools.

## Features

* **Music Playback:**
    * Plays music from various sources like YouTube, Spotify, and SoundCloud.
    * Supports multiple audio formats, including MP3, WAV, and FLAC.
    * Offers basic playback controls like play, pause, skip, and stop.
    * Provides information about the current track, like title, artist, and duration.
* **Voice Channel Integration:**
    * Connects to voice channels on Discord servers, playing music for all connected users.
    * Provides commands to join and leave voice channels.
    * Detects when a user joins or leaves a voice channel, automatically adjusting playback.
* **Search and Selection:**
    * Allows users to search for music using keywords or links.
    * Provides a list of relevant results for selection, including song title, artist, and duration.
    * Handles ambiguous searches, offering suggestions and refinement options.
* **User Interaction:**
    * Enables users to control the bot through simple commands.
    * Offers a clear and intuitive interface for interacting with music playback.
    * Provides help information and guidance for using the bot.
* **Queue Management:**
    * Allows users to add tracks to a queue for continuous playback.
    * Provides options for viewing and managing the queue, including removing tracks, rearranging the order, and clearing the queue.
    * Enables users to control the order of playback within the queue.
* **Customizations:**
    * Offers options for customizing the bot's appearance and behavior.
    * Allows for setting volume levels, playback preferences, and other settings.
    * Enables server admins to control the bot's access and usage, including restricted commands or limited functionality for specific roles.
* **Moderation:**
    * Incorporates moderation tools to manage music requests and prevent inappropriate content.
    * Enables server admins to control the bot's access and usage.
    * Monitors user activity and implements measures to prevent spam or disruptive behavior.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/Melody.git
   ```
2. **Install Dependencies:**
   ```bash
   cd Melody
   pip install -r requirements.txt
   ```
3. **Set Up Environment Variables:**
    * Create a `.env` file in the project root directory.
    * Add the following environment variables (replace placeholders with your actual values):
        * `DISCORD_TOKEN`: Your Discord bot token.
        * `PREFIX`: The command prefix for the bot (e.g., `!`).
        * `DATABASE_PATH`: The path to your SQLite database file (e.g., `melody.db`).
        * `YOUTUBE_API_KEY`: Your YouTube Data API v3 key.
        * `SPOTIFY_CLIENT_ID`: Your Spotify Web API client ID.
        * `SPOTIFY_CLIENT_SECRET`: Your Spotify Web API client secret.
        * `SOUNDCLOUD_CLIENT_ID`: Your SoundCloud API client ID.
        * `SOUNDCLOUD_CLIENT_SECRET`: Your SoundCloud API client secret.
4. **Run the Bot:**
   ```bash
   python main.py
   ```

## Usage

* **Join a Voice Channel:**
    * Use the command `!join` to have the bot join the voice channel you're currently in.
* **Play Music:**
    * Use the command `!play <search query>` or `!play <URL>` to play a song.
    * Example:
        * `!play Billie Eilish Bad Guy`
        * `!play https://www.youtube.com/watch?v=MV2iW0zbd5U`
* **Control Playback:**
    * `!pause`: Pauses the current song.
    * `!resume`: Resumes playback of the paused song.
    * `!skip`: Skips to the next song in the queue.
    * `!stop`: Stops the music and disconnects from the voice channel.
* **Manage Queue:**
    * `!queue`: Shows the current queue.
    * `!queue <search query>` or `!queue <URL>`: Adds a song to the queue.
    * `!clear_queue`: Clears the current queue.
* **Now Playing:**
    * `!now_playing` or `!np`: Shows information about the currently playing song.

## Contributing

Contributions are welcome! To contribute to Melody:

1. **Fork the Repository:** Create a fork of the repository on GitHub.
2. **Create a Branch:** Create a new branch for your changes.
3. **Make Changes:** Implement your changes and write clear, concise commit messages.
4. **Test Changes:** Ensure your changes work as expected and pass all tests.
5. **Submit a Pull Request:** Submit a pull request to the original repository.

## License

Melody is licensed under the MIT License. See the `LICENSE` file for more details.