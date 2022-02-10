from types import coroutine
import aiosqlite
from discord.ext import commands
import discord
from constants import Colors, Replies, Emojis
import random


class Welcome(commands.Cog):
    """
    A Cog that handles most everything when a member joins
    """

    def __init__(self, bot, server_config=None):
        self.bot = bot
        self.server_config = server_config or {}

    async def cog_command_error(self, ctx, error) -> coroutine:
        """
        A cog command error handler
        ---
        ctx : discord.Context
        error : discord.ext.commands.errors.CommandError
        """
        return await ctx.send(
            embed=discord.Embed(
                title=f"{random.choice(Replies.error_replies)} {random.choice(Emojis.pepe_sad_emojis)}",
                description=error,
                color=Colors.red,
            )
        )

    @staticmethod
    async def table_check() -> None:
        """
        A static method that creates the tables for the database if they don't exist
        ---
        Arguments -> None
        ---
        Returns -> None
        """
        async with aiosqlite.connect("database/config.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS config(
                        guild_id bigint UNIQUE,
                        welcome_channel_id bigint,
                        welcome_message TEXT,
                        welcome_enabled boolean
                    )
                    """
                )
                await connection.commit()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """
        A corotinue that adds all info to server_config
        ---
        Arguments -> None
        ---
        Returns -> None
        """
        async with aiosqlite.connect("database/config.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT * FROM config
                    """
                )
                rows = await cursor.fetchall()
                self.server_config = {
                    row[0]: {
                        "welcome_channel_id": row[1],
                        "welcome_message": row[2],
                        "welcome_enabled": row[3],
                    }
                    for row in rows
                }

    @commands.has_permissions()
    @commands.command()
    async def set_welcome(
        self, ctx, *, welcome_channel_id: int = None, welcome_message: str = None
    ) -> None:
        if len(welcome_channel_id) > 18:
            welcome_message = welcome_channel_id
            welcome_channel_id = ctx.channel.id

        """
        A command that sets the welcome channel and welcome message
        if you're planning on using the welcome command just know that you can replace user with $user_mention so it would mention the user and you can replace server with $server_name so it would mention the server
        ---
        ctx : discord.Context
        welcome_channel_id : int
        welcome_message : str
        ---
        Returns -> None

        """
        await ctx.send(
            "just know that you can replace user with $user_mention so it would mention the user and you can replace server with $server_name so it would mention the server"
        )
        async with aiosqlite.connect("database/config.db") as connection:
            async with connection.cursor() as cursor:
                statement = """
                INSERT INTO config (guild_id, welcome_channel_id, welcome_message, welcome_enabled) VALUES (:guild_id, :welcome_channel_id, :welcome_message, :welcome_enabled)
                ON CONFLICT(guild_id) DO UPDATE SET welcome_channel_id = :welcome_channel_id, welcome_message = :welcome_message, welcome_enabled = :welcome_enabled
                Where guild_id = :guild_id
                """
                await cursor.execute(
                    statement,
                    {
                        "guild_id": ctx.guild.id,
                        "welcome_channel_id": welcome_channel_id,
                        "welcome_message": welcome_message,
                        "welcome_enabled": True,
                    },
                )
                await connection.commit()
                await ctx.send(
                    embed=discord.Embed(
                        title="Success",
                        description="Welcome channel and message set",
                        color=Colors.green,
                    )
                )
                self.server_config[ctx.guild.id] = {
                    "welcome_channel_id": welcome_channel_id or ctx.channel.id,
                    "welcome_message": welcome_message
                    or f"welcome $ to {ctx.guild.name}",
                    "welcome_enabled": True,
                }

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        """
        A corotinue that sends a welcome message to the welcome channel
        ---
        member : discord.Member
        ---
        Returns -> Nono
        """
        if member.guild.id not in self.server_config:
            return
        embed = discord.Embed(
            title=f"welcome to {member.guild.name}",
            description=self.server_config[member.guild.id]["welcome_message"]
            .replace("$user_mention", member.mention)
            .replace("$server_name", member.guild.name),
        )
        try:
            embed.set_author(name=member.name, icon_url=member.avatar.url)
        except AttributeError:
            embed.set_author(
                name=member.name,
                icon_url="https://cdn.discordapp.com/avatars/820603175048445953/21de117dd05693a61884f01fadc21cf6.png?size=1024",
            )
        try:
            embed.set_thumbnail(url=member.avatar.url)
        except AttributeError:
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/820603175048445953/21de117dd05693a61884f01fadc21cf6.png?size=1024"
            )
        embed.set_footer(text=member.guild.member_count, icon_url=member.guild.icon.url)
        channel = await member.guild.get_channel(
            self.server_config[member.guild.id]["welcome_channel_id"]
        ).send(embed=embed)
        await channel.send(member.mention, embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))
