class BotError(Exception):
    """Base class for all custom errors in the bot."""
    pass


class CommandError(BotError):
    """Error class for command-related issues."""
    pass


class MusicError(BotError):
    """Error class for music playback-related issues."""
    pass


class DatabaseError(BotError):
    """Error class for database-related issues."""
    pass