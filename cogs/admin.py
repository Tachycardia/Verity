#!/usr/bin/env python3
# Program: Admin
# Author: Darren Trieu Nguyen
# Version: 0.1
# Function: Contains functions for the facilitation of moderation

import discord
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # TODO: Add optional HTML Parser to prettify the voice status output
    """ Outputs information for a given member
    """
    @commands.command()
    async def analyze(self, ctx, memberIdentifier):
        # Extracting member object from identifier 
        member = await commands.MemberConverter().convert(ctx, memberIdentifier)

        # Outputting member data
        await ctx.send('--- Beginning Analysis ---')
        await ctx.send('Member Name: ' + str(member.name))
        await ctx.send('Member Server Nick: ' + str(member.nick))
        await ctx.send('Member ID: ' + str(member.id))
        await ctx.send('Member Avatar: ' + str(member.avatar_url))
        await ctx.send('Joined ' + str(member.guild) + ' at ' + str(member.joined_at))
        await ctx.send('Current status: ' + str(member.status))
        await ctx.send('Current activity: ' + str(member.activity))
        await ctx.send('Voice Status: ' + str(member.voice))
        await ctx.send('Roles:')
        for role in member.roles:
            if not (str(role) == '@everyone'):
                await ctx.send('  ' + str(role))
        await ctx.send('--- Analysis Complete ---')

        
    # TODO: Add user perm check
    """ Kicks a member from the discord server
    """
    @commands.command()
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, memberIdentifier, reason=None):

        member = await commands.MemberConverter().convert(ctx, memberIdentifier)

        await ctx.send('Kicking ' + str(member) + ' for: ' + str(reason))

        # Kicking member
        try: 
            await member.kick()
        except Forbidden:
            await ctx.send('Error: Not enough permissions to' \
                           + ' perform this action')
        except HTTPException:
            await ctx.send('Error: Kicking failed')

def setup(bot):
    bot.add_cog(Admin(bot))
