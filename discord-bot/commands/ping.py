from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Trả về Pong!"""
        await ctx.send("Pong!")

# v2: sử dụng async setup
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
