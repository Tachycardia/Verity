#!/usr/bin/env python3
# Program: verify.py
# Author: Darren Trieu Nguyen
# Version: 1.0
# Function: Checks to see if a user has had the "Unverified" role for more
#           than a given period of time. If so, then kicks them from the server

from discord.ext import commands
import discord
from datetime import date
import datetime
import logging

class Verify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """ Verification Function:
        Parses through all members with the role 'Unverified'
        If the unverified member has been a member of the server for more
        than threshold days, kick the member
        Default Threshold = 30 days
    """
    async def verify(self, threshold=14):
        while(True):
            """
            logName = date.today().isoformat() + '.log'
            logging.basicConfig(filename=logName, level=logging.INFO)
            """

            today = str(datetime.datetime.now())
            unverifiedDict = {}
            # Checking each server 
            for guild in self.bot.guilds:
                # Distinguishing members with a role of the name 'Unverified'
                unverifiedMembers = [member for member in guild.members \
                                     if 'Unverified' \
                                     in [role.name for role in member.roles]]
                """
                logging.info('Current unverified members in ' \
                             + str(guild.name) + ': ')
                """
                for member in unverifiedMembers:
                    unverifiedDict[member] = re.split('-| |\.', \
                                                      str(member.joined_at))
                # Checking each unverified member
                for member in unverifiedDict.keys():
                    joinDate = date(int(unverifiedDict[member][0]), \
                                    int(unverifiedDict[member][1]), \
                                    int(unverifiedDict[member][2]))
                    unverifiedTime = date.today() - joinDate
                    """
                    logging.info('[' + str(today) + ']:' \
                                 + str(member.name) + ' has spent '\
                                 + str(unverifiedTime.days) \
                                 + ' days unverified')
                    """
                    if (unverifiedTime.days >= threshold):
                        await guild.kick(member)
                        """
                        logging.info('[' + str(today) + ']:' \
                                     'Kicking ' + str(member.name) + ' from ' \
                                     + str(guild.name) \
                                     + ' for being unverified for ' \
                                     + str(unverifiedTime.days) + ' days')
                        """
            # Run verifications checks every hour
            await asyncio.sleep(3600)

