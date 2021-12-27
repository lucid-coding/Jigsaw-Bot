import asyncpg
import os
from discord.ext import commands
import discord
from config import DNS2, TOKEN,DNS1


async def create_db_pool2():
    bot.db2 = await asyncpg.create_pool(
        dsn=DNS1
    )


async def get_pre(bot, message) -> str:
    """
    A corotinue where it gets the message and returns a string
        ---
    Arguments -> bot : discord.Object
    message - > discord.Contenxt
    """
    prefix = await bot.db2.fetch(
        "SELECT prefix from prefix_table WHERE id = $1", message.guild.id
    )
    if prefix:
        return prefix[0]
    return "$"


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_pre, case_insensitive=True, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    activity = discord.Game(name="$help")
    await bot.change_presence(status=discord.Status.idle, activity=activity)


async def create_db_pool():
    """creates a database pool""
    ---
    Arguments -> None
    """
    bot.db = await asyncpg.create_pool(
        dsn=dns2
    )


async def create_db_pool3():
    """a database for blacklist and stuff related to it
    ---
    Arguments -> None
    """
    bot.blacklist_db = await asyncpg.create_pool(
        dsn=DNS2
    )


bot.loop.run_until_complete(create_db_pool())
bot.loop.run_until_complete(create_db_pool2())
bot.loop.run_until_complete(create_db_pool3())
for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

bot.load_extension("jishaku")
bot.run(TOKEN)
