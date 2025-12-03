import asyncio
import os
import random
from io import BytesIO
from typing import Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from petpetgif import petpet


class Funny_Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sfx_path = "./cogs/cat_sfx"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is charged up!")

    @app_commands.command(
        name="pet", description="Make a petpet gif of a member's avatar."
    )
    async def pet(
        self, interaction: discord.Interaction, member: discord.Member | None = None
    ):
        target = member or random.choice(interaction.guild.members)

        avatar_bytes = await target.display_avatar.replace(
            format="png", size=128
        ).read()

        src = BytesIO(avatar_bytes)
        dest = BytesIO()

        petpet.make(src, dest)
        dest.seek(0)

        await interaction.response.send_message(
            file=discord.File(dest, filename=f"{target.id}_petpet.gif")
        )

    @app_commands.command(
        name="meow",
        description="Sends a random meow sound affect!",
    )
    async def meow(self, interaction: discord.Interaction):
        # choose mp3
        files = [f for f in os.listdir(self.sfx_path) if f.lower().endswith(".mp3")]

        if not files:
            await interaction.response.send_message("No mp3 files found.")
            return

        chosen = random.choice(files)
        full_path = os.path.join(self.sfx_path, chosen)

        # create file object
        file = discord.File(full_path, filename="meow.mp3")

        await interaction.response.send_message("You asked for this, bucko!", file=file)

    @app_commands.command(
        name="meme",
        description='Grabs a random meme from the "hot" category of r/memes',
    )
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.defer()
        url = "https://www.reddit.com/r/memes/hot.json?limit=500"
        headers = {"User-Agent": "CatBot/0.1 by Tranquil"}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        await interaction.followup.send(
                            f"Could not fetch memes, Reddit returned status {response.status}..."
                        )
                        return

                    data = await response.json()
            except Exception as e:
                await interaction.followup.send(f"Error fetching memes: {e}")
                return

        posts = data.get("data", {}).get("children", [])
        image_posts = [
            post["data"]
            for post in posts
            if post["data"].get("post_hint") == "image"
            and not post["data"].get("over_18", False)
        ]

        if not image_posts:
            await interaction.followup.send("No memes found. :sob:")
            return

        random_post = random.choice(image_posts)
        meme_embed = discord.Embed(
            color=discord.Color.blue(),
        )
        meme_embed.set_author(
            name=f"Meme request by {interaction.user.name}",
            icon_url=interaction.user.display_avatar.url,
        )
        meme_embed.set_image(url=random_post["url"])
        meme_embed.set_footer(
            text=f"Post created by {random_post.get('author', 'N/A')}", icon_url=None
        )

        await interaction.followup.send(
            random_post.get("title", "Untitled meme"), embed=meme_embed
        )

    @app_commands.command(name="cats", description="Grabs a random cat image")
    async def cats(self, interaction: discord.Interaction, amount: Optional[int]):
        await interaction.response.defer()
        if amount is None:
            amount = 1
        elif amount > 10:
            await interaction.followup.send(
                "Please keep it under 10 cats at a time! I don't have enough food to get more than 10 cats to pose... 😭"
            )
            await asyncio.sleep(3)
            await interaction.followup.send("Here, take a picture of me instead!")
            await asyncio.sleep(1.5)
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_image(url=self.bot.user.display_avatar.url)
            embed.set_footer(text="Most beautiful cat alive... 😮‍💨")
            await interaction.channel.send(embed=embed)
            return

        await interaction.followup.send("Come here kitties!")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thecatapi.com/v1/images/search?limit=10"
            ) as response:
                data = await response.json()
        embeds = []
        for i in range(amount):
            cat_image_url = data[i]["url"]
            i = discord.Embed(colour=discord.Colour.blue())
            i.set_image(url=cat_image_url)
            i.set_footer(
                text=f"Cats requested by {interaction.user.name}",
                icon_url=interaction.user.display_avatar.url,
            )
            embeds.append(i)

        for embed in embeds:
            await interaction.followup.send(embed=embed)
            await asyncio.sleep(0.1)

    @app_commands.command(
        name="slap", description="Slap a random server member (including yourself)! >:)"
    )
    async def slap(
        self,
        interaction: discord.Interaction,
        reason: Optional[str],
        member: discord.Member | None = None,
    ):
        await interaction.response.defer()
        if reason is None:
            await interaction.followup.send(
                "Please give a reason why at least! You can't just slap someone for no reason!"
            )
            return
        if member is not None:
            await interaction.followup.send(
                f"{interaction.user.name} slapped {member.mention} because *{reason}*"
            )
            await interaction.channel.send("👏👏👏")
            return

        to_slap = random.choice(interaction.guild.members)
        await interaction.followup.send(
            f"{interaction.user.name} slapped {to_slap} because *{reason}*"
        )
        await interaction.channel.send("👏👏👏")

    @app_commands.command(name="mimic", description="Mimics anything you say!")
    async def mimic(self, interaction: discord.Interaction, *, sentence: str):
        await interaction.response.defer()
        await interaction.followup.send(sentence)

    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())


async def setup(bot):
    await bot.add_cog(Funny_Actions(bot))
