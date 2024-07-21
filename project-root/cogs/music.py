import discord
from discord.ext import commands
import asyncio
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import soundcloud
from soundcloud.client import Client
import requests
from utils.music_player import MusicPlayer
from utils.errors import MusicError
from utils.helper import format_duration

# Suppress noisy YouTube DL logging
youtube_dl.utils.bug_reports_message = lambda: ''

class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.current_song = None
        self.voice_client = None
        self.music_player = None
        self.config = bot.config

        # Configure Spotify API
        self.spotify_client_id = self.config.get('spotify_client_id')
        self.spotify_client_secret = self.config.get('spotify_client_secret')
        self.spotify = self.get_spotify_client()

        # Configure SoundCloud API
        self.soundcloud_client_id = self.config.get('soundcloud_client_id')
        self.soundcloud_client_secret = self.config.get('soundcloud_client_secret')
        self.soundcloud = Client(client_id=self.soundcloud_client_id, client_secret=self.soundcloud_client_secret)

    def get_spotify_client(self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.spotify_client_id,
            client_secret=self.spotify_client_secret
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    async def play_song(self, ctx, song: dict):
        """Plays a song from the queue."""
        self.current_song = song
        try:
            if self.music_player is None:
                self.music_player = MusicPlayer(song['source'])
                await self.music_player.play_song()
            else:
                await self.music_player.stop()
                self.music_player = MusicPlayer(song['source'])
                await self.music_player.play_song()
            await ctx.send(f"Now playing: **{song['title']}** by **{song['artist']}** ({format_duration(song['duration'])})")
        except subprocess.CalledProcessError as e:
            raise MusicError(f"Error playing song: {e}")

    async def search_music(self, query: str) -> dict:
        """Searches for music using the appropriate API."""
        if 'youtube.com' in query:
            return await self.search_youtube(query)
        elif 'spotify.com' in query:
            return await self.search_spotify(query)
        elif 'soundcloud.com' in query:
            return await self.search_soundcloud(query)
        else:
            return await self.search_youtube(query)

    async def search_youtube(self, query: str) -> dict:
        """Searches for music on YouTube."""
        try:
            ydl_opts = {'format': 'bestaudio/best'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    # Playlist
                    info = info['entries'][0]
                return {
                    'source': info['url'],
                    'title': info['title'],
                    'artist': info['uploader'],
                    'duration': int(info['duration']),
                }
        except Exception as e:
            raise MusicError(f"Error searching YouTube: {e}")

    async def search_spotify(self, query: str) -> dict:
        """Searches for music on Spotify."""
        try:
            results = self.spotify.search(q=query, type='track')
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                return {
                    'source': track['external_urls']['spotify'],
                    'title': track['name'],
                    'artist': track['artists'][0]['name'],
                    'duration': int(track['duration_ms'] / 1000),
                }
            else:
                raise MusicError("No results found on Spotify.")
        except Exception as e:
            raise MusicError(f"Error searching Spotify: {e}")

    async def search_soundcloud(self, query: str) -> dict:
        """Searches for music on SoundCloud."""
        try:
            results = self.soundcloud.get('/tracks', q=query)
            if results:
                track = results[0]
                return {
                    'source': track['permalink_url'],
                    'title': track['title'],
                    'artist': track['user']['username'],
                    'duration': int(track['duration'] / 1000),
                }
            else:
                raise MusicError("No results found on SoundCloud.")
        except Exception as e:
            raise MusicError(f"Error searching SoundCloud: {e}")

    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx, *, query: str):
        """Plays a song from a URL or search query."""
        try:
            song = await self.search_music(query)
            await self.queue.put(song)
            if self.voice_client is None:
                await self.join_voice_channel(ctx)
            if self.voice_client.is_playing():
                await ctx.send(f"Added **{song['title']}** to the queue.")
            else:
                await self.play_song(ctx, song)
        except MusicError as e:
            await ctx.send(embed=self.bot.embeds.error_embed(str(e)))
        except Exception as e:
            await ctx.send(embed=self.bot.embeds.error_embed(f"An unexpected error occurred: {e}"))

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pauses the current song."""
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            await ctx.send("Paused.")
        else:
            await ctx.send("Nothing is playing.")

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resumes the paused song."""
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            await ctx.send("Resumed.")
        else:
            await ctx.send("Nothing is paused.")

    @commands.command(name='skip', aliases=['s'])
    async def skip(self, ctx):
        """Skips to the next song in the queue."""
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            await self.play_next(ctx)
        else:
            await ctx.send("Nothing is playing.")

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stops the music and disconnects from the voice channel."""
        if self.voice_client:
            await self.voice_client.disconnect()
            self.music_player = None
            self.voice_client = None
            self.current_song = None
            await ctx.send("Stopped.")
        else:
            await ctx.send("Not connected to any voice channel.")

    @commands.command(name='queue', aliases=['q'])
    async def queue(self, ctx, *, query: str = None):
        """Adds a song to the queue."""
        try:
            if query is None:
                # Show queue if no query is provided
                if self.queue.empty():
                    await ctx.send("The queue is empty.")
                else:
                    queue_list = [f"**{song['title']}** by **{song['artist']}** ({format_duration(song['duration'])})" for song in list(self.queue._queue)]
                    await ctx.send(f"**Queue:**\n{'\n'.join(queue_list)}")
                return
            song = await self.search_music(query)
            await self.queue.put(song)
            await ctx.send(f"Added **{song['title']}** to the queue.")
        except MusicError as e:
            await ctx.send(embed=self.bot.embeds.error_embed(str(e)))
        except Exception as e:
            await ctx.send(embed=self.bot.embeds.error_embed(f"An unexpected error occurred: {e}"))

    @commands.command(name='clear_queue')
    async def clear_queue(self, ctx):
        """Clears the current queue."""
        if not self.queue.empty():
            self.queue = asyncio.Queue()
            await ctx.send("Queue cleared.")
        else:
            await ctx.send("The queue is already empty.")

    @commands.command(name='now_playing', aliases=['np'])
    async def now_playing(self, ctx):
        """Displays information about the currently playing song."""
        if self.current_song:
            await ctx.send(f"Now playing: **{self.current_song['title']}** by **{self.current_song['artist']}** ({format_duration(self.current_song['duration'])})")
        else:
            await ctx.send("Nothing is playing.")

    async def join_voice_channel(self, ctx):
        """Joins the voice channel that the user is in."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            self.voice_client = await channel.connect()
            await ctx.send(f"Joined {channel.name}.")
        else:
            await ctx.send("You are not connected to a voice channel.")

    async def play_next(self, ctx):
        """Plays the next song in the queue."""
        if not self.queue.empty():
            song = await self.queue.get()
            await self.play_song(ctx, song)
        else:
            await ctx.send("Queue is empty.  Ending playback.")
            await self.voice_client.disconnect()
            self.music_player = None
            self.voice_client = None
            self.current_song = None

    async def handle_voice_disconnect(self, ctx):
        """Handles the bot disconnecting from the voice channel."""
        if self.voice_client and self.voice_client.is_connected():
            await self.voice_client.disconnect()
            self.music_player = None
            self.voice_client = None
            self.current_song = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Handles voice state updates to disconnect if the bot is alone in the channel."""
        if member == self.bot.user:
            if after.channel is None and self.voice_client is not None and self.voice_client.is_connected():
                await self.handle_voice_disconnect(None)

def setup(bot: commands.Bot):
    bot.add_cog(MusicCog(bot))