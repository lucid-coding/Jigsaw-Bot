import asyncio
import random
from typing import Coroutine, Optional
import discord
from discord.ext import commands

from constants import Emojis, Replies


class AfkCommand(commands.Cog):
    def __init__(self, bot, dct=None, pings=None) -> None:
        self.bot = bot
        self.dct = dct or {}
        self.pings = pings or {}

    @commands.command()
    async def afk(self, ctx, *, message=None) -> Optional[Coroutine]:
        """
        An afk command.
        ---
        Arugments ->
        Optinal[message] : str

        """
        if ctx.author.id in self.dct:

            return await ctx.send(
                embed=discord.Embed(
                    title="",
                    description=f"You are already AFK with status : {self.dct[ctx.author.id]} ",
                )
            )

        await ctx.send(
            embed=discord.Embed(
                title="",
                description=f"You have been set to AFK with status : {message} ",
            )
        )

        await asyncio.sleep(1)

        self.dct[ctx.author.id] = message or "AFK"
        self.pings[ctx.author.id] = 0

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.id in self.dct.keys():
            self.dct.pop(message.author.id)
            if self.pings[message.author.id] == 0:
                return await message.channel.send(
                    embed=discord.Embed(
                        title=f"{random.choice(Replies.welcome_back_replies)}",
                        description=f"welcome back  {message.author.mention} {Emojis.ZeroTwoHug}",
                    )
                )

            elif self.pings[message.author.id] == 1:

                return await message.channel.send(
                    embed=discord.Embed(
                        title=f"{random.choice(Replies.welcome_back_replies)}",
                        description=f"you've been pinged {self.pings[message.author.id]} time",
                    )
                )

            return await message.channel.send(
                embed=discord.Embed(
                    title=f"{random.choice(Replies.welcome_back_replies)}",
                    description=f"welcome back {message.author.mention} you've been pinged {self.pings[message.author.id]} times ",
                )
            )
        else:
            for member in message.mentions:
                if member != message.author and member.id in self.dct:
                    user_message = (
                        self.dct[member.id] if self.dct[member.id] != "AFK" else None
                    )
                    if user_message is None:
                        await message.channel.send(
                            embed=discord.Embed(title="you've pinged someone whos afk")
                        )
                    else:
                        await message.channel.send(
                            embed=discord.Embed(
                                title="You've pinged someone whos afk",
                                description=f"With status : {user_message}",
                            )
                        )
                    self.pings[member.id] = self.pings[member.id] + 1


def setup(bot):
    bot.add_cog(AfkCommand(bot))
