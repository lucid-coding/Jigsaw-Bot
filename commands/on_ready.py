import re
import random
from typing import Coroutine
from discord.ext import commands
import discord
from discord.message import Message
from discord.ui import View
from constants import Colors, Replies, Emojis
from buttons import Delete_button


class On_ready(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    """
    A cog with most listeners.
    """
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                description=f"`{ctx.message.content}` command was not found",
                color=Colors.red,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_footer(text=ctx.guild.member_count, icon_url=ctx.guild.icon.url)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            view = View()
            button = Delete_button(ctx)
            view.add_item(button)
            return await ctx.send(embed=embed, view=view)
        raise error

    @commands.Cog.listener()
    async def on_ready(self):
        print("logged in")

    async def cog_command_error(self, ctx, error):
        return await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                description=error,
                color=Colors.red,
            )
        )

    @commands.Cog.listener()
    async def on_member_join(self, member) -> Message:
        channel = self.bot.get_channel(913653805122453551)
        embed = discord.Embed(
            title="   ",
            description="[self](https://discord.com/channels/913653805122453545/913856880265285702/913894248653406348) <:peperules:914189058719219754> [blessed](https://discord.com/channels/913653805122453545/914165430560636999/914168257202761748)",
            color=0x36393F,
        )
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=member.guild.member_count, icon_url=member.guild.icon.url)
        await channel.send(f"{member.mention}", embed=embed)

    # @commands.command()
    # async def welcome_test(self, ctx):
    #     channel = self.bot.get_channel(913653805122453551)
    #     embed = discord.Embed(
    #         title="   ",
    #         description="[self](https://discord.com/channels/913653805122453545/913856880265285702/913894248653406348) <:peperules:914189058719219754> [blessed](https://discord.com/channels/913653805122453545/914165430560636999/914168257202761748)",
    #         color=0x36393F,
    #     )
    #     embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    #     embed.set_thumbnail(url=ctx.author.avatar.url)
    #     embed.set_footer(text=ctx.guild.member_count, icon_url=ctx.guild.icon.url)
    #     await channel.send(f"{ctx.author.mention}", embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> Coroutine:
        if re.fullmatch(rf"<@!?{self.bot.user.id}>", message.content):
            x = await self.bot.db2.fetch(
                "SELECT prefix from prefix_table where id = $1", message.guild.id
            )
            x = (i["prefix"] for i in x)
            if x:

                return await message.channel.send(f"My prefix is `{x.__next__()}`!")
            return await message.channel.send("My prefix is $")


def setup(bot):
    bot.add_cog(On_ready(bot))
