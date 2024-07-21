import discord
from discord.ext import commands
import requests
from utils.database import Database
from utils.errors import CommandError
from utils.helper import get_prefix
from utils.embeds import Embeds

class AdminCog(commands.Cog):
    """Cog for handling administrative commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = bot.config
        self.database = Database(self.config.get('database_path'))
        self.database.connect()  # Connect to the database
        self.embeds = Embeds()  # Initialize embed class

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        """Loads a cog."""
        try:
            self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(embed=self.embeds.success_embed(f'Loaded cog: {cog}'))
        except Exception as e:
            await ctx.send(embed=self.embeds.error_embed(f'Failed to load cog: {cog}\n{e}'))

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        """Unloads a cog."""
        try:
            self.bot.unload_extension(f'cogs.{cog}')
            await ctx.send(embed=self.embeds.success_embed(f'Unloaded cog: {cog}'))
        except Exception as e:
            await ctx.send(embed=self.embeds.error_embed(f'Failed to unload cog: {cog}\n{e}'))

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        """Reloads a cog."""
        try:
            self.bot.reload_extension(f'cogs.{cog}')
            await ctx.send(embed=self.embeds.success_embed(f'Reloaded cog: {cog}'))
        except Exception as e:
            await ctx.send(embed=self.embeds.error_embed(f'Failed to reload cog: {cog}\n{e}'))

    @commands.command(name='blacklist')
    @commands.has_permissions(administrator=True)
    async def blacklist(self, ctx, user: discord.Member):
        """Blacklists a user from using the bot."""
        if user == self.bot.user:
            raise CommandError("You can't blacklist me!")

        try:
            self.database.add_blacklist(user.id)
            await ctx.send(embed=self.embeds.success_embed(f"Blacklisted {user.mention} from using the bot."))
        except Exception as e:
            await ctx.send(embed=self.embeds.error_embed(f"Failed to blacklist {user.mention}:\n{e}"))

    @commands.command(name='unblacklist')
    @commands.has_permissions(administrator=True)
    async def unblacklist(self, ctx, user: discord.Member):
        """Removes a user from the blacklist."""
        try:
            self.database.remove_blacklist(user.id)
            await ctx.send(embed=self.embeds.success_embed(f"Unblacklisted {user.mention}."))
        except Exception as e:
            await ctx.send(embed=self.embeds.error_embed(f"Failed to unblacklist {user.mention}:\n{e}"))

    @commands.command(name='whitelist')
    @commands.has_permissions(administrator=True)
    async def whitelist(self, ctx, user: discord.Member):
        """Whitelists a user to use the bot."""
        if user == self.bot.user:
            raise CommandError("You can't whitelist me!")

        try:
            self.database.add_whitelist(user.id)
            await ctx.send(embed=self.embeds.success_embed(f"Whitelisted {user.mention} to use the bot."))
        except Exception as e:
            await ctx.send(embed=self.embeds.error_embed(f"Failed to whitelist {user.mention}:\n{e}"))

    @commands.command(name='unwhitelist')
    @commands.has_permissions(administrator=True)
    async def unwhitelist(self, ctx, user: discord.Member):
        """Removes a user from the whitelist."""
        try:
            self.database.remove_whitelist(user.id)
            await ctx.send(embed=self.embeds.success_embed(f"Unwhitelisted {user.mention}."))
        except Exception as e:
            await ctx.send(embed=self.embeds.error_embed(f"Failed to unwhitelist {user.mention}:\n{e}"))

    @commands.command(name='set_prefix')
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix: str):
        """Sets a custom prefix for the bot in this server."""
        if len(prefix) > 5:
            raise CommandError("Prefix cannot be longer than 5 characters.")
        if not prefix.isalnum():
            raise CommandError("Prefix must be alphanumeric.")

        try:
            self.config.set('guild_prefixes', {str(ctx.guild.id): prefix})
            self.config.save()
            await ctx.send(embed=self.embeds.success_embed(f'Prefix set to: `{prefix}`'))
        except Exception as e:
            await ctx.send(embed=self.embeds.error_embed(f'Failed to set prefix:\n{e}'))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Admin Cog ready. {self.bot.user} is online!')

def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))