#!/usr/bin/env python3
# Program: Admin
# Author: Darren Trieu Nguyen
# Version: 0.1
# Function: Contains functions for the facilitation of moderation

import discord
from discord.ext import commands

# TODO: Make this a functional decorator that handles errors and outputs to 
#       ctx.send
def eCtx(func):
    def exceptionHandler():
        print('ExceptionCtx Run')
        func()
        print('ExceptionCtx Done Running')
    return exceptionHandler

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # TODO: Add optional HTML Parser to prettify the voice status output
    # TODO: Catch exceptions and output to ctx.send
    """ Outputs information for a given member
    """
    @commands.command()
    @commands.is_owner()
    async def analyze(self, ctx, memberIdentifier):
        # Extracting member object from identifier 
        try:
            member = await \
                     commands.MemberConverter().convert(ctx, memberIdentifier)

            # Outputting member data
            await ctx.send('--- Beginning Analysis ---')
            await ctx.send('Member Name: ' + str(member.name))
            await ctx.send('Member Server Nick: ' + str(member.nick))
            await ctx.send('Member ID: ' + str(member.id))
            await ctx.send('Member Avatar: ' + str(member.avatar_url))
            await ctx.send('Joined ' + str(member.guild) + ' at ' \
                           + str(member.joined_at))
            await ctx.send('Current status: ' + str(member.status))
            await ctx.send('Current activity: ' + str(member.activity))
            await ctx.send('Voice Status: ' + str(member.voice))
            await ctx.send('Roles:')
            for role in member.roles:
                if not (str(role) == '@everyone'):
                    await ctx.send('  ' + str(role))
            await ctx.send('--- Analysis Complete ---')
        except commands.errors.NotOwner:
            await ctx.send('You do not own me.')
        except:
            await ctx.send('Error: Member "' + str(memberIdentifier) \
                           + '" could not be found')

        
    """ Kicks a member from the discord server
    """
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, memberIdentifier, reason=None):

        member = await commands.MemberConverter().convert(ctx, memberIdentifier)

        if (self.bot.is_owner(member) == False):
            await ctx.send('Kicking ' + str(member) + ' for: ' + str(reason))

            # Kicking member
            try: 
                await member.kick()
            except:
                await ctx.send('Error: Failed to kick "' \
                               + str(memberIdentifier) \
                               + '".')
        


def setup(bot):
    bot.add_cog(Admin(bot))
