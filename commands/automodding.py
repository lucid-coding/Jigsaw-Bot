from discord.ext import commands


class AutoModding(commands.Cog):
    ...


def setup(bot):
    bot.add_cog(AutoModding(bot))
