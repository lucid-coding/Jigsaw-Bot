"""
A file for Snipe related commands.
"""
# pylint: disable=import-error
from typing import Coroutine, Optional
import random
from discord.ext import tasks
import discord
from discord.ext import commands
from constants import Emojis, Replies, Colors


class snipe(commands.Cog):
    """
    A cog for all commands related to snipe or its database
    ---
    Inherting from commands.Cog which allows this to be a cog class
    """

    def __init__(
        self,
        bot,
        message=None,
        author=None,
        blacklisted_stuff=None,
        edited_author=None,
        edited_message=None,
    ):
        self.bot = bot
        self.message = message
        self.author = author
        self.edited_author = edited_author
        self.edited_message = edited_message
        self.blacklisted_stuff = blacklisted_stuff
        self.my_loop.start()

    async def cog_command_error(self, ctx, error):
        await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)}"
                + f"{random.choice(Emojis.pepe_sad_emojis)}",
                description=error,
                color=Colors.red,
            )
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        content = [i for i in message.content if i.isalpha() or i == " "]
        content = "".join(content).split()
        try:
            blacklisted_text = self.blacklisted_stuff[message.guild.id]
        except KeyError:
            return None
        statment = set(blacklisted_text.split()) & set(content)
        if statment:
            return
        self.message = message.content
        self.author = message.author

    @commands.command(aliases=["s"])
    async def snipe(self, ctx):
        if self.message is None:
            return await ctx.send("there are no deleted messages")
        embed = discord.Embed()
        embed = discord.Embed(title="   ", description=f"{self.message}")
        embed.set_author(name=self.author.name, icon_url=self.author.avatar.url)
        embed.set_thumbnail(url=self.author.avatar.url)
        embed.set_footer(
            text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def blacklist(self, ctx, stuff=None):
        if stuff is None:
            return await ctx.send("please select some stuff")
        data = await self.bot.blacklist_db.fetch(
            "select * from blacklist where guild_id = $1", ctx.guild.id
        )
        if not data:
            text_data = await self.bot.blacklist_db.fetch(
                "select * from blacklist where guild_id = $1", ctx.guild.id
            )
            text_data_info = [i["text"] for i in text_data]

            text_data_info.append(stuff)
            string_of_data = " ".join(text_data)
            await self.bot.blacklist_db.execute(
                "INSERT INTO blacklist VALUES ($1,$2)", ctx.guild.id, string_of_data
            )
            return await ctx.send(
                embed=discord.Embed(
                    title="success",
                    description=f"added `{stuff}` to the database. ",
                    color=Colors.green,
                )
            )

        string_of_data = [i["text"] for i in data]
        for i in string_of_data:
            i = i.split()
            if stuff in i:

                return await ctx.send(
                    embed=discord.Embed(
                        title="Failed",
                        description=f"{stuff} is already stored in the database",
                        color=Colors.red,
                    )
                )
        string_of_data.append(stuff)
        await self.bot.blacklist_db.execute(
            "UPDATE blacklist SET text = $1 where guild_id = $2",
            " ".join(string_of_data),
            ctx.guild.id,
        )

        return await ctx.send(
            embed=discord.Embed(
                title="success",
                description=f"added `{stuff}` to the database. ",
                color=Colors.green,
            )
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def show_blacklist(self, ctx):
        x = await self.bot.blacklist_db.fetch(
            "SELECT * FROM blacklist where guild_id = $1", ctx.guild.id
        )
        return await ctx.send(
            embed=discord.Embed(
                title=f"blacklisted words for {ctx.guild.name}",
                description="".join(words["text"] for words in x),
            )
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def del_blacklist(self, ctx, *, word=None):

        x = await self.bot.blacklist_db.fetch(
            "select text from blacklist where guild_id = $1 ", ctx.guild.id
        )
        data = (i["text"] for i in x)
        data = list(data)

        print(data)
        data = data[0].split()
        print(data)
        if word not in data:
            return await ctx.send(
                embed=discord.Embed(
                    title="Fail",
                    description=f"couldnt find `{word}` in the database. ",
                    color=Colors.red,
                )
            )
        for index, element in enumerate(data):
            if element == word:
                data.pop(index)
                break
        hm = await self.bot.blacklist_db.execute(
            "UPDATE blacklist SET text = $1 where guild_id = $2",
            " ".join(data),
            ctx.guild.id,
        )
        if hm == "UPDATE 1":
            return await ctx.send(
                embed=discord.Embed(
                    title="success",
                    description=f"removed `{word}` from the database. ",
                    color=Colors.green,
                )
            )

    @tasks.loop(seconds=30)
    async def my_loop(self):
        data = await self.bot.blacklist_db.fetch(
            "SELECT guild_id , text FROM blacklist"
        )
        ids = [i["guild_id"] for i in data]
        words = [i["text"] for i in data]
        self.blacklisted_stuff = dict(zip(ids, words))

    @commands.Cog.listener()
    async def on_message(self, message) -> Optional[Coroutine]:
        if message.author.bot:
            return
        content = [i for i in message.content if i.isalpha() or i == " "]
        content = "".join(content).split()
        try:
            blacklisted_text = self.blacklisted_stuff[message.guild.id]
        except Exception as E:
            print(E)
            return None
        statment = set(blacklisted_text.split()) & set(content)
        if statment:
            await message.delete()
            text = ", ".join(statment)
            embed = discord.Embed(
                title=f"you've sent a blacklisted word in {message.guild.name}",
                description=f"Word : {text}",
            )
            embed.set_author(
                name=message.author.name, icon_url=message.author.avatar.url
            )
            embed.set_thumbnail(url=message.author.avatar.url)
            embed.set_footer(
                text=message.guild.member_count, icon_url=message.guild.icon.url
            )
            return await message.author.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, message) -> Optional[Coroutine]:
        if message.author.bot:
            return
        content = [i for i in message.content if i.isalpha() or i == " "]
        content = "".join(content).split()
        try:
            blacklisted_text = self.blacklisted_stuff[message.guild.id]
        except Exception as E:
            print(E)
            return None
        statment = set(blacklisted_text.split()) & set(content)
        if statment:
            await message.delete()
            text = ", ".join(statment)
            embed = discord.Embed(
                title=f"you've sent a blacklisted word in {message.guild.name}",
                description=f"Word : {text}",
            )
            embed.set_author(
                name=message.author.name, icon_url=message.author.avatar.url
            )
            embed.set_thumbnail(url=message.author.avatar.url)
            embed.set_footer(
                text=message.guild.member_count, icon_url=message.guild.icon.url
            )
            return await message.author.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        content = [i for i in message.content if i.isalpha() or i == " "]
        content = "".join(content).split()
        try:
            blacklisted_text = self.blacklisted_stuff[message.guild.id]
        except KeyError:
            return None
        statment = set(blacklisted_text.split()) & set(content)
        if statment:
            return
        self.edited_message = message.content
        self.edited_author = message.author

    @commands.command(aliases=["es"])
    async def editsnipe(self, ctx):
        if self.edited_message is None:
            return await ctx.send("there are no edited messages")
        embed = discord.Embed()
        embed = discord.Embed(title="   ", description=f"{self.edited_message}")
        embed.set_author(
            name=self.edited_author.name, icon_url=self.edited_author.avatar.url
        )
        embed.set_thumbnail(url=self.edited_author.avatar.url)
        embed.set_footer(
            text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(snipe(bot))
