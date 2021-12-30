from discord.ext import commands


class Welcome(commands.Cog):
    """
    A Cog that handles most everything when a member joins
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        ...

    @commands.command()
    async def set_welcome(self,ctx):
        ...

def setup(bot):
    bot.add_cog(Welcome(bot))
