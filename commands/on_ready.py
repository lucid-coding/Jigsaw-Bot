from commands.prefix import PrefixManager
import re
import random
from typing import Coroutine
from discord.ext import commands
import discord
from discord.ui import View
from constants import Colors, Replies, Emojis
from buttons import Delete_button


class On_ready(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    """
    A cog with most listeners.
    ---
    No arugments are passed
    self.bot = bot 
    where bot is an object of discord.commands.bot
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
        if not isinstance(error, commands.CommandOnCooldown):
            raise error

    async def cog_command_error(self, ctx, error):
        return await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                description=error,
                color=Colors.red,
            )
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> Coroutine:
        if re.fullmatch(rf"<@!?{self.bot.user.id}>", message.content):
            await message.channel.send(
                f"my prefix is `{ await PrefixManager.prefix_getter(message)}` "
            )


def setup(bot):
    bot.add_cog(On_ready(bot))
