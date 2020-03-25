#!/usr/bin/env python3
# Program: core.py
# Author: Darren Trieu Nguyen
# Version: 0.1
# Function: Contains the core functions of the Verity bot

from discord.ext import commands
import discord
from datetime import date
import datetime
import logging

class Core(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """ Initialization information to standard output
    """
    @commands.Cog.listener()
    async def on_ready(self, command_prefix='`'):
        # Preamble
        print('Logged in as {0.user}'.format(self.bot))
        print('Currently logged into ' + str(len(self.bot.guilds)) \
              + ' servers: ')
        for guild in self.bot.guilds:
            print('Server: ' + str(guild.name)\
                  + '; Total Members: ' + str(len(guild.members)))
        print('Current date is: ' + str(date.today().isoformat()))

        # Initiating Log
        logName = date.today().isoformat() + '.log'
        logging.basicConfig(filename=logName, level=logging.INFO)

        print('Initialization Complete')

def setup(bot):
    bot.add_cog(Core(bot))
