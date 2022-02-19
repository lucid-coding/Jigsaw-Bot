import random
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

    def __init__(self, bot, active_players : list = None , number_of_times_played : dict = None):
        self.bot = bot
        self.active_players = active_players or []
        self.number_of_times_played = number_of_times_played or {}
    
    def _highlow(self) -> Tuple[int, int]:
        """
        A method that returns a Tuple containing the number and the hint
        ---
        Arguments -> None
        """
        hint = None
        number = random.randint(1,100,10)
        if number > 30 and number < 90:
            hint = random.randrange(number-30,number+10)
        elif hint is None:
            return self._highlow()
        return number, hint
    
    async def cog_check(self,ctx):
        """
        A Cog check
        ---
        Arugments -> 
        ctx : commands.Context
        """
        return not ctx.author.bot
    
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
            description=f"{user.name}'s balance is {await User.balance(user)}{Emojis.currency_emoji}",
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
            description=f"{ctx.author.name} got 1000{Emojis.currency_emoji} due to using the daily command and now they have {await User.balance(ctx.author)}{Emojis.currency_emoji}",
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
            embed = discord.Embed(title = f"{ctx.author.name}'s highlow command",description=f'you guessed wrong, you lost 100{Emojis.currency_emoji} the number was {number}',color=Colors.yellow)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ImageUrls.lose_url)
            embed.set_footer(text=f"{ctx.author.name}'s highlow command", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            await User.remove_balance(ctx.author,number)
    
    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.command()
    async def pull(self,ctx) -> Optional[Coroutine]:
        """
        Skip -  Skip is a game of strategy
        Extra
        The bot gives the player an offer for skipping. example if the play plays with 500 coins and the bot offers 200 coins more the player can choose to skip the offer for a better one, the bot can give the player a higher reward or the bot can choose to take the money randomly. Saying { You failed }. Skips can go on as long as it wants and only stops when the player says stop or looses the money.

        Command
        !skip 500 - betting 500 to play
        stop - stopping command 
        ---
        Arguments ->
        ctx : commands.context
        """
        user_balance = await User.balance(ctx.author)
        if 500 >= user_balance:
            return await ctx.send(
                embed=discord.Embed(
                    title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                    description=f"you don't have enough money you need atleast 500 {Emojis.currency_emoji}",
                    color=Colors.red,
                )
            )

        if ctx.author.id in self.active_players:
            return await ctx.send(embed= discord.Embed(description=f'{ctx.author.name} you are already in a game',color=Colors.red))
        else : self.active_players.append(ctx.author.id)
        def check(m):
            """
            check function for the skip command
            ---
            Arguments ->
            m : discord.Message
            """
            return m.author == ctx.author and m.channel == ctx.channel
        amount = 500
        embed = discord.Embed(title = f"{ctx.author.name}'s skip command",description=f'{ctx.author.name} you have {await User.balance(ctx.author)} coins the game costs 500{Emojis.currency_emoji}\n use "skip" to go for a higher bet and "stop" to secure the bag. **anything else would be taken as "skip"**',color=Colors.yellow)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=ImageUrls.bag_url)
        embed.set_footer(text=f"{ctx.author.name}'s skip command", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        while ctx.author.id in self.active_players:
            try:
                bet = await self.bot.wait_for('message',check=check,timeout=30)
                if bet.content.lower() == 'stop':
                    try:
                        self.number_of_times_played[ctx.author.id] - 1
                    except KeyError:
                        embed = discord.Embed(title=f'{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}', description="you just started, you can't end it right now")
                        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                        embed.set_thumbnail(url=ImageUrls.error_url)
                        embed.set_footer(text=f"{ctx.author.name}'s skip command", icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        continue


                    self.active_players.remove(ctx.author.id)
                    await User.add_balance(ctx.author,amount)
                    embed = discord.Embed(description=f'{ctx.author.name} you have stopped the game you won {amount}{Emojis.currency_emoji}',color=Colors.yellow)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    embed.set_thumbnail(url=ImageUrls.bag_url)
                    embed.set_footer(text=f"{ctx.author.name}'s skip command", icon_url=ctx.author.avatar.url)
                    return await ctx.send(embed=embed)
                if not random.randrange(0,3) and bet.content.lower() != 'stop':
                    self.active_players.remove(ctx.author.id)
                else:
                    self.number_of_times_played[ctx.author.id] = self.number_of_times_played.get(ctx.author.id,0) + 1 or 1
                    if self.number_of_times_played[ctx.author.id] >= 3:
                        amount *= 2
                    else:
                        amount += 500
                    embed = discord.Embed(description=f"the bet is now at {amount}{Emojis.currency_emoji} send 'stop' to secure it or skip to continue",color=Colors.yellow)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    embed.set_thumbnail(url=ImageUrls.bag_url)
                    embed.set_footer(text=f"{ctx.author.name}'s skip command", icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
            except asyncio.TimeoutError:
                await User.remove_balance(ctx.author,500)
                return await ctx.send(f"{ctx.author.name} you took too long to play, you have lost your skip command")
        else:
            embed = discord.Embed(
                title=f"{ctx.author.name}'s skip command",
                description=f"you failed",
                color=Colors.red,
            ) 
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ImageUrls.lose_url)
            embed.set_footer(text=f"{ctx.author.name}'s skip command", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            await User.remove_balance(ctx.author,500)
    
    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.command(aliases=['give','gift','give_money','give_coins','give_credits'])
    async def pay(self,ctx, user : discord.Member, amount : int) -> Optional[Coroutine]:
        """
        Pay -  Pay is a game of strategy
        ---
        """
        if amount < 0 or not isinstance(amount,int):
            embed = discord.Embed(
                title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                description="you can't pay negative or non-integer amounts or anything besides an integer",
                color=Colors.red,
            )

            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ImageUrls.error_url)
            embed.set_footer(text=f"{ctx.author.name}'s pay command", icon_url=ctx.author.avatar.url)
            return await ctx.send(embed=embed)
        elif amount > await User.balance(ctx.author):
            embed = discord.Embed(
                title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                description=f"you don't have enough money to do that,  you have {amount}{Emojis.currency_emoji}",
                color=Colors.red,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ImageUrls.error_url)
            embed.set_footer(text=f"{ctx.author.name}'s pay command", icon_url=ctx.author.avatar.url)
            return await ctx.send(embed=embed)
        await User.remove_balance(ctx.author,amount)
        if isinstance(user,int):
            await User.add_balance(ctx.guild.get_member(user),amount)
        else:
            await User.add_balance(user,amount)
        embed = discord.Embed(
            title='Transaction done',
            description=f"{ctx.author.name} has paid {user.name} {amount}{Emojis.currency_emoji}",
            color=Colors.green,
        )

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text=f"{ctx.author.name} sounds like a daddy material ", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Economy(bot))
