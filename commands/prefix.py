from typing import Optional
from aiosqlite.core import Connection
from discord.ext import commands
import aiosqlite
from discord import Message


class PrefixHandler(commands.Cog):
    """
    A That handles Stuff related to the Database
    """

    @commands.command()
    async def prefix(self, ctx: commands.Context, new_prefix: str) -> Message:
        await PrefixManager.prefix_setter(ctx, new_prefix)
        return await ctx.send(f"prefix has been set to {new_prefix}")


def setup(bot):
    bot.add_cog(PrefixHandler(bot))


class PrefixManager:
    """
    Class for actually dealing with the bot's prefix database
    """

    async def prefix_for_bot_class(bot: commands.Bot, message: Message):
        prefix = await PrefixManager.prefix_getter(message)
        return commands.when_mentioned_or(prefix)(bot, message)

    @staticmethod
    async def table_check() -> None:
        """
        A PrefixHandler static method that checks if the tables were maid or not
        ---
        Arguments -> None
        """
        async with aiosqlite.connect("database/guilds.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                CREATE TABLE IF NOT EXISTS prefixes(
                    guild_id bigint,
                    prefix TEXT
                    
                )
                """
                )

    async def prefix_setter(
        ctx: commands.Context, new_prefix: str
    ) -> Optional[Connection]:
        """
        A Corotinue that gets the prefix of the guild.
        ---
        Arguments ->
        ctx : commands.Context
        new_prefix: str
        """
        async with aiosqlite.connect("database/guilds.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT * FROM prefixes
                    WHERE guild_id = ?
                    """,
                    (ctx.guild.id,),
                )
                if await cursor.fetchone():
                    await cursor.execute(
                        """
                        UPDATE prefixes
                        SET prefix = ?
                        WHERE guild_id = ?
                        """,
                        (
                            new_prefix,
                            ctx.guild.id,
                        ),
                    )
                else:
                    await cursor.execute(
                        """
                        INSERT INTO prefixes
                        ( guild_id , prefix )
                        VALUES (? , ?)
                        """,
                        (
                            ctx.guild.id,
                            new_prefix,
                        ),
                    )
                return await connection.commit()

    async def prefix_getter(message: Message) -> str:
        """
        A Corotinue that gets the prefix of the guild.
        ---
        Arguments ->
        bot : commands.Object , "which is the bot in other words or the object of commands"
        message : commands.Message
        """

        async with aiosqlite.connect("database/guilds.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT * FROM prefixes
                    WHERE guild_id = ?
                    """,
                    (message.guild.id,),
                )
                data = await cursor.fetchone()
            return data[1] if data else "$"
