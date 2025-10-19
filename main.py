import datetime
import discord
from discord import app_commands
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv('./token.env')
TOKEN: str = os.getenv('TOKEN')

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
        print('An error with syncing application commands has occurd: ', e)

@bot.tree.command(name='hello', description='Says hello back to the person who ran the command.')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'{interaction.user.mention} Hello there!')

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(f"You don't have the required permissions to use this command. You need: {', '.join(error.missing_permissions)}. Sorry!", ephemeral=True)
    elif isinstance(error, app_commands.CommandInvokeError):
        await interaction.response.send_message(f'You\'re either trying to run this on yourself, or me. And I don\'t like the idea of either!', ephemeral=True)
    else:
        raise error

@bot.event
async def on_app_command_completion(interaction: discord.Interaction, command: discord.app_commands.Command):
    audit_channel = await get_or_create_audit_channel(interaction.guild)
    if audit_channel:
        embed = discord.Embed(
            title="Slash Command Executed",
            description=f"**Command:** `/{command.name}`",
            color=discord.Color.blue()
        )
        embed.add_field(name="User", value=interaction.user.mention, inline=True)
        embed.add_field(name="User ID", value=interaction.user.id, inline=True)
        embed.add_field(name="Channel", value=interaction.channel.mention, inline=True)
        embed.add_field(name="Guild", value=interaction.guild.name if interaction.guild else "Direct Message", inline=True)
        embed.set_footer(text=f"Timestamp: {datetime.datetime.now()}")
        
        await audit_channel.send(embed=embed)
    else:
        print(f"Audit log channel with ID {audit_channel} not found.")

async def get_or_create_audit_channel(guild: discord.Guild, name: str = "audit-log") -> discord.TextChannel:
    existing_channel = discord.utils.get(guild.text_channels, name=name)
    if existing_channel:
        return existing_channel

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        guild.owner: discord.Permissions(view_channel=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }

    for member in guild.members:
        if member.guild_permissions.administrator and member != guild.owner:
            overwrites[member] = discord.PermissionOverwrite(view_channel=True)

    new_channel = await guild.create_text_channel(name, overwrites=overwrites, reason="Creating audit log channel")
    return new_channel

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())