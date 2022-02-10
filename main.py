import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('discord_secret')
prefix = '.'

class CustomHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        return await super().send_bot_help(mapping)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help(group)

    async def send_command_help(self, command):
        print(command)
        return await super().send_command_help(command)


client = commands.Bot(command_prefix = prefix) 

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

# Error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required arguments.')

# Searchs for all the cogs and loads them
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        # Remove the .py extension
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
