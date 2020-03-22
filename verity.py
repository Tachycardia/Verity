#!/usr/bin/env python3
# Program: verity.py
# Author: Darren Trieu Nguyen
# Verison: 0.7
# Function: Bot to verify users

import sys
import os.path
from os import path
import logging
import asyncio
import discord
import sys
import re
import time

from datetime import date
import datetime

# Verification Bot
class Verity(discord.Client):

    async def on_ready(self):
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
        if message.author == self.user:
            return

        if ('Verity' in message.content) or ('verity' in message.content):
            await message.channel.send('Hello!')

    """ Manages log date
        DEPRECATED
    """
    async def chatLog(self):
        while(True):
            logName = date.today().isoformat() + '.log'
            logging.basicConfig(filename=logName, level=logging.INFO)

            # Run log name updates
            await asyncio.sleep(3600)

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
    print('Checking for secret key in file: verityKey.secret')

    # Checks to see if verityKey.secret exists, if it doesn't creates it.
    if (path.exists('verityKey.secret')):
        print('Client secret file found, proceeding')
    else: 
        print('Client secret file not found, creating verityKey.secret')
        with open('verityKey.secret', 'w') as secretFile:
            secretFile.write('')
        secretFile.close()
        print('Put the client secret key in verityKey.secret')
        sys.exit()
        
    print('Attempting to read client secret key')
    with open('verityKey.secret', 'r') as secretFile:
        clientSecretKey = secretFile.read()
    secretFile.close()

    if len(clientSecretKey) < 1:
        print('Error: verityKey.secret is empty.')
        print('Put the client secret key in verityKey.secret')
        sys.exit()
        
    print('Initializing Verity:')
    ver = Verity()
    ver.loop.create_task(ver.verify())
    ver.run(clientSecretKey)
           
    return ver


if __name__ == '__main__':
    ver = initialize()
