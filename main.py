import asyncpg
import os
from disnake.ext import commands
import disnake
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) # can be useless
TOKEN = os.getenv('DISCORD_TOKEN')
DNS1 = os.getenv('DNS1')
DNS2 = os.getenv('DNS"')

async def create_db_pool2():
    bot.db2 = await asyncpg.create_pool(
        dsn=DNS1
    )


async def get_pre(bot, message) -> str:
    """
    A corotinue where it gets the message and returns a string
        ---
    Arguments -> bot : disnake.Object
    message - > disnake.Contenxt
    """
    prefix = await bot.db2.fetch(
        "SELECT prefix from prefix_table WHERE id = $1", message.guild.id
    )
    if prefix:
        return prefix[0]
    return "$"


intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=get_pre, case_insensitive=True, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    activity = disnake.Game(name="$help")
    await bot.change_presence(status=disnake.Status.idle, activity=activity)


async def create_db_pool():
    """creates a database pool""
    ---
    Arguments -> None
    """
    bot.db = await asyncpg.create_pool(
        dsn="postgresql://postgres:xLzrH6DJUENGSpW0n8AE@containers-us-west-19.railway.app:6603/railway"
    )


async def create_db_pool3():
    """a database for blacklist and stuff related to it
    ---
    Arguments -> None
    """
    bot.blacklist_db = await asyncpg.create_pool(
        dsn=DNS2
    )


#bot.loop.run_until_complete(create_db_pool())
#bot.loop.run_until_complete(create_db_pool2())
#bot.loop.run_until_complete(create_db_pool3())
for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

bot.load_extension("jishaku")
bot.run(TOKEN)
