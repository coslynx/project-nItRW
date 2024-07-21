import discord

class Embeds:
    """Handles the creation of embeds for Discord messages."""

    def error_embed(self, description: str) -> discord.Embed:
        """Creates an embed for an error message.

        Args:
            description: The error message to display.

        Returns:
            A discord.Embed object representing the error embed.
        """
        embed = discord.Embed(
            title="Error",
            description=description,
            color=discord.Color.red()
        )
        return embed

    def success_embed(self, description: str) -> discord.Embed:
        """Creates an embed for a success message.

        Args:
            description: The success message to display.

        Returns:
            A discord.Embed object representing the success embed.
        """
        embed = discord.Embed(
            title="Success",
            description=description,
            color=discord.Color.green()
        )
        return embed

    def info_embed(self, description: str) -> discord.Embed:
        """Creates an embed for an informative message.

        Args:
            description: The informative message to display.

        Returns:
            A discord.Embed object representing the info embed.
        """
        embed = discord.Embed(
            title="Info",
            description=description,
            color=discord.Color.blue()
        )
        return embed