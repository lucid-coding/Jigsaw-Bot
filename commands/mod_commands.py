import asyncio
import typing
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.errors import Forbidden
from discord.ext.commands import BucketType
from discord.ext import commands
from typing import Coroutine, Optional
import discord
from discord.ui.view import View
from constants import Colors, Emojis, Replies
import random
from buttons import Delete_button, HelpView
import datetime


class ban(commands.Cog):
    """
    A cog for banning members -> None
    No arguements can be passed within objects.
    """

    def __init__(self, bot, muted_people=None, last_user=None):
        self.bot = bot
        self.last_user = last_user
        self.muted_people = {} if muted_people is None else muted_people

    def converter(self, time_unit):

        """
        A time_unit coverter
        return time * unit as an exmaple
        1h is time * 60 * 60
        first ons is converting it to minutes then hours
        ---
        Arguments would looks something like
        int string thats one letter long. either h , s , d ,

        """
        time = time_unit[:-1]
        unit = time_unit[-1]

        conv = {"h": time * 60 * 60, "m": time * 60, "s": time}
        unit = unit.lower()
        return conv[unit]

    async def cog_command_error(self, ctx, error) -> Coroutine:
        """
        A Cog error handler
        ---
        arguements -> ctx discord.ctx
        error is the procided error.
        """
        view = View()
        button = Delete_button(ctx)
        view.add_item(button)
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(
            error,
            discord.Forbidden,
        ):

            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="the bot doesnt have enough perms",
                    color=Colors.red,
                ),
                view=view,
            )

        return await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)}"
                + f"{random.choice(Emojis.pepe_sad_emojis)}",
                description=error,
                color=Colors.red,
            ),
            view=view,
        )

    def check(self, ctx, user):
        if ctx.author is ctx.guild.owner:
            return True
        if not user.roles:
            return False
        if ctx.author.id == user.id:
            return True
        if ctx.author.top_role > user.top_role:
            return True
        return False

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, BucketType.member)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        if not self.check(ctx, user):
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="cant ban yourself or anyone higher than you",
                    color=Colors.red,
                )
            )

        if isinstance(user, int):
            user = self.bot.fetch_user(user)
            if not user:
                return await ctx.send(
                    embed=discord.Embed(
                        title=f"{random.choice(Replies.error_replies)}",
                        description="The id seems to be invalid.",
                        color=Colors.red,
                    )
                )

        if ctx.author.id == user.id:
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="cant mute yourself or anyone higher than you",
                    color=Colors.red,
                )
            )
        embed = discord.Embed(
            title=f"{user.name} got banned from {ctx.guild}",
            description=f" Reason : {reason}",
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(
            text=f"executed by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        try:
            await user.send(
                embed=discord.Embed(
                    title=f"you got banned from {ctx.guild}",
                    description=f"Reason : {reason} ",
                )
            )
        except Forbidden:
            await ctx.send(
                "they have their dms close. I couldn’t DM <:dead:901964054766178314>"
            )
        finally:
            await user.ban(reason=reason, delete_message_days=0)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, BucketType.member)
    async def unban(
        self, ctx, *, member: typing.Union[discord.Object, discord.User]
    ) -> None:
        """
        Unban command only a user can be passed
        ---
        Arguement Union[discord.Object,discord.User, discord.Member]
        -> None
        """
        await ctx.guild.unban(member)
        embed = discord.Embed(title="user got unbanned")
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(
            text=f"executed by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, BucketType.member)
    @commands.command()
    async def pban(self, ctx, user: discord.Member, *, reason=None) -> Coroutine:
        """
        Purge banned command, Purges a user messages and bans them
        ---
        Arugments
        ctx : discord.ctx
        user : discord.Member
        reason : string

        """
        if not self.check(ctx, user):
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="cant ban yourself or anyone higher than you",
                    color=Colors.red,
                )
            )
        if isinstance(user, int):
            user = self.bot.fetch_user(user)
            if not user:
                return await ctx.send(
                    embed=discord.Embed(
                        title=f"{random.choice(Replies.error_replies)}",
                        description="The id seems to be invalid.",
                        color=Colors.red,
                    )
                )

        if user.id == ctx.author.id:
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="you cant ban yourself",
                    color=Colors.red,
                )
            )
        embed = discord.Embed(
            title=f"{user} got banned !",
            description=f"{user} have been banned for {reason}; their messages have been purged",
        )
        try:
            await user.send(
                embed=discord.Embed(
                    title=f"You got banned from {ctx.guild}",
                    description=f"Reason : {reason} ",
                )
            )
        except Exception as e:
            await ctx.send(
                "they have their dms close. I couldn’t DM <:dead:901964054766178314>"
            )
            print(e, f"occured in {__file__} line number -> 141")
        finally:
            await ctx.guild.ban(user=user, reason=reason, delete_message_days=7)
            await ctx.send(embed=embed)

    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, BucketType.member)
    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason="there was no reason."):
        """
        A command that kicks a user
        ---
        Arguments ->
        user
        """
        if not self.check(ctx, user):
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="cant kick yourself or anyone higher than you",
                    color=Colors.red,
                )
            )
        if user.id == ctx.author.id:
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="you cant kick yourself",
                    color=Colors.red,
                )
            )
        if user is None:
            return await ctx.send(
                discord.Embed(
                    title="an error occured", description="mention a user to kick"
                )
            )

        embed = discord.Embed(
            title=f"{user.name} got kicked from {ctx.guild}",
            description=f"Reason : {reason}",
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(
            text=f"executed by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        try:
            xembed = discord.Embed(
                title=f"You got kicked from {ctx.guild}",
                description=f"Reason : {reason}\n",
            )
            xembed.set_thumbnail(url=user.avatar.url)
            xembed.add_field(name="\u200b", value=f"Got kicked by : {ctx.author}")
            await user.send(embed=xembed)
        except Forbidden:
            await ctx.send(
                "they have their dms close. I couldn’t DM <:dead:901964054766178314>"
            )
        finally:
            await user.kick(reason=reason)
            await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx) -> None:
        await ctx.send(
            embed=discord.Embed(
                title="Pong!",
                description=f"Pong! {round(self.bot.latency *1000)}ms",
                color=Colors.green,
            )
        )

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(
        self,
        ctx,
        user: discord.Member,
        time_n_unit="1h",
        *,
        reason="there was no reason",
    ) -> Coroutine:
        """
        A command that mutes a user
        ---
        Arguments ->
        ctx : discord.ctx
        user : discord.Member which represents a discord user or a account.
        time_n_unit : str ,which represents the time and the unit
        reason : str , "The reason for the mute"
        """
        if not self.check(ctx, user):
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="cant mute yourself or anyone higher than you",
                    color=Colors.red,
                )
            )
        if user.id == ctx.author.id:
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="you cant mute yourself",
                    color=Colors.red,
                )
            )
        if isinstance(user, int):
            role = ctx.guild.get(user)
            if not role:
                return await ctx.send(
                    embed=discord.Embed(
                        title=f"{random.choice(Replies.error_replies)}",
                        description="The id seems to be invalid.",
                        color=Colors.red,
                    )
                )
        if user is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="please mention someone to mute",
                    color=Colors.red,
                )
            )
        reason = reason or "Reason: None"

        def function_converter(time):
            unit = time[-1]
            time = int(time.replace(unit, " "))

            if not isinstance(time, int):
                return "add a unit"

            if not isinstance(unit, str):
                return "make sure the unit is valid"
            conv = {"h": time * 60 * 60, "m": time * 60, "s": time}
            return conv[unit]

        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role is None:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(
                    muted_role,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                    read_messages=True,
                )
            await ctx.send("muted role was not found , finished creating one")
        await user.add_roles(muted_role)
        try:
            x = function_converter(time_n_unit)
        except ValueError:
            x = 3600
            reason = "Reason: None"
            time_n_unit = "1h"
        self.muted_people[user.id] = x
        embed = discord.Embed(title=f"{user.name} has been muted")
        embed.add_field(
            name="\u200b", value=f"**Reason**: {reason}\n **Time**: {time_n_unit}"
        )
        embed.set_footer(
            text=f"executed by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)
        await asyncio.sleep(x)
        await user.remove_roles(muted_role)
        self.muted_people.pop(user.id)
        await ctx.send(
            embed=discord.Embed(
                title="unmute !", description=f"{user.name} has been unmuted !"
            )
        )

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        """
        A command that unmutes a user, if there isnt a Muted discord.Object.role
        ---
        Arguments
        ctx : discord.ctx
        user : dicsord.Member . "which is a user/ account"
        """
        if isinstance(user, int):
            role = ctx.guild.get(user)
            if not role:
                return await ctx.send(
                    embed=discord.Embed(
                        title=f"{random.choice(Replies.error_replies)}",
                        description="The id seems to be invalid.",
                        color=Colors.red,
                    )
                )

        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            return await ctx.send(
                embed=discord.Embed(
                    title="Role Error",
                    description="you dont seem to have the Muted role , it would autocreate when trying to mute anyone ",
                    color=Colors.red,
                )
            )
        if not self.check(ctx, user):
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="cant mute yourself or anyone higher than you",
                    color=Colors.red,
                )
            )
        if user.id == ctx.author.id and not ctx.guild.owner:
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="you cant unmute yourself",
                    color=Colors.red,
                )
            )

        if role := discord.utils.get(user.roles, name="Muted"):
            await user.remove_roles(role)
            embed = discord.Embed(title=f"{user} got unmuted")
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(
                text=f"executed by {ctx.author}", icon_url=ctx.author.avatar.url
            )
            try:
                self.muted_people.pop(user.id)
            except ValueError:
                await ctx.send(
                    embed=discord.Embed(
                        title="that following user isn't muted ", color=Colors.red
                    )
                )

            return await ctx.send(embed=embed)
        await ctx.send(
            embed=discord.Embed(
                title="that following user isn't muted ", color=Colors.red
            )
        )

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        if member.id in self.muted_people:
            muted_role = discord.utils.get(member.guild.roles, name="Muted")
            await member.add_roles(muted_role)
            try:
                await asyncio.sleep(self.muted_people[member.id])
            except Exception as E:
                raise E
            await member.remove_roles(muted_role)

    @commands.command(aliases=["ava", "av"])
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"", description="", color=ctx.author.color)
        embed.set_footer(
            text=f"{member} profile picture ", icon_url=f"{ctx.guild.icon.url}"
        )
        view = View()
        button = Delete_button(ctx, discord.ButtonStyle.gray)
        view.add_item(button)
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.cooldown(1, 15, BucketType.member)
    async def help(self, ctx):
        """
        Are you lost ? feel free to use the help command.
        ---
        Arguements -> None
        """
        view = HelpView(ctx)
        button = Delete_button(ctx)
        view.add_item(button)
        await ctx.send(
            embed=discord.Embed(title="Help commands", color=Colors.gray), view=view
        )

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(
        self,
        ctx,
        user: discord.Member,
        time: int = 1,
        unit: str = "hours",
        *,
        reason=None,
    ) -> None:
        """
        A timeout command
        ---
        Arguements
        takes in a user : discord.Member
        time :s tr -> Optional
        unit : int -> Optional
        *reason :str -> Optional
        """
        reason = reason or "Nothing"
        if not self.check(ctx, user):
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="cant timeout yourself or anyone higher than you",
                    color=Colors.red,
                )
            )
        if user.id == ctx.author.id:
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="you cant timeout yourself",
                    color=Colors.red,
                )
            )
        if unit.lower() in ["hour", "hours", "h"]:
            time_object = datetime.timedelta(hours=time)
        elif unit.lower() in ["min", "minutes", "minute"]:
            time_object = datetime.timedelta(minutes=time)
        elif unit.lower() in ["Day", "Days"]:
            time_object = datetime.timedelta(days=time)
        elif unit.lower() in ["secs", "sec", "secounds", "s"]:
            time_object = datetime.timedelta(seconds=time)
        final = discord.utils.utcnow() + time_object
        await user.edit(timeout_until=final)
        view = View()
        button = Delete_button(ctx, ButtonStyle.gray)
        view.add_item(button)
        await ctx.send(
            embed=discord.Embed(
                title=f"{user.name} got timedout",
                description=f"{user.mention} got timed out for {time}{unit} For {reason}",
                color=Colors.green,
            ),
            view=view,
        )

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, user: discord.Member) -> Optional[Coroutine]:
        """
        A command that removes the timeout from a person
        """
        view = View()
        button = Delete_button(ctx, ButtonStyle.gray)
        view.add_item(button)
        if user:
            await user.edit(timeout_until=discord.utils.utcnow())
            return await ctx.send(
                embed=discord.Embed(
                    title=f"",
                    description=f"{user.name} got their timeout removed",
                    color=Colors.green,
                    view=view,
                )
            )
        await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                description="Missing user Argument",
                color=Colors.red,
            ),
            view=view,
        )


def setup(bot):
    bot.add_cog(ban(bot))
