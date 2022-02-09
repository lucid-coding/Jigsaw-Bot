import random
from tkinter import Image
import discord
import asyncio
import random
from famous_acters import acters
from discord.ext import commands
from userdb import User
from constants import Emojis, ImageUrls, Replies, Colors
from typing import Coroutine, Optional, Tuple, Union
from buttons import Delete_button
from discord.ui import View


class Economy(commands.Cog):
    """
    A cog for all commands related to economy or its database
    ---
    Inherting from commands.Cog which allows this to be a cog class
    """

    def __init__(self, bot):
        self.bot = bot

    def _highlow(self) -> Tuple[int, int]:
        """
        A method that returns a Tuple containing the number and the hint
        ---
        Arguments -> None
        """
        hint = None
        number = random.randint(1,100)
        if number > 30 and number < 90:
            hint = random.randrange(number-30,number+10)
        elif hint is None:
            return self._highlow()
        return number, hint

    async def cog_command_error(self, ctx, error) -> Coroutine:
        """
        A cog command error handler
        ---
        ctx : discord.Context
        error : discord.ext.commands.errors.CommandError
        ---
        Returns -> Coroutine
        """
        view = View()
        button = Delete_button(ctx)
        view.add_item(button)
        if isinstance(error, commands.CommandOnCooldown):
            if error.retry_after > 3600:
                embed = discord.Embed(
                    title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                    description=f"You are on cooldown for {str(error.retry_after / 3600)[:2]} hours",
                    color=Colors.red,
                )
                return await ctx.send(
                    embed=embed, delete_after=error.retry_after, view=view
                )
            elif error.retry_after > 60 and error.retry_after < 3600:
                embed = discord.Embed(
                    title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                    description=f"You are on cooldown for {str(error.retry_after / 60 )[:2]} minutes",
                    color=Colors.red,
                )
                return await ctx.send(
                    embed=embed, delete_after=error.retry_after, view=view
                )
            else:
                embed = discord.Embed(
                    title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                    description=f"You are on cooldown for {str(error.retry_after)[:2]} seconds",
                    color=Colors.red,
                )
                return await ctx.send(
                    embed=embed, delete_after=error.retry_after, view=view
                )

        return await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                description=error,
                color=Colors.red,
            ),
            view=view,
        )

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, user: discord.Member = None):
        """
        Gets the balance of the user or the author
        ---
        Arguments ->
        user : discord.Member
        """
        user = user or ctx.author
        embed = discord.Embed(
            description=f"{user.name}'s balance is {await User.balance(user)}{Emojis.coin_emoji}",
            color=Colors.green,
        )
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.set_thumbnail(
            url=ImageUrls.bank_url
        )
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.set_footer(text=f"{user.name}'s balance", icon_url=user.avatar.url)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command()
    async def daily(self, ctx) -> None:
        """
        A corotuine that gives a user their daily command
        ---
        Arguments ->
        ctx : discord.Context
        """
        await User.add_balance(ctx.author, 1000)
        embed = discord.Embed(
            description=f"{ctx.author.name} got 1000$  due to using the daily command and now they have {await User.balance(ctx.author)}",
            color=Colors.green,
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(
            text=f"{ctx.author.name}'s daily command", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["cf", "coinflip", "flip", "coin", "flipcoin"])
    async def coin_flip(
        self, ctx, amount: Union[int, str], heads_or_tails: str
    ) -> Optional[Coroutine]:
        """
        A coint flip command
        ---
        Arguments ->
        ctx : discord.Context
        amount : int
        heads_or_tails : str
        """
        if heads_or_tails not in ["heads", "tails", "h", "t","head","tail"]:
            return await ctx.send(
                embed=discord.Embed(
                    description=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                    color=Colors.red,
                )
            )
        if amount == "all":
            amount = await User.balance(ctx.author)
        if amount < 100:
            embed = discord.Embed(
                description=f"{ctx.author.name} you need to bet at least 100{Emojis.currency_emoji}",
                color=Colors.red,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/918891402224611379/939945659056934913/unknown.png"
            )
            return await ctx.send(embed=embed)
        if random.randrange(0, 2):
            await User.add_balance(ctx.author, amount)
            embed = discord.Embed(
                description=f"{ctx.author.name} won {amount}{Emojis.currency_emoji} and now they have {await User.balance(ctx.author)}{Emojis.currency_emoji}",
                color=Colors.yellow,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/918891402224611379/939945659056934913/unknown.png"
            )
            embed.set_footer(
                text=f"{ctx.author} won {amount} coin flip",
                icon_url=ctx.author.avatar.url,
            )
            return await ctx.send(embed=embed)
        await User.remove_balance(ctx.author, amount)
        embed = discord.Embed(
            description=f"{ctx.author.name} lost {amount}{Emojis.currency_emoji} and now they have {await User.balance(ctx.author)}{Emojis.currency_emoji}",
            color=Colors.red,
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/918891402224611379/939945659056934913/unknown.png"
        )
        embed.set_footer(
            text=f"{ctx.author} lost {amount}'s coin flip",
            icon_url=ctx.author.avatar.url,
        )
        return await ctx.send(embed=embed)

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command()
    async def beg(self, ctx) -> Coroutine:
        """
        A command where a user begs for money
        ---
        Arguments ->
        ctx : discord.Context
        ---
        Returns -> Coroutine
        """
        amount = random.randrange(100, 1000, step=50)
        if not random.randrange(0, 4):
            embed = discord.Embed(
                description=f"{acters[random.randrange(0,len(acters))]['name']} says {random.choice(Replies.begging_responds)}",color=Colors.gray
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            return await ctx.send(embed=embed)
        await User.add_balance(ctx.author, amount)
        embed = discord.Embed(
            description=f"{acters[random.randrange(0,len(acters))]['name']} gave {ctx.author.name} {amount}{Emojis.currency_emoji} , {random.choice(Replies.positive_replies)}",
            color=Colors.yellow
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.set_footer(
            text=f"{ctx.author.name}'s beg command, now they have {await User.balance(ctx.author)} coins ", icon_url=ctx.author.avatar.url)
        return await ctx.send(embed=embed)

    @commands.cooldown(1,30,commands.BucketType.user)
    @commands.command(aliases=['hl','lowhigh'])
    async def highlow(self,ctx) -> Coroutine:
        """
        A highlow command
        ---
        Arguments ->
        ctx : discord.Context
        ---
        Returns -> Coroutine
        """
        def check(m):
            """
            check function for the highlow command
            ---
            Arguments ->
            m : discord.Message
            """
            return m.author == ctx.author and m.channel == ctx.channel
        balance = await User.balance(ctx.author)
        if balance <= 99:
            return await ctx.send(
                embed=discord.Embed(
                    title=f"you don't have enough money you need atleast 100 {Emojis.currency_emoji}",
                    description=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                    color=Colors.red,
                )
            )
        number , hint = self._highlow()
        embed = discord.Embed(title = f"{ctx.author.name}'s highlow command",description=f'your hint is {hint}',color=Colors.yellow)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.set_footer(text=f"{ctx.author.name}'s highlow command", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        try:
            guess = await self.bot.wait_for('message',check=check,timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send(f"{ctx.author.name} you took too long to guess, you have lost your highlow command")
        
        if guess.content.lower() in ['jackpot','jp','jackpot!','hit'] and hint == number:
            await User.add_balance(ctx.author,number**2*2)
            embed = discord.Embed(
                description=f"{ctx.author.name} YOU GOT THE JACKPOT RIGHT !!! {number} and won {number**2*2}{Emojis.currency_emoji}")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ImageUrls.treasure_url)
            embed.set_footer(
                text=f"{ctx.author.name}'s highlow command, now they have {await User.balance(ctx.author)} coins ", icon_url=ctx.author.avatar.url)
        elif guess.content.lower() in ['high','higher','h'] and number > hint:
            embed = discord.Embed(title = f"{ctx.author.name}'s highlow command",description=f'you guessed high, you won {number}{Emojis.currency_emoji}',color=Colors.yellow)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ImageUrls.win_url)
            embed.set_footer(text=f"{ctx.author.name}'s highlow command", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            await User.add_balance(ctx.author,number)
        elif guess.content.lower() in ['low','lower','l'] and number < hint:
            embed = discord.Embed(title = f"{ctx.author.name}'s highlow command",description=f'you guessed low, you won {number}{Emojis.currency_emoji}',color=Colors.yellow)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ImageUrls.win_url)
            embed.set_footer(text=f"{ctx.author.name}'s highlow command", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            await User.add_balance(ctx.author,number)
        else:
            embed = discord.Embed(title = f"{ctx.author.name}'s highlow command",description=f'you guessed wrong, you lost {number}{Emojis.currency_emoji} the number was {number}',color=Colors.yellow)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ImageUrls.lose_url)
            embed.set_footer(text=f"{ctx.author.name}'s highlow command", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            await User.remove_balance(ctx.author,number)

            

def setup(bot):
    bot.add_cog(Economy(bot))
