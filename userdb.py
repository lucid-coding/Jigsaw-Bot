import aiosqlite
import discord

# just a fake push
class User:
    @staticmethod
    async def table_check() -> None:
        """
        A PrefixHandler static method that checks if the tables were maid or not
        ---
        Arguments -> None
        """
        async with aiosqlite.connect("database/user.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                CREATE TABLE IF NOT EXISTS USERS (
                    user_id bigint UNIQUE,
                    balance bigint
                )
                """
                )
                await connection.commit()

    @staticmethod
    async def balance(user: discord.Member = None) -> int:
        """
        A method that returns a user Balance
        ---
        user : discord.Member
        """
        async with aiosqlite.connect("database/user.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                SELECT balance FROM USERS
                WHERE user_id = ?
                """,
                    (user.id,),
                )
                if x := await cursor.fetchone():
                    return x[0]
                return 0

    @staticmethod
    async def add_balance(user: discord.Member, amount: int = 100) -> bool:
        """
        A method that adds balance to a user
        ---
        user : discord.Member
        amount : int
        """
        async with aiosqlite.connect("database/user.db") as connection:
            async with connection.cursor() as cursor:
                statement = """
                        INSERT INTO USERS (user_id, balance) VALUES (:a, :b)
                        ON CONFLICT(user_id) DO UPDATE SET balance = balance + :b
                        WHERE user_id = :a
                         """
                await cursor.execute(statement, {"a": user.id, "b": amount or 0})
                await connection.commit()

    @staticmethod
    async def remove_balance(user: discord.Member, amount: int = 100) -> bool:
        """
        A method that removes balance to a user
        ---
        user : discord.Member
        amount : int
        """
        async with aiosqlite.connect("database/user.db") as connection:
            async with connection.cursor() as cursor:
                statement = """
                        INSERT INTO USERS (user_id, balance) VALUES (:a, :b)
                        ON CONFLICT(user_id) DO UPDATE SET balance = balance - :b
                        WHERE user_id = :a
                         """
                await cursor.execute(statement, {"a": user.id, "b": amount or 0})
                await connection.commit()

    @staticmethod
    async def test() -> None:
        async with aiosqlite.connect("database/user.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                SELECT * FROM USERS
                """
                )
                return await cursor.fetchall()
