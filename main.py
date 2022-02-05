from discord.ext import commands
from os import getenv, listdir
from discord import Intents, AllowedMentions
from commands.prefix import PrefixManager
from userdb import User


class LucidBot(commands.Bot):
    def __init__(self, token) -> None:
        self.token = token
        super().__init__(
            command_prefix=PrefixManager.prefix_for_bot_class,
            case_insensitive=True,
            intents=Intents.all(),
            strip_after_prefix=True,
            allowed_mentions=AllowedMentions(
                everyone=False, replied_user=False, roles=False
            ),
        )
        self.remove_command('help')
        self.load_extension("jishaku")
        self.get_command("jishaku").hidden = True
        """Jishaku is hidden within the help command"""
        for cog in listdir("./commands"):
            if cog.endswith(".py") and not cog.startswith("__"):
                try:
                    self.load_extension(f"commands.{cog[:-3]}")
                except Exception as e:
                    raise e

    @property
    def server_invite_url(self) -> str:
        return "https://discord.gg/GMSSNu3z4n"

    @property
    def bot_invite_url(self) -> str:
        return self.INVITE_URL

    async def on_ready(self) -> None:
        await PrefixManager.table_check()
        await User.table_check()
        print('Done checking tables')
        self.INVITE_URL = f"https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=3691367512&scope=bot%20applications.commands"

    def run(self):
        super().run(self.token)


if __name__ == "__main__":
    bot = LucidBot(getenv("token"))
    bot.run()
