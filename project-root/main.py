import discord
from discord.ext import commands
from utils.config import Config
from utils.database import Database
from utils.errors import BotError
from utils.helper import get_prefix

# Initialize the bot and set intents
intents = discord.Intents.default()
intents.members = True  # Enable member intents for voice channel management
intents.message_content = True  # Enable message content intents to access message content

bot = commands.Bot(command_prefix=get_prefix, intents=intents)

# Load the configuration from the config file (or environment variables)
bot.config = Config(config_file='config.json')  # Replace 'config.json' with your config file name if you're using one

# Connect to the database
bot.database = Database(bot.config.get('database_path'))
bot.database.connect()

# Load cogs (modules)
bot.load_extension('cogs.music')
bot.load_extension('cogs.admin')

# Error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Invalid command. Use `{get_prefix(bot, ctx.message)}help` for a list of commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument. Use `{get_prefix(bot, ctx.message)}help <command>` for usage details.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f"You do not have the required permissions to use this command.")
    elif isinstance(error, BotError):
        await ctx.send(embed=bot.embeds.error_embed(str(error)))
    else:
        await ctx.send(embed=bot.embeds.error_embed(f"An unexpected error occurred: {error}"))

# On ready event
@bot.event
async def on_ready():
    print(f'Melody is online! {bot.user}')

# Run the bot
if __name__ == "__main__":
    bot.run(bot.config.get('token'))