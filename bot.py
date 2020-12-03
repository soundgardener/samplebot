import datetime
import platform
import discord
import os
import json
from discord.ext import commands
from discord.utils import get


def get_prefix(client,message):
    if not message.guild:
        return commands.when_mentioned_or("$")(client, message)

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("$")(client, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(client, message)

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=421444514343944203)



@client.event
async def on_ready():
    print(f'Logged in as: {client.user.name} : {client.user.id}')
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='testin'))


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("hello!")
        break


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# cog commands

@client.command()
async def ping(ctx):
    pingEmbed = discord.Embed(
        colour=discord.Colour.purple()
    )
    pingEmbed.set_author(name=f'Pong! 🏓 {round(client.latency * 1000)}ms',
                         icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
    await ctx.send(embed=pingEmbed)


@client.command()
async def stats(ctx):
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(client.guilds)
    memberCount = len(set(client.get_all_members()))
    await ctx.send(
        f"Bot Stats:\nThis bot is in **{serverCount}** servers with a total of **{memberCount}** members.\nI'm running Python **{pythonVersion}** and Discord.py **{dpyVersion}**.")

@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member : discord.Member):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)
            await ctx.send(f"{member.mention} has been muted.")
            return

            overwrite = discord.PermissionsOverwrite(send_messages = False)
            newRole = await guild.create_role(name="Muted")

            for channel in guild.text_channels:
                await channel.set_permissions(newRole, overwrite=overwrite)
            await member.add_roles(newRole)
            await ctx.send(f"{member.mention} has been muted.")

@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member : discord.Member):
    guild = ctx.guild

    for role in guild.roles:
        if role.name=="Muted":
            await  member.remove_roles(role)
            await ctx.send(f"{member.mention} has been unmuted.")
            return



client.run('token goes here')
