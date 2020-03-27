#!/usr/bin/env python3
# Program: testCog.py
# Author: Darren Trieu Nguyen
# Version: 1.0
# Function: Testing Cog: Test cog for commands

import discord
from discord.ext import commands

class TestCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def command1(self, ctx):
        print('Command 1 Run')
        await ctx.send('Command 1 Successfully Run')


def setup(bot):
    bot.add_cog(TestCog(bot))
