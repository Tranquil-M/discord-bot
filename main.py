from code import interact
import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

with open('./cogs/bot_statuses.txt') as f:
    statuses = f.readlines()
    bot_statuses = cycle(statuses)

@tasks.loop(seconds=30)
async def change_status():
    await bot.change_presence(activity=discord.CustomActivity(name=next(bot_statuses)))

@bot.event
async def on_ready():
    change_status.start()
    print(f'{bot.user.name} is ready to rumble!')
    try:
        synced_commands = await bot.tree.sync()
        print(f'Synced {len(synced_commands)} commands.')
    except Exception as e:
        print('An error with suncing application commands has occurd: ', e)

@bot.tree.command(name='hello', description='Says hello back to the person who ran the command.')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'{interaction.user.mention} Hello there!')

with open('token.txt') as file:
    token = file.read()

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())