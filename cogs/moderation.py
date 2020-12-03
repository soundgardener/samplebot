import datetime
import json
import cogs as cogs
import discord
from discord.ext import commands
import platform


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation Cog has been loaded")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embadfuckyou = discord.Embed(
            colour=discord.Colour.purple(),
            title=f"{member.name} has been banned.",
            description="fuck")
        await ctx.send(embed=embadfuckyou)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            banError = discord.Embed(
                colour=discord.Colour.purple()
            )
            banError.set_author(name="Please mention a person at the end of the command.",
                                 icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
            await ctx.send(embed=banError)

    # ban command



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} has been unbanned.')

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            unbanError = discord.Embed(
                colour=discord.Colour.purple()
            )
            unbanError.set_author(name="Please add the person's discord user at the end of the command. ($unban Example#1234)",
                                 icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
            await ctx.send(embed=unbanError)

    # unban command

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(user=member, reason=reason)


    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            kickError = discord.Embed(
                colour=discord.Colour.purple()
            )
            kickError.set_author(name='Please mention a person at the end of the command.',
                                 icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
            await ctx.send(embed=kickError)

    # kick command

    @commands.command(aliases=['quit', 'eject'])
    @commands.is_owner()
    async def logout(self, ctx):
        logError = discord.Embed(
            colour=discord.Colour.purple()
        )
        logError.set_author(name=f'Hey {ctx.author.mention}, I am now logging out :wave:',
                           icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
        logError.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=logError)

        await self.client.logout()

    @logout.error
    async def logout_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            exError = discord.Embed(
                colour=discord.Colour.red()
            )
            exError.set_author(name="Hey, you can't do that >:^(",
                               icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
            await ctx.send(embed=exError)

    # logout command

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def echo(self, ctx, *, message=None):
        message = message or "Please provide message to be echo'd"
        await ctx.message.delete()
        await ctx.send(message)

    # echo command

    @commands.command(aliases=['nuke', 'purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)

        nuke = discord.Embed(
            colour=discord.Colour.green()
        )
        nuke.set_author(name=f'{amount} messages deleted',
                        icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
        nuke.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=nuke)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            nukeError = discord.Embed(
                colour=discord.Colour.red()
            )
            nukeError.set_author(name='Please specify an amount of messages to delete.',
                                 icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
            await ctx.send(embed=nukeError)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        pass


        @commands.command()
        @commands.guild_only()
        @commands.has_permissions(administrator=True)
        @commands.bot_has_guild_permissions(manage_channels=True)
        async def lockdown(self, ctx, channel: discord.TextChannel=None):
            channel = channel or ctx.channel

            if ctx.guild.default_role not in channel.overwrites:
                overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
                }
                await channel.edit(overwrites=overwrites)
                await ctx.send(f"```I have put {channel.name} on lockdown.```")
            elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
                overwrites = channel.overwrites[ctx.guild.default_role]
                overwrites.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                await ctx.send(f"I have put `{channel.name}` on lockdown.")
            else:
                overwrites = channel.overwrites[ctx.guild.default_role]
                overwrites.send_messages = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                await ctx.send(f"I have removed `{channel.name}` from lockdown.")




def setup(client):
    client.add_cog(Moderation(client))
