import asyncio
import typing
from discord.errors import Forbidden
from discord.ext.commands import BucketType
from discord.ext import commands
from typing import Coroutine
import discord
from discord.ui.view import View
from constants import Colors, Emojis, Replies
import random
from buttons import Delete_button, HelpView


class ban(commands.Cog):
    """
    A cog for banning members -> None
    No arguements can be passed within objects.
    """

    def __init__(self, bot, muted_people=None, last_user=None):
        self.bot = bot
        self.last_user = last_user
        self.muted_people = {} if muted_people is None else muted_people

    async def cog_command_error(self, ctx, error) -> Coroutine:

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
        await ctx.guild.unban(member)
        embed = discord.Embed(title=f"{member} got unbanned")
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(
            text=f"executed by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, BucketType.member)
    @commands.command()
    async def pban(self, ctx, user: discord.Member, *, reason=None):
        if not self.check(ctx, user):
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="cant ban yourself or anyone higher than you",
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
    ):
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
        if user is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="please mention someone to mute",
                    color=Colors.red,
                )
            )
        if reason is None:
            reason = "Reason: None"

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
        x = function_converter(time_n_unit)
        self.muted_people[user.id] = x
        embed = discord.Embed(title=f"{user.name} has been muted", inline=False)
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
        # await ctx.send(f'{function_converter(time_n_unit)} {reason=} {user.name=}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        if not self.check(ctx, user):
            return await ctx.send(
                embed=discord.Embed(
                    title="oh no an error occured",
                    description="cant ban yourself or anyone higher than you",
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

        role = discord.utils.get(user.roles, name="Muted")
        if role:
            await user.remove_roles(role)
            embed = discord.Embed(title=f"{user} got unmuted")
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(
                text=f"executed by {ctx.author}", icon_url=ctx.author.avatar.url
            )
            self.muted_people.pop(user.id)
            return await ctx.send(embed=embed)
        await ctx.send("that user isn't muted huh ?")

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
    @commands.cooldown(1, 30, BucketType.member)
    async def help(self, ctx):
        view = HelpView(ctx)
        button = Delete_button(ctx)
        view.add_item(button)
        await ctx.send(
            embed=discord.Embed(title="Help commands", color=Colors.gray), view=view
        )


def setup(bot):
    bot.add_cog(ban(bot))
