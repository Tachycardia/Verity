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

from cogs.reply import Reply
from cogs.greetings import Greetings


# Verification Bot
# TODO: Move Verity class functions to "main cog"
class Verity(commands.Bot):

    def __init__(self, command_prefix='`'):
        pass

    async def on_ready(self, command_prefix='`'):
        # Preamble
        print('Logged in as {0.user}'.format(self))
        print('Currently logged into ' + str(len(self.guilds)) \
              + ' servers: ')
        for guild in self.guilds:
            print('Server: ' + str(guild.name)\
                  + '; Total Members: ' + str(len(guild.members)))
        print('Current date is: ' + str(date.today().isoformat()))

        # Initiating Log
        logName = date.today().isoformat() + '.log'
        logging.basicConfig(filename=logName, level=logging.INFO)

        print('Initialization Complete')

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
        # Do not reply to itself
        """
        if message.author == self.user:
            return

        if ('Verity' in message.content) or ('verity' in message.content):
            await message.channel.send('Hello!')
        """

    """ Verification Function:
        Parses through all members with the role 'Unverified'
        If the unverified member has been a member of the server for more
        than threshold days, kick the member
        Default Threshold = 30 days
    """
    async def verify(self, threshold=14):
        while(True):
            logName = date.today().isoformat() + '.log'
            logging.basicConfig(filename=logName, level=logging.INFO)

            today = str(datetime.datetime.now())
            unverifiedDict = {}
            # Checking each server 
            for guild in self.guilds:
                # Distinguishing members with a role of the name 'Unverified'
                unverifiedMembers = [member for member in guild.members \
                                     if 'Unverified' \
                                     in [role.name for role in member.roles]]
                logging.info('Current unverified members in ' \
                             + str(guild.name) + ': ')
                for member in unverifiedMembers:
                    unverifiedDict[member] = re.split('-| |\.', \
                                                      str(member.joined_at))
                # Checking each unverified member
                for member in unverifiedDict.keys():
                    joinDate = date(int(unverifiedDict[member][0]), \
                                    int(unverifiedDict[member][1]), \
                                    int(unverifiedDict[member][2]))
                    unverifiedTime = date.today() - joinDate
                    logging.info('[' + str(today) + ']:' \
                                 + str(member.name) + ' has spent '\
                                 + str(unverifiedTime.days) \
                                 + ' days unverified')
                    if (unverifiedTime.days >= threshold):
                        await guild.kick(member)
                        logging.info('[' + str(today) + ']:' \
                                     'Kicking ' + str(member.name) + ' from ' \
                                     + str(guild.name) \
                                     + ' for being unverified for ' \
                                     + str(unverifiedTime.days) + ' days')
            # Run verifications checks every hour
            await asyncio.sleep(3600)

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
    #ver.add_cog(Greetings(ver))
    ver.add_cog(Reply(ver))
    #ver.loop.create_task(ver.verify())
    ver.run(clientSecretKey)
           
    return ver


if __name__ == '__main__':
    ver = initialize()
