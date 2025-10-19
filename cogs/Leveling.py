import discord
from discord.ext import commands

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Leveling is online and ready to get some execution points!')

async def setup(bot):
    await bot.add_cog(Leveling(bot))