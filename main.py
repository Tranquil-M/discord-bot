import discord
import asyncio
import random
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return f'{ctx.author} slapped {to_slap} because *{argument}*'

@bot.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)


@bot.command()
async def test(ctx, *arg1):
    if 'hi' or 'hello' in arg1:
        answer = "Hello! How can I assist you today?"
    await ctx.send(answer)

@bot.command()
async def mimic(ctx, *, arg):
    await ctx.send(arg)

with open('token.txt.gpg') as file:
    token = file.read()

bot.run(token)