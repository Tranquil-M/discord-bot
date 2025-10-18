import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
import random

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

with open('./cogs/bot_statuses.txt') as f:
    statuses = f.readlines()
    bot_statuses = cycle(statuses)

@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(activity=discord.CustomActivity(name=next(bot_statuses)))

@bot.event
async def on_ready():
    change_status.start()
    print(f'{bot.user.name} is ready to rumble!')

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