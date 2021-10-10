#!/bin/env python
import os

import discord
from discord.ext import commands

# setup of logging and env-vars
# logging must be initialized before environment, to enable logging in environment
from .log_setup import logger
from .environment import PREFIX, TOKEN

"""
This bot is based on a template by nonchris
https://github.com/nonchris/discord-bot
"""

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


# login message
@bot.event
async def on_ready():
    """!
    function called when the bot is ready. emits the '[Bot] has connected' message
    """
    print(f'{bot.user.name} has connected')

    logger.info(f"Bot has connected, active on {len(bot.guilds)} guilds")

    print(f'Bot is connected to the following guilds:')
    print()
    member_count = 0
    for g in bot.guilds:
        print(f"{g.name} - {g.id} - Members: {g.member_count}")
        member_count += g.member_count
    print()
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"{PREFIX}help"))

    # LOADING Extensions
    bot.remove_command('help')  # unload default help message
    initial_extensions = [
        '.cogs.misc',
        '.cogs.help',
        '.cogs.quiz'
    ]

    for extension in initial_extensions:
        bot.load_extension(extension, package=__package__)


def start_bot(token=None):
    """ Start the bot, takes token, uses token from env if none is given """

    if token:
        bot.run(token)
    if TOKEN:
        bot.run(TOKEN)
    else:
        logger.error("No token was given! - Exiting")
