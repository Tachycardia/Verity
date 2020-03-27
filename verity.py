#!/usr/bin/env python3
# Program: verity.py
# Author: Darren Trieu Nguyen
# Version: 0.8
# Function: General discord bot

import sys
import os.path
from os import path
import logging
import asyncio
from datetime import date
import datetime
import re
import time

try:
    from discord.ext import commands
    import discord
except ImportError:
    print('Error: Discord.py is not installed.\n')
    sys.exit(1)

import cogs

# Verification Bot
# TODO: Move Verity class functions to "main cog"
class Verity(commands.Bot):

    def __init__(self, command_prefix='`'):
        pass

    async def on_message(self, message):
        logName = date.today().isoformat() + '.log'
        logging.basicConfig(filename=logName, level=logging.INFO)
        today = str(datetime.datetime.now())
        if message.guild is not None:
            logging.info('[' + str(today) + \
                         ']: Guild: {0.guild.name}: ' + \
                         'Channel: {0.channel.name}: ' + 
                         'Message from {0.author}: {0.content}'.format(message))
        else:
            logging.info('[' + str(today) + \
                         ']: Direct Message: ' + \
                         'Channel: {0.channel.name}: ' + 
                         'Message from {0.author}: {0.content}'.format(message))


    """
    async def retrieveAudit(self, guild, limit=-1):
        if (limit < 0):
            for entry in guild.audit_logs()
    """

# Initialization function
def initialize():

    # Checks the config file: verity.config
    configFilePath = 'verity.config'

    if (path.exists(configFilePath)):
        print('Reading config file')
    else:
        print('Config file not found, generating default config file')
        with open('verity.config') as configFile:
            configFile.write('ClientTokenFile=verityKey.secret')
            configFile.write('CogsPath=Cogs/')
        configFile.close()
        print('Default config file generated')

    # Parsing the config file for configuration values
    with open(configFilePath) as configFile:
        # ClientTokenFile
        secretFilePath = configFile.readline().split('=', maxsplit=1)[1].rstrip()
        # CogsPath
        cogsPath = configFile.readline().split('=', maxsplit=1)[1].rstrip()

    print('Checking for secret key in file: ' + str(secretFilePath))

    # Checks to see if verityKey.secret exists, if it doesn't creates it.
    if (path.exists(secretFilePath)):
        print('Client secret file found, proceeding')
    else: 
        print('Client secret file not found, creating ' + str(secretFilePath))
        with open(secretFilePath, 'w') as secretFile:
            secretFile.write('')
        secretFile.close()
        print('Put the client secret key in ' + str(secretFilePath))
        sys.exit()
        
    # Reading the client secret key
    print('Attempting to read client secret key from ' + str(secretFilePath))

    with open(secretFilePath, 'r') as secretFile:
        clientSecretKey = secretFile.read()
    secretFile.close()

    if len(clientSecretKey.split(' \n\t')) < 1:
        print('Error: ' + str(secretFilePath) + ' is empty.')
        print('Put the client secret key in ' + str(secretFilePath))
        sys.exit()
        
    # Initializing Verity Bot
    print('Initializing Verity:')
    #ver = Verity()
    ver = commands.Bot('`')
    ver.add_cog(cogs.Reply(ver))
    ver.add_cog(cogs.Core(ver))
    ver.add_cog(cogs.Admin(ver))
    #ver.add_cog(Verify(ver))
    #ver.loop.create_task(ver.verify())
    ver.run(clientSecretKey)
           
    return ver


if __name__ == '__main__':
    ver = initialize()
