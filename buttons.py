"""
A file where buttons are stored
"""

import discord
from constants import Colors, Replies, Emojis, BOTNAME
from discord.ext import commands
from discord.ui import Button, View
import random
from typing import Coroutine, Optional, Literal


class Delete_button(Button):
    """
    Some discord button that deletes the author and the bots message if everything goes smoothly
    Arguments

    ctx : discord.Context should be passed
    class discord.ButtonStyle
    or discord.ButtonStyle.danger, discord.ButtonStyle.gray
    ----
    """

    def __init__(
        self,
        ctx: commands.Context,
        style: Literal[discord.ButtonStyle.danger, discord.ButtonStyle.gray] = None,
    ) -> None:
        self.ctx = ctx
        self._style = style
        super().__init__(
            style=self._style or discord.ButtonStyle.danger,
            emoji=f"{random.choice(Emojis.trash_emojis)}",
        )

    async def callback(self, interaction) -> Coroutine:
        """
        A discord.ui.button callback function returns a coroutine
        deletes the bot message and the authors message
        -----
        when the if statment fails
        it sends to the user a random error_reply with a random "pepe" sad emoji
        ephemeral=True so only the user can sees it'
        """
        if interaction.user.id == self.ctx.author.id:
            # checking if the author id meets the user interaction id
            await self.ctx.message.delete()
            # deleting the author message
            return await interaction.message.delete()
            # and finally deleting the interaction message which is the bots message
        return await interaction.send_message(
            f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
            ephemeral=True,
        )


class HelpView(View):
    """
    A class for the help command view.
    """

    def __init__(
        self, ctx: commands.Context, *, timeout: Optional[float] = 180
    ) -> None:
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def on_error(self, error, _, interaction) -> Coroutine:
        print("i occured in ", __file__)
        return await interaction.send_message(
            f"{error}{random.choice(Emojis.pepe_sad_emojis)}", ephemeral=True
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.ctx.author.id != interaction.user.id:
            await interaction.response.send_message(
                f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                ephemeral=True,
            )
            await self.ctx.send(f"you are not {self.ctx.author}")
            return False
        return True

    @discord.ui.button(
        label="mod", style=discord.ButtonStyle.secondary, emoji=Emojis.mod_button
    )
    async def mod_callback(self, _, interaction) -> None:
        """
        A function that edits the help message and shows the modding commands
        ---
        Arguments -> interaction : discord.Interacion
        """
        prefix = self.ctx.message.content[0]
        embed = discord.Embed(title="Mod helping command", color=Colors.gray)
        embed.add_field(
            name="Banning",
            value=f'{prefix}Ban "{prefix}ban <@{BOTNAME}> reason"\n{prefix}pban `deletes the user messages and ban them` "{prefix}pban <@{BOTNAME}>"\n{prefix}unban "{prefix}unban <@{BOTNAME}>"',
            inline=False,
        )
        embed.add_field(
            name="kick", value=f'{prefix}kick "{prefix}kick <@{BOTNAME}>"', inline=False
        )
        embed.add_field(
            name="mute",
            value=f'{prefix}mute "{prefix}mute <@{BOTNAME}>"\n{prefix}unmute "{prefix}unmute <@{BOTNAME}>',
            inline=False,
        )
        embed.set_thumbnail(url=self.ctx.guild.icon.url)
        await interaction.message.edit(embed=embed)

    @discord.ui.button(
        label="fun", style=discord.ButtonStyle.secondary, emoji=Emojis.fun_button
    )
    async def fun_callback(self, _, interaction) -> None:
        """
        A function that edits the help message and shows "Fun commands"
        """
        prefix = self.ctx.message.content[0]
        embed = discord.Embed(title="Fun commands", color=Colors.gray)
        embed.add_field(
            name=f"{prefix}Gay",
            value=f"are you not sure if your gay or not ? use {prefix}gay",
        )
        embed.add_field(
            name=f"{prefix}pp", value=f"shows how much you be packin {Emojis.sus_emoji}"
        )
        embed.add_field(
            name="Api commands",
            value=f"{prefix}Kiss <@{BOTNAME}>\n{prefix}Hug <@{BOTNAME}>\n{prefix}Pat <@{BOTNAME}>\n{prefix}Cuddle <@{BOTNAME}>\n{prefix}Slap <@{BOTNAME}>\n{prefix}Kill <@{BOTNAME}>",
        )
        await interaction.message.edit(embed=embed)

    @discord.ui.button(
        label="info", style=discord.ButtonStyle.secondary, emoji=Emojis.info_button
    )
    async def info_callback(self, item, interaction) -> None:
        """
        A function that edits the help message and shows "info commands"
        ---
        Arguments -> interaction : discord.Interacion
        """
        prefix = self.ctx.message.content[0]
        embed = discord.Embed(title="Info commands", color=Colors.gray)
        embed.add_field(name=f"{prefix}Ping", value="shows the latency of the bot")
        embed.add_field(
            name=f"{prefix}Avatar", value=f"{prefix}Avatar 'displays an image of User'"
        )
        embed.add_field(
            name=f"{prefix}prefix",
            value=f"changes the server prefix and can be used like '{prefix}prefix ! '",
        )
        await interaction.message.edit(embed=embed)
