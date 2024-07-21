import discord
from datetime import datetime, timedelta

def get_prefix(bot: discord.Bot, message: discord.Message) -> str:
    """
    Gets the bot's prefix for commands.

    Args:
        bot: The Discord bot instance.
        message: The Discord message object.

    Returns:
        The bot's prefix.
    """
    config = bot.config
    prefix = config.get('prefix')
    if isinstance(message.channel, discord.DMChannel):
        return prefix
    else:
        guild_prefix = config.get('guild_prefixes', {}).get(str(message.guild.id))
        if guild_prefix:
            return guild_prefix
        else:
            return prefix

def get_user(bot: discord.Bot, user_id: int) -> discord.User:
    """
    Gets a user object from a Discord ID.

    Args:
        bot: The Discord bot instance.
        user_id: The Discord ID of the user.

    Returns:
        The user object.
    """
    user = bot.get_user(user_id)
    if user is None:
        try:
            user = bot.fetch_user(user_id)
        except discord.HTTPException:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
    return user

def get_channel(bot: discord.Bot, channel_id: int) -> discord.abc.GuildChannel:
    """
    Gets a channel object from a Discord ID.

    Args:
        bot: The Discord bot instance.
        channel_id: The Discord ID of the channel.

    Returns:
        The channel object.
    """
    channel = bot.get_channel(channel_id)
    if channel is None:
        try:
            channel = bot.fetch_channel(channel_id)
        except discord.HTTPException:
            raise ChannelNotFoundError(f"Channel with ID {channel_id} not found.")
    return channel

def get_guild(bot: discord.Bot, guild_id: int) -> discord.Guild:
    """
    Gets a guild object from a Discord ID.

    Args:
        bot: The Discord bot instance.
        guild_id: The Discord ID of the guild.

    Returns:
        The guild object.
    """
    guild = bot.get_guild(guild_id)
    if guild is None:
        try:
            guild = bot.fetch_guild(guild_id)
        except discord.HTTPException:
            raise GuildNotFoundError(f"Guild with ID {guild_id} not found.")
    return guild

def format_time(seconds: int) -> str:
    """
    Formats a time duration in seconds into HH:MM:SS format.

    Args:
        seconds: The time duration in seconds.

    Returns:
        The formatted time duration in HH:MM:SS format.
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def format_duration(seconds: int) -> str:
    """
    Formats a time duration in seconds into a human-readable string.

    Args:
        seconds: The time duration in seconds.

    Returns:
        The formatted time duration in a human-readable string.
    """
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} {seconds} seconds"
    else:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours} hour{'s' if hours > 1 else ''} {minutes} minute{'s' if minutes > 1 else ''} {seconds} seconds"

def format_timestamp(timestamp: datetime) -> str:
    """
    Formats a timestamp into a human-readable string.

    Args:
        timestamp: The timestamp.

    Returns:
        The formatted timestamp in a human-readable string.
    """
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def format_date(date: datetime) -> str:
    """
    Formats a date into a human-readable string.

    Args:
        date: The date.

    Returns:
        The formatted date in a human-readable string.
    """
    return date.strftime("%Y-%m-%d")

class UserNotFoundError(Exception):
    """Custom exception for when a user is not found."""
    pass

class ChannelNotFoundError(Exception):
    """Custom exception for when a channel is not found."""
    pass

class GuildNotFoundError(Exception):
    """Custom exception for when a guild is not found."""
    pass