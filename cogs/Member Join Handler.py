import discord
from discord.ext import commands
import os
import random
import easy_pil

class Member_Join_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} is ready to go! I think...')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = member.guild.system_channel
        images = [image for image in os.listdir('./cogs/welcome_images')]
        random_image = random.choice(images)

        bg = easy_pil.Editor(f'./cogs/welcome_images/{random_image}').resize((1920, 1080))

        avatar_image = await easy_pil.load_image_async(str(member.display_avatar.url))
        avatar = easy_pil.Editor(avatar_image).resize((250, 250)).circle_image()

        font_big = easy_pil.Font.poppins(size=80, variant='bold')
        font_small = easy_pil.Font.poppins(size=60, variant='bold')

        bg.paste(avatar, (835, 340))
        bg.ellipse((830, 335), 259, 259, outline='white', stroke_width=5)

        bg.text((960, 620), f'Welcome to {member.guild.name}, {member.name}!', color='white', font=font_big, align = 'center')
        bg.text((960, 740), f'You are our {member.guild.member_count}th member! yayyyy!', color='white', font=font_small, align = 'center')

        file = discord.File(fp=bg.image_bytes, filename=random_image)

        await welcome_channel.send(f'Hey, {member.mention}! Please read and follow the rules in the rules channel, thank you!')
        await welcome_channel.send(file=file)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = member.guild.system_channel
        images = [image for image in os.listdir('./cogs/leaving_images')]
        file = discord.File(f'./cogs/leaving_images/{random.choice(images)}')
        await channel.send(f'NOOOOO!!! COME BACKKKK!!! {member.name.upper()}!!!')
        await channel.send(file=file)

async def setup(bot):
    await bot.add_cog(Member_Join_Handler(bot))