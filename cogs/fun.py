import random
from random import choice, randint
from typing import Optional
from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown
import discord
from discord.ext import commands
import datetime



class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun Cog has been loaded")

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",

                     "It is decidedly so.",

                     "Without a doubt.",

                     "Yes - definitely.",

                     "You may rely on it.",

                     "As I see it, yes.",

                     "Most likely.",

                     "Outlook good.",

                     "Yes.",

                     "Signs point to yes.",

                     "Reply hazy, try again.",

                     "Ask again later.",

                     "Better not tell you now.",

                     "Cannot predict now.",

                     "Concentrate and ask again.",

                     "Don't count on it.",

                     "My reply is no.",

                     "My sources say no.",

                     "Outlook not so good.",

                     "Very doubtful."]
        _8ballEmbed = discord.Embed(
            colour=discord.Colour.purple()
        )
        _8ballEmbed.set_author(name=f'Question: {question}\nAnswer: {random.choice(responses)}')
        _8ballEmbed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=_8ballEmbed)

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument ):
            _8ballError = discord.Embed(
                colour=discord.Colour.purple()
            )
            _8ballError.set_author(name='Please type a question after the command.',
                               icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
            await ctx.send(embed= _8ballError)

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")

    @slap_member.error
    async def slap_member_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            slapError = discord.Embed(
                colour=discord.Colour.red()
            )
            slapError.set_author(name='Please mention a member at the end of the command.',
                               icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
            await ctx.send(embed=slapError)

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!")

    @command(name="fact")
    async def animal_fact(self, ctx, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(title=f"{animal.title()} fact",
                                  description=data["fact"],
                                  colour=ctx.author.colour)
                    if image_link is not None:
                        embed.set_author(name="Powered by some-random-api.ml",
                                         icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            await ctx.send("No facts are available for that animal.")
    @animal_fact.error
    async def animaL_fact_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            factError = discord.Embed(
                colour=discord.Colour.purple()
            )
            factError.set_author(name='Please type one ouf of these at the end of the command: dog, cat, panda, fox, bird, koala',
                               icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
            factError.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=factError)


    @commands.command(aliases=["pet"])
    async def headpat(self, ctx, member: Member):
        headpats = ["https://tenor.com/view/good-boy-pat-on-head-stitch-gif-14742401",
                    "https://tenor.com/view/anime-head-pat-anime-head-rub-neko-anime-love-anime-gif-16121044",
                    "https://tenor.com/view/rikka-head-pat-pat-on-head-anime-rikka-gif-13911345",
                    "https://tenor.com/view/anime-pet-gif-9200932",
                    "https://tenor.com/view/kanna-kamui-pat-head-pat-gif-12018819",
                    "https://tenor.com/view/pat-head-loli-dragon-anime-gif-9920853",
                    "https://tenor.com/view/nagi_no_asukara-nagi-manaka-head-pat-gif-8841561",
                    "https://tenor.com/view/head-pat-anime-kawaii-neko-nyaruko-gif-15735895",
                    "https://tenor.com/view/pat-head-good-job-anime-gif-15471762",
                    "https://tenor.com/view/head-pat-its-okay-anime-gif-17863262",
                    "https://tenor.com/view/anime-friends-hug-imiss-this-head-pat-gif-17841335"]


        await ctx.send(f"{ctx.author.mention} petted {member.mention}!\n {random.choice(headpats)}")

    @headpat.error
    async def headpat_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            patError = discord.Embed(
                colour=discord.Colour.purple()
            )
            patError.set_author(name='Please mention a member at the end of the command.',
                               icon_url="https://cdn.discordapp.com/attachments/784147795132547143/784150310096076880/cat_pog.gif")
            await ctx.send(embed=patError)


def setup(client):
    client.add_cog(Fun(client))
