import asyncpg
import os
from discord.ext import commands
import discord
from config import DNS, DNS2, TOKEN, DNS1

intents = discord.Intents(
    guild_reactions=True,  # reaction add/remove/clear
    guild_messages=True,  # message create/update/delete
    guilds=True,  # guild/channel join/remove/update
    integrations=True,  # integrations update
    voice_states=True,  # voice state update
    dm_reactions=True,  # reaction add/remove/clear
    guild_typing=True,  # on typing
    dm_messages=True,  # message create/update/delete
    presences=True,  # member/user update for games/activities
    dm_typing=True,  # on typing
    webhooks=True,  # webhook update
    members=True,  # member join/remove/update
    invites=True,  # invite create/delete
    emojis=True,  # emoji update
    bans=True,  # member ban/unban
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


bot = commands.Bot(
    command_prefix=get_pre,
    case_insensitive=True,
    intents=intents,
    slash_commands=True,
)
bot.remove_command("help")


@bot.event
async def on_ready():
    activity = discord.Game(name="$help")
    await bot.change_presence(status=discord.Status.idle, activity=activity)


async def create_pool():
    """a database for blacklist and stuff related to it
    ---
    Arguments -> None
    """
    bot.blacklist_db = await asyncpg.create_pool(dsn=DNS2)
    bot.db = await asyncpg.create_pool(dsn=DNS)
    bot.db2 = await asyncpg.create_pool(dsn=DNS1)


bot.loop.run_until_complete(create_pool())
for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
bot.load_extension("jishaku")
bot.get_command("jsk").hidden = True
bot.run(TOKEN)
