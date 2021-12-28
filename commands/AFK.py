import asyncio
import random
import discord
from discord.ext import commands

from constants import Emojis, Replies


class AfkCommand(commands.Cog):
    def __init__(self, bot, dct=None, pings=None) -> None:
        self.bot = bot
        self.dct = dct or {}
        self.pings = pings or {}

    @commands.command()
    async def afk(self, ctx, *, message=None):
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
                    f"welcome back {message.author.mention} you've been pinged {self.pings[message.author.id]} time"
                )

            return await message.channel.send(
                f"welcome back {message.author.mention} you've been pinged {self.pings[message.author.id]} times"
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
                                title="you've pinged someone whos afk",
                                description=user_message,
                            )
                        )
                    self.pings[member.id] = self.pings[member.id] + 1

    # @commands.command(aliases=['store_messages'])
    # async def store(self,ctx,*,message=None):
    #     if message is None : return await ctx.send('we need a message sir')
    #     await self.bot.db.execute("INSERT INTO messages VALUES ($1 ,$2) ",ctx.author.id,message)
    #     await ctx.send(f'Done inserting {message} into the database')
    # @commands.command(aliases=['show_messages'])
    # async def show(self,ctx):
    #     x = await self.bot.db.fetch("SELECT message FROM messages WHERE ID = $1",ctx.author.id)
    #     if len(x) == 0:
    #         return await ctx.send(embed=discord.Embed(title=f'{ctx.author.name} messages',description='No messages are available for this user'))

    #     return await ctx.send(embed=discord.Embed(title=f'{ctx.author.name} messages',description='\n'.join(record["message"] for record in x)))
    # @commands.command(aliases=['delete_messages'])
    # async def delete(self,ctx,*,message):
    #     x = await self.bot.db.fetch("DELETE FROM messages where id = $1 and message = $2",ctx.author.id,message)
    # @commands.command(aliases=['delete_all_messages'])
    # async def delete_all(self,ctx):
    #     x = await self.bot.db.fetch("DELETE FROM messages where id = $1",ctx.author.id)
    #     return await ctx.send(":thumbsup:")


def setup(bot):
    bot.add_cog(AfkCommand(bot))
