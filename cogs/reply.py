#!/usr/bin/env python3
# Program: reply.py
# Author: Darren Trieu Nguyen
# Version: 1.0
# Function: Testing Cog: Bot will reply when its name is mentioned

import discord
from discord.ext import commands

class Reply(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Do not reply to itself
        if message.author == self.bot.user:
            return

        if ('Verity' in message.content) or ('verity' in message.content):
            await message.channel.send('Hello!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

def setup(bot):
    bot.add_cog(Reply(bot))
