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
    "working on it"
    ...
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
        edited_author=None,
        edited_message=None,
    ):
        self.bot = bot
        self.message = message or {}
        self.author = author or {}
        self.edited_author = edited_author or {}
        self.edited_message = edited_message or {}

    async def cog_command_error(self, ctx, error):
        await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)}"
                + f"{random.choice(Emojis.pepe_sad_emojis)}",
                description=error,
                color=Colors.red,
            )
        )

    @commands.command(aliases=["s"])
    async def snipe(self, ctx):
        """
        Gets the recent deleted message and shows it.
        ---
        No arguments
        """
        try:
            if self.message[ctx.channel.id] is None:
                return await ctx.send("there are no deleted messages")
            message = self.message[ctx.channel.id]
            author = self.author[ctx.channel.id]
            embed = discord.Embed()
            embed = discord.Embed(title="   ", description=f"{message}")
            embed.set_author(name=author.name, icon_url=author.avatar.url)
            embed.set_thumbnail(url=author.avatar.url)
            embed.set_footer(
                text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
            )
            await ctx.send(embed=embed)
        except KeyError:
            return await ctx.send("there are no deleted messages")

    @commands.Cog.listener()
    async def on_message_edit(self, before, message) -> Optional[Coroutine]:
        """
        An event that checks if the user edited there message to a blacklisted one
        """
        if message.author.bot:
            return
        self.edited_message[message.channel.id] = message.content, before.content
        self.edited_author[message.channel.id] = message.author

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        self.message[message.channel.id] = message.content
        self.author[message.channel.id] = message.author

    @commands.command(aliases=["es"])
    async def editsnipe(self, ctx):
        try:
            embed = discord.Embed()
            embed = discord.Embed(
                title="   ",
                description=f"Before : {self.edited_message[ctx.channel.id][1]}\n\nAfter :{self.edited_message[ctx.channel.id][0]}",
            )
            embed.set_author(
                name=self.edited_author[ctx.channel.id].name,
                icon_url=self.edited_author[ctx.channel.id].avatar.url,
            )
            embed.set_thumbnail(url=self.edited_author[ctx.channel.id].avatar.url)
            embed.set_footer(
                text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
            )
            await ctx.send(embed=embed)
        except KeyError:
            return await ctx.send("there are no edited messages")


def setup(bot):
    bot.add_cog(snipe(bot))
