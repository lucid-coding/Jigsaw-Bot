"""
A file where buttons are stored
"""
from main import LucidBot

from ctypes import Union
import discord
from discord.enums import ButtonStyle
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
            try:
                await self.ctx.message.delete()
                # trying to delete the message, this would work if the message isnt a slash-command
            except discord.errors.NotFound:
                # this is basically checking if the message was used by a slash-command so it's not needed to delete it , otherwise it would create a error.
                pass
            return await interaction.message.delete()
            # and finally deleting the interaction message which is the bots message
        return await interaction.response.send_message(
            f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
            ephemeral=True,
        )


class HelpView(View):
    """
    A class for the help command view.
    ---
    Inheriting from discord.ui.View
    """

    def __init__(
        self, ctx: commands.Context, *, timeout: Optional[float] = 180
    ) -> None:

        super().__init__(timeout=timeout)

        self.ctx = ctx
        self.prefix = self.ctx.message.content[0]
        self.add_item(
            Button(
                label="Invite me !",
                url=self.ctx.bot.INVITE_URL,
            )
        )

    async def on_error(self, error, _, interaction) -> Coroutine:
        """
        A discord.ui.view on_error function returns a coroutine
        ---
        Arguments :
        error : discord.errors.Forbidden
        _ : discord.ext.commands.Command
        interaction : discord.ui.Interaction
        """
        return await interaction.response.send_message(
            f" {error} {random.choice(Emojis.pepe_sad_emojis)}", ephemeral=True
        )

    async def interaction_check(self, _, interaction: discord.Interaction) -> bool:
        """
        A discord.ui.view interaction_check function returns a boolean
        ---
        Arguments :
        _ : discord.ext.commands.Command
        interaction : discord.ui.Interaction
        """
        if self.ctx.author.id != interaction.user.id:
            await interaction.response.send_message(
                f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                ephemeral=True,
            )
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

        embed = discord.Embed(title="Mod helping command", color=Colors.gray)
        embed.add_field(
            name="Banning",
            value=f'{self.prefix}Ban "{self.prefix}ban <@{BOTNAME}> reason"\n{self.prefix}pban `deletes the user messages and ban them` "{self.prefix}pban <@{BOTNAME}>"\n{self.prefix}unban "{self.prefix}unban <@{BOTNAME}>"',
            inline=False,
        )
        embed.add_field(
            name="kick", value=f'{self.prefix}kick "{self.prefix}kick <@{BOTNAME}>"', inline=False
        )
        embed.add_field(
            name="mute",
            value=f'{self.prefix}mute "{self.prefix}mute <@{BOTNAME}>"\n{self.prefix}unmute "{self.prefix}unmute <@{BOTNAME}>',
            inline=False,
        )
        embed.add_field(
            name="timeout",
            value=f'{self.prefix}timeout "{self.prefix}timeout <@{BOTNAME}> time"\n{self.prefix}untimeout "{self.prefix}untimeout <@{BOTNAME}>',
            inline=False,
        )

        embed.set_thumbnail(url=self.ctx.guild.icon.url)
        await interaction.message.edit(embed=embed)

    @discord.ui.button(
        label='welcome', style=discord.ButtonStyle.secondary, emoji=Emojis.welcome_button
    )
    async def welcome_callback(self, _, interaction) -> None:
        """
        A function that edits the help message and shows the welcome commands
        ---
        Arguments -> interaction : discord.Interacion
        """
        embed = discord.Embed(title="Welcome helping command", color=Colors.gray)
        embed.add_field(
            name="set_welcome",
            value=f'{self.prefix}set_welcome "{self.prefix}set_welcome welcome_channel_id welcome_message"\n"Arguments are a string and a integer"',
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
        embed = discord.Embed(title="Fun commands", color=Colors.gray)
        embed.add_field(
            name=f"{self.prefix}Gay",
            value=f"are you not sure if your gay or not ? use {self.prefix}gay",
            inline=False
        )
        embed.add_field(
            name=f"{self.prefix}pp",
            value=f"shows how much you be packin {Emojis.sus_emoji}",
            inline=False
        )
        embed.add_field(
            name="Api commands",
            value=f"{self.prefix}Kiss <@{BOTNAME}>\n{self.prefix}Hug <@{BOTNAME}>\n{self.prefix}Pat <@{BOTNAME}>\n{self.prefix}Cuddle <@{BOTNAME}>\n{self.prefix}Slap <@{BOTNAME}>\n{self.prefix}Kill <@{BOTNAME}>",
            inline=False
        )
        
        embed.add_field(
            name="animal commands",
            value=f'{self.prefix}Dog\n{self.prefix}Cat',
            inline=False
        )
        await interaction.message.edit(embed=embed)

    @discord.ui.button(
        label="info", style=discord.ButtonStyle.secondary, emoji=Emojis.info_button
    )
    async def info_callback(self, _, interaction) -> None:
        """
        A function that edits the help message and shows "info commands"
        ---
        Arguments -> interaction : discord.Interacion
        """
        embed = discord.Embed(title="Info commands", color=Colors.gray)
        embed.add_field(name=f"{self.prefix}Ping", value="shows the latency of the bot")
        embed.add_field(
            name=f"{self.prefix}Avatar", value=f"{self.prefix}Avatar 'displays an image of User'"
        )
        embed.add_field(
            name=f"{self.prefix}self.prefix",
            value=f"changes the server prefix and can be used like '{self.prefix}prefix ! '",
        )
        await interaction.message.edit(embed=embed)
    @discord.ui.button(
        label="economy", style=discord.ButtonStyle.secondary, emoji=Emojis.economy_button
    )
    async def economy_callback(self, _, interaction) -> None:
        """
        A function that edits the help message and shows "economy commands"
        ---
        Arguments -> 
        interaction : discord.Interacion
        """
        embed = discord.Embed(title="Economy commands", color=Colors.gray)
        embed.add_field(
            name=f"{self.prefix}Balance",
            value=f"shows your balance or another user; can be used like '{self.prefix}balance'",
            inline=False
        )
        embed.add_field(
            name=f"{self.prefix}Beg",
            value=f"{self.prefix}Beg 'beg for money'",
            inline=False
        )
        embed.add_field(
            name=f"{self.prefix}Daily",
            value=f"{self.prefix}Daily 'get your daily money'",
            inline=False
        )
        embed.add_field(
            name=f"{self.prefix}coinflip",
            value=f"{self.prefix}coinflip 'flips a coin' , can be used like '{self.prefix}coinflip 100 tails' \n Arguments are Amount any whole number then 'heads' or 'tails'",
            inline=False
        )
        embed.add_field(
            name=f"{self.prefix}highlow",
            value=f"{self.prefix}highlow amount 'guess the number' \n Arguments are 'high' or 'low' and 'jackpot'",
            inline=False
        )
        await interaction.message.edit(embed=embed)
