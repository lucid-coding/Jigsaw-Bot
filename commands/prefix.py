from typing import Coroutine
from discord.components import Button
from discord.ext import commands
from discord.ui.view import View
from buttons import Delete_button
from constants import Replies, Emojis, Colors
import random
import discord


class PrefixClass(commands.Cog):
    """
    A Cog that handles most things about prefixes
    ---
    and where the prefix is delcared in main file
    bot.db2 is delcared in the pool , line 11
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error) -> None:
        await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)}"
                + f"{random.choice(Emojis.pepe_sad_emojis)}",
                description=error,
                color=Colors.red,
            )
        )

    @commands.command()
    async def prefix(self, ctx, prefix=None) -> Coroutine:
        view = View()
        button = Delete_button(ctx)
        view.add_item(button)
        if not prefix:
            return await ctx.send(
                embed=discord.Embed(
                    title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                    description="please provide a prefix **this command is used to change the bot prefix**",
                    color=Colors.red,
                ),
                view=view,
            )

        data = await self.bot.db2.fetch(
            "SELECT prefix from prefix_table where id = $1", ctx.guild.id
        )
        if not data:
            await self.bot.db2.execute(
                "INSERT INTO prefix_table VALUES($1,$2)", ctx.guild.id, prefix
            )
        else:
            await self.bot.db2.execute(
                "UPDATE prefix_table SET prefix = $1 where id = $2",
                prefix,
                ctx.guild.id,
            )
        await ctx.send(
            embed=discord.Embed(
                title="success",
                description=f"{prefix} has been stored",
                color=Colors.green,
            )
        )


def setup(bot):
    bot.add_cog(PrefixClass(bot))
