import random
import discord
from discord.ext import commands
import aiohttp
from constants import Replies, Emojis


class catties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                description=error,
            )
        )

    @commands.command()
    async def cat(self, ctx):
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
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://kawaii.red/api/gif/kiss/token=801474997238366209.QY8T1qkju7Jx6X0dlKss/"
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
        member = member or ctx.author
        lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        pp = random.choice(lst) * "="
        embed = discord.Embed(
            title=" peepee size machine", description=f"{member.name}'s penis 8{pp}>"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, member: discord.Member) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://kawaii.red/api/gif/hug/token=801474997238366209.QY8T1qkju7Jx6X0dlKss/"
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
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://kawaii.red/api/gif/cuddle/token=801474997238366209.QY8T1qkju7Jx6X0dlKss/"
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
    async def slap(self, ctx, member: discord.Member) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://kawaii.red/api/gif/slap/token=801474997238366209.QY8T1qkju7Jx6X0dlKss/"
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
    async def pat(self, ctx, member: discord.Member) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://kawaii.red/api/gif/pat/token=801474997238366209.QY8T1qkju7Jx6X0dlKss/"
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
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://kawaii.red/api/gif/kill/token=801474997238366209.QY8T1qkju7Jx6X0dlKss/"
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
