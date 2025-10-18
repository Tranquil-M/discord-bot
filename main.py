import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
import random

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return f'{ctx.author} slapped {to_slap} because *{argument}*'

bot_statuses = cycle(['Thinking about you ♥️', 'I love cheese... and milk... I\'m not lactose intolerant I promise!', 'What\'s the difference between a snowman and a snow woman? The snow balls! 😎'])

@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(activity=discord.CustomActivity(name=next(bot_statuses)))

@bot.event
async def on_ready():
    change_status.start()
    print(f'{bot.user.name} is ready to rumble!')

@bot.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)

@bot.command()
async def mimic(ctx, *, arg):
    await ctx.send(arg)

@bot.command()
async def sendembed(ctx):
    embed = discord.Embed(title="Sample Embed", description="This is an example of an embedded message.", color = discord.Color.blue())
    embed.set_thumbnail(url=ctx.author.avatar.url)
    embed.add_field(name='Name of field', value='Value of field', inline=False)
    embed.set_image(url=ctx.guild.icon)
    embed.set_author(name='author text', icon_url=ctx.author.avatar.url)
    await ctx.send(embed = embed)

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