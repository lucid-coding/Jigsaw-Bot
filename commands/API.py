import random
import discord
from discord.ext import commands
import aiohttp
from constants import Replies, Emojis, Colors
import json
with open("token.json") as f:
    API_TOKEN = json.load(f)["API_TOKEN"]

class catties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                description=error,
                color=Colors.red,
            )
        )

    @commands.command()
    async def cat(self, ctx):
        """
        A command that shows a picture of a cat
        ---
        Arguments -> None
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed()
                    embed.set_image(url=js[0]["url"])
                    embed.set_author(
                        name=f"requested by {ctx.author.name}",
                        icon_url=ctx.author.avatar.url,
                    )
                    embed.set_footer(text=f"{ctx.guild}", icon_url=ctx.guild.icon.url)
                    await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        """
        A command that shows a picture of a dog
        ---
        Arguments -> None
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed()
                    embed.set_image(url=js["message"])
                    embed.set_author(
                        name=f"requested by {ctx.author.name}",
                        icon_url=ctx.author.avatar.url,
                    )
                    embed.set_footer(text=f"{ctx.guild}", icon_url=ctx.guild.icon.url)
                    await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, member: discord.Member) -> str:
        """
        A command that sends a "kissing gif" to any user

        ---
        Arguments ->
        member : discord.Member

        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://kawaii.red/api/gif/kiss/token={API_TOKEN}"
            ) as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(
                        title="",
                        description=f"{ctx.author.mention} kissed {member.mention}",
                    )
                    embed.set_image(url=js["response"])
                    embed.set_author(
                        name=f"requested by {ctx.author.name}",
                        icon_url=ctx.author.avatar.url,
                    )
                    embed.set_footer(text=f"{ctx.guild}", icon_url=ctx.guild.icon.url)
                    await ctx.send(embed=embed)

    @commands.command()
    async def gay(self, ctx, member: discord.Member = None) -> None:
        """
        Shows how gay a user is.
        ---
        Arguements ->
        Member : Optional[discord.Member]
        """

        member = member or ctx.author
        lst = [
            0,
            5,
            10,
            15,
            20,
            25,
            30,
            35,
            40,
            45,
            50,
            55,
            60,
            65,
            70,
            75,
            80,
            85,
            90,
            95,
            100,
        ]
        embed = discord.Embed(
            title="Gay r8 machine",
            description=f"{member.mention} is {random.choice(lst)}% gay :rainbow_flag:",
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def pp(self, ctx, member: discord.Member = None) -> None:
        """
        Shows how much you packin ;) you can also try it on someone
        ---
        Arguments ->
        member : discord.Member

        """
        member = member or ctx.author
        lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        pp = random.choice(lst) * "="
        embed = discord.Embed(
            title=" peepee size machine", description=f"{member.name}'s penis 8{pp}>"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, member: discord.Member) -> None:
        """
        A command that sends a "hugging gif" to any user

        ---
        Arguments ->
        member : discord.Member
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://kawaii.red/api/gif/hug/token={API_TOKEN}"
            ) as r:
                if r.status == 200:
                    js = await r.json()
                    if ctx.author.id == member.id:
                        embed = discord.Embed(
                            description=f"{ctx.author.mention} hugged themselves "
                        )
                    else:
                        embed = discord.Embed(
                            description=f"{ctx.author.mention} hugged {member.mention}"
                        )
                    embed.set_author(
                        name=f"requested by {ctx.author.name}",
                        icon_url=ctx.author.avatar.url,
                    )
                    embed.set_footer(text=f"{ctx.guild}", icon_url=ctx.guild.icon.url)
                    embed.set_image(url=js["response"])
                    await ctx.send(embed=embed)

    @commands.command()
    async def cuddle(self, ctx, member: discord.Member) -> str:
        """
        A command that sends a "cuddling gif" to any user

        ---
        Arguments ->
        member : discord.Member
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://kawaii.red/api/gif/cuddle/token={API_TOKEN}"
            ) as r:
                if r.status == 200:
                    js = await r.json()
                    if ctx.author.id == member.id:
                        embed = discord.Embed(
                            description=f"{ctx.author.mention} cuddles with themselves "
                        )
                    else:
                        embed = discord.Embed(
                            description=f"{ctx.author.mention} cuddled with {member.mention}"
                        )
                    embed.set_author(
                        name=f"requested by {ctx.author.name}",
                        icon_url=ctx.author.avatar.url,
                    )
                    embed.set_footer(text=f"{ctx.guild}", icon_url=ctx.guild.icon.url)
                    embed.set_image(url=js["response"])
                    await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member) -> None:
        """
        A command that sends a "slap gif" to any user

        ---
        Arguments ->
        member : discord.Member
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://kawaii.red/api/gif/slap/token={API_TOKEN}"
            ) as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(
                        description=f"{ctx.author.mention} slapped {member.mention}"
                    )
                    embed.set_image(url=js["response"])
                    embed.set_author(
                        name=f"requested by {ctx.author.name}",
                        icon_url=ctx.author.avatar.url,
                    )
                    embed.set_footer(text=f"{ctx.guild}", icon_url=ctx.guild.icon.url)
                    await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, member: discord.Member) -> None:
        """
        A command to pat any user.
        ---
        Arguments -> discord.Member
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://kawaii.red/api/gif/pat/token={API_TOKEN}"
            ) as r:
                if r.status == 200:
                    js = await r.json()
                    if ctx.author.id == member.id:
                        embed = discord.Embed(
                            description=f"{ctx.author.mention} patted themselves "
                        )
                    else:
                        embed = discord.Embed(
                            description=f"{ctx.author.mention} pat pat {member.mention}"
                        )
                    embed.set_author(
                        name=f"requested by {ctx.author.name}",
                        icon_url=ctx.author.avatar.url,
                    )
                    embed.set_footer(text=f"{ctx.guild}", icon_url=ctx.guild.icon.url)
                    embed.set_image(url=js["response"])
                    await ctx.send(embed=embed)

    @commands.command()
    async def kill(self, ctx, member: discord.Member) -> str:
        """
        A command to kill any user. dont kill yourself tho
        ---
        Arguments -> discord.Member
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://kawaii.red/api/gif/kill/token={API_TOKEN}"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    if ctx.author.id == member.id:
                        embed = discord.Embed(
                            description=f"{ctx.author.mention} killed themselves "
                        )
                    else:
                        embed = discord.Embed(
                            description=f"{ctx.author.mention} killed {member.mention}"
                        )
                    embed.set_author(
                        name=f"requested by {ctx.author.name}",
                        icon_url=ctx.author.avatar.url,
                    )
                    embed.set_footer(text=f"{ctx.guild}", icon_url=ctx.guild.icon.url)
                    embed.set_image(url=result["response"])
                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(catties(bot))
