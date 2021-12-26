import discord
from discord.ext import commands
from discord.ui import Button, View
from buttons import Delete_button
from constants import Replies, Emojis
import random


class Mybutton(Button):
    def __init__(self, ctx, label):
        self.ctx = ctx
        super().__init__(label=label, style=discord.ButtonStyle.green, emoji="👍")

    async def callback(self, interaction) -> None:

        if interaction.user.id == self.ctx.author.id:

            return await interaction.response.send_message(
                f"hello {self.ctx.author.name}"
            )

        return await interaction.response.send_message(
            f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)} \n this command was only for {self.ctx.author.mention} consider using your own"
        )


class buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test_button(self, ctx):
        button = Mybutton(ctx, "click me")
        view = View()
        view.add_item(button)
        await ctx.send("button", view=view)


def setup(bot):
    bot.add_cog(buttons(bot))
