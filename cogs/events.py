import discord
from discord.ext import commands
import random
import datetime
import json


# In cogs we make our own class
# for d.py which subclasses commands.Cog

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Cog has been loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='general')
        if channel:
            joinEmbed = discord.Embed(
                description='Welcome to the server!',
                colour=discord.Colour.purple()
            )
            joinEmbed.set_thumbnail(url=member.avatar_url)
            joinEmbed.set_author(name=member.name, icon_url=member.avatar_url)
            joinEmbed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            joinEmbed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=joinEmbed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='general')
        if channel:
            leftEmbed = discord.Embed(
                description="Good Riddance.",
                color=discord.Colour.red(),
            )
            leftEmbed.set_thumbnail(url=member.avatar_url)
            leftEmbed.set_author(name=member.name, icon_url=member.avatar_url)
            leftEmbed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            leftEmbed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=leftEmbed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            await ctx.send("Hey! You lack permission to use this command.")
        raise error


    

def setup(client):
    client.add_cog(Events(client))
