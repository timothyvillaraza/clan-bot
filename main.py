import os
import discord
from replit import db
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

# bot Instance: All commands will start with '.'
bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents)


# On Ready Event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    cogListString = ''

    print('Loading cogs...')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = filename[:-3]  # File by name without .py extension
            await bot.load_extension(f'cogs.{cog_name}')
            cogListString += f'cogs.{cog_name}\n'
            print(f'    {cog_name} loaded')
    print()  # newline


@bot.command()
async def load(ctx, extension):
    cogListString = ''
    bot.load_extension(f'cogs.{extension}')
    cogListString += f'{extension}\n'

    embed_message = discord.Embed(title='Loaded Cogs',
                                  color=discord.Color.blue(),
                                  description=cogListString)

    await ctx.send(embed=embed_message)


@bot.command()
async def unload(ctx, extension):
    cogListString = ''
    bot.unload_extension(f'cogs.{extension}')
    cogListString += f'{extension}\n'

    embed_message = discord.Embed(title='Unloaded Cogs',
                                  color=discord.Color.blue(),
                                  description=cogListString)

    await ctx.send(embed=embed_message)


# Load All Cogs
@bot.command()
async def loadAllCogs(ctx):
    cogListString = ''

    print('Loading cogs...')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = filename[:-3]  # File by name without .py extension
            await bot.load_extension(f'cogs.{cog_name}')
            cogListString += f'cogs.{cog_name}\n'
            print(f'    {cog_name} loaded')
    print()  # newline

    embed_message = discord.Embed(title='Loaded Cogs',
                                  color=discord.Color.blue(),
                                  description=cogListString)

    await ctx.send(embed=embed_message)


@bot.command()
async def clear_db(ctx):
    """

    Clears all keys in the repl.it database

    """

    await ctx.send('Clearing all database keys.')

    for key in db:
        print(f'{key} deleted')
        del db[key]

    await ctx.send('All keys in the database deleted.')


# Run the bot
bot.run(os.environ['DISCORD_BOT_TOKEN'])
