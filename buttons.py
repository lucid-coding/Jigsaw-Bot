"""
A file where buttons are stored
"""

import disnake
from constants import Colors, Replies, Emojis, BOTNAME
from disnake.ext import commands
from disnake.ui import Button, View
import random
from typing import Coroutine, Optional


class Delete_button(Button):
    """
    ctx : disnake.Context should be passed
    ----
    Some disnake button that deletes the author and the bots message if everything goes smoothly
    """

    def __init__(self, ctx: commands.Context) -> None:
        self.ctx = ctx
        super().__init__(
            style=disnake.ButtonStyle.danger,
            emoji=f"{random.choice(Emojis.trash_emojis)}",
        )

    async def callback(self, interaction) -> Coroutine:
        """
        A disnake.ui.button callback function returns a coroutine
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
        print("i occured in " , __file__)
        return await interaction.send_message(
            f"{error}{random.choice(Emojis.pepe_sad_emojis)}", ephemeral=True
        )

    async def interaction_check(self, interaction: disnake.Interaction) -> bool:
        if self.ctx.author.id != interaction.user.id:
            await interaction.response.send_message(
                f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                ephemeral=True,
            )
            await self.ctx.send(f"you are not {self.ctx.author}")
            return False
        return True

    @disnake.ui.button(
        label="mod", style=disnake.ButtonStyle.secondary, emoji=Emojis.mod_button
    )
    async def mod_callback(self, _, interaction) -> None:
        """
        A function that edits the help message and shows the modding commands
        ---
        Arguments -> interaction : disnake.Interacion 
        """
        prefix = self.ctx.message.content[0]
        embed = disnake.Embed(title="Mod helping command", color=Colors.gray)
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

    @disnake.ui.button(
        label="fun", style=disnake.ButtonStyle.secondary, emoji=Emojis.fun_button
    )
    async def fun_callback(self, _, interaction) -> None:
        """
        A function that edits the help message and shows "Fun commands"
        """
        prefix = self.ctx.message.content[0]
        embed = disnake.Embed(title="Fun commands", color=Colors.gray)
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

    @disnake.ui.button(
        label="info", style=disnake.ButtonStyle.secondary, emoji=Emojis.info_button
    )
    async def info_callback(self, _, interaction) -> None:
        """
        A function that edits the help message and shows "info commands"
        ---
        Arguments -> interaction : disnake.Interacion
        """
        prefix = self.ctx.message.content[0]
        embed = disnake.Embed(title="Info commands", color=Colors.gray)
        embed.add_field(name=f"{prefix}Ping", value="shows the latency of the bot")
        embed.add_field(
            name=f"{prefix}Avatar", value=f"{prefix}Avatar 'displays an image of User'"
        )
        embed.add_field(
            name=f"{prefix}prefix",
            value=f"changes the server prefix and can be used like '{prefix}prefix ! '",
        )
        await interaction.message.edit(embed=embed)
