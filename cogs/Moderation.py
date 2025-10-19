import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation is ready to mod!')

    @app_commands.command(name='clear', description='Deletes a specified amount of messages from the current channel.')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def delete_messages(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer()
        if amount < 1:
            await interaction.delete_original_response()
            await interaction.followup.send(f'{interaction.user.mention} you can\'t subtract zero, man! Put a positive integer, come on now.', ephemeral=True)
            return
        elif amount > 500:
            await interaction.delete_original_response()
            await interaction.followup.send(f'WOAH, {interaction.user.mention}! Calm down! Keep under 500 please? I have my limits too!', ephemeral=True)
            return
        
        deleted_messages = await interaction.channel.purge(limit = amount)
        await asyncio.sleep(2)
        await interaction.channel.send(f'Deleted {len(deleted_messages)} messages! ...you can\'t bring them back. So I hope you did this right!')

    @app_commands.command(name='kick', description='Kicks a specified member.')
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await interaction.guild.kick(member)
        await interaction.response.send_message(f'{member.mention} has walked the plank! The reason why is apparently "{reason}". Ouch. Courtesy of {interaction.user.mention}!', ephemeral=True)

    @app_commands.command(name='ban', description='Bans a specified member from the server.')
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await interaction.guild.ban(member)
        await interaction.response.send_message(f'{member.mention} has kicked the bucket! The reason why is apparently "{reason}". Damn. Kinda harsh don\'t you think? Thanks, {interaction.user.mention}.', ephemeral=True)

    @app_commands.command(name='unban', description='Unbans a specified member by their user ID.')
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member_identifier: str):
        await interaction.response.defer()
        try:
            member_name = member_identifier

            async for ban_entry in interaction.guild.bans():
                user = ban_entry.user
                if (user.name) == (member_name):
                    await interaction.guild.unban(user)
                    await interaction.followup.send(f"Unbanned {user.name}. Welcome back!", ephemeral=True)
                    return

            await interaction.followup.send(f"Okay, um... says here '{member_identifier}' isn\'t, like, banned? Try a different user.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("I do not have the necessary permissions to unban users. Gimme perms. Please.")
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Moderation(bot))