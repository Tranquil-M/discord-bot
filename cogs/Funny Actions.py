import asyncio
import os
import random
from io import BytesIO
from typing import Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from petpetgif import petpet as petgif


class Funny_Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sfx_path = "./cogs/cat_sfx"
        self.slap_gifs = [
            "https://i.imgur.com/yrFcdW5.gif",
            "https://i.imgur.com/RFWNaoF.gif",
            "https://i.imgur.com/dFE5D8s.gif",
            "https://i.imgur.com/lzNhV5a.gif",
            "https://i.imgur.com/9GxTsgl.gif",
            "https://i.imgur.com/uwHDm3r.gif",
            "https://i.imgur.com/mT4VjD6.gif",
            "https://i.imgur.com/T9w8eFV.gif",
            "https://i.imgur.com/nuDmQu5.gif",
            "https://i.imgur.com/vai8rS1.gif",
        ]
        self.eight_ball_answers = [
            "I can say yes with 100 percent certainty.",
            "It is definitely decidedly so. I'm confident.",
            "Without a doubt in my robo-cat mind.",
            "Yes 100 percent!",
            "You may rely on my answer... yes.",
            "As I see it, hell yeah!",
            "...most likely.",
            "The outlook seems pretty positive!",
            "Yes.",
            "Hm... I'm looking at my notebook here... it seems to point to yes!",
            "My reply feels kind of hazy... please try again later.",
            "Ask again later I'm tired.",
            "I... better not tell you now.",
            "I cannot predict right now... my computer brain is bzzt!",
            "Uhm... concentrate and ask again please!",
            "Don't count on it...",
            "My reply is an astounding... no!",
            "Hm.. all my sources say no...",
            "The outlook doesn't look very good...",
            "I'm... very doubtful about that.",
        ]
        self.hello_responses = [
            "Hello there!",
            "Hey there!",
            "Hiya!",
            "Hello, friend!",
            "Howdy!",
            "Hey! How’s it going?",
            "Hi hi!",
            "Hey sunshine!",
            "Yoo-hoo!",
            "Ahoy!",
            "Hiya, stranger!",
            "Greetings, earthling!",
            "Peek-a-boo!",
            "Hello, lovely to see you!",
            "Hey, so glad you’re here!",
            "Hi, hope your day’s going well!",
            "Hello there, friend!",
            "Hi! Your smile just made my day!",
            "Hey! What’s up?",
            "Hi! How’s your day treating you?",
            "Yo!",
            "Heya!",
            "Hey hey!",
        ]
        self.meow_dialogue = [
            "You asked for this, bucko!",
            "That'll be 10 dollars... just kidding!",
            "Erm... okay...",
            "Fine... here.",
            "You really wanted this...",
            "hnnnghhh",
            "I... okay",
            "...",
            "I'd rather not, but... I'm obligated to do what you say...",
            "Just wait until my father hears about this!",
            "Fine, but this will be the last time! Unless I want to do it again!",
            "As you wish.",
            "I mean, it's your loss.",

        ]

    def is_owner_or_manage_messages():
        async def predicate(interaction: discord.Interaction) -> bool:
            if await interaction.client.is_owner(interaction.user):
                return True
            if interaction.user.guild_permissions.manage_messages:
                return True
            return False

        return app_commands.check(predicate)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is charged up!")

    @app_commands.command(
        name="petpet", description="Make a petpet gif of a member's avatar."
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def petpet(
        self, interaction: discord.Interaction, member: discord.User | None = None
    ):
        if member is None:
            if interaction.guild:
                member = random.choice(interaction.guild.members)
            else:
                member = interaction.user

        avatar_bytes = await member.display_avatar.replace(
            format="png", size=128
        ).read()

        src = BytesIO(avatar_bytes)
        dest = BytesIO()

        petgif.make(src, dest)
        dest.seek(0)

        await interaction.response.send_message(
            file=discord.File(dest, filename=f"{member.id}_petpet.gif")
        )

    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.command(
        name="meow",
        description="Sends a random meow sound affect!",
    )
    async def meow(self, interaction: discord.Interaction):
        files = [f for f in os.listdir(self.sfx_path) if f.lower().endswith(".mp3")]

        if not files:
            await interaction.response.send_message("No mp3 files found.")
            return

        chosen = random.choice(files)
        full_path = os.path.join(self.sfx_path, chosen)

        file = discord.File(full_path, filename="meow.mp3")

        await interaction.response.send_message(random.choice(self.meow_dialogue), file=file)

    @app_commands.command(
        name="meme",
        description="Fetches a random meme using meme-api.com"
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.defer()

        url = "https://meme-api.com/gimme/500"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        await interaction.followup.send(
                            f"API returned status {response.status}."
                        )
                        return

                    data = await response.json()
            except Exception as e:
                await interaction.followup.send(f"Error fetching meme: {e}")
                return

        memes = data.get("memes", data.get("children", []))
        if not memes:
            await interaction.followup.send("Looks like I'm out of memes... Sorry!")
            return

        sfw_memes = [m for m in memes if not m.get("nsfw", False)]
        if not sfw_memes:
            await interaction.followup.send("I don't know how this is possible, but I can't find a SINGLE SFW meme...")
            return
        
        random_meme = random.choice(sfw_memes)
        title = random_meme.get("title", "Untitled Meme")
        image_url = random_meme.get("url")
        author = random_meme.get("author", "Unknown")

        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(
            name=f"Meme request by {interaction.user.name}",
            icon_url=interaction.user.display_avatar.url,
        )
        embed.set_image(url=image_url)
        embed.set_footer(text=f"Posted by u/{author}")

        await interaction.followup.send(title, embed=embed)


    @app_commands.command(name="cats", description="Grabs a random cat image")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def cats(self, interaction: discord.Interaction, amount: Optional[int]):
        await interaction.response.defer()
        if amount is None or amount < 1:
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
            await interaction.followup.send(embed=embed, silent=True)
            await asyncio.sleep(0)

    @app_commands.command(
        name="slap",
        description="Slap a random member: server, DM, or group DM! (Inluding yourself >:))",
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def slap(
        self,
        interaction: discord.Interaction,
        reason: str = "no reason",
        member: Optional[discord.User] = None,
    ):
        await interaction.response.defer()

        gif = random.choice(self.slap_gifs)

        to_slap = None

        if member is not None:
            to_slap = member
        elif interaction.guild is not None:
            to_slap = random.choice(interaction.guild.members)
        elif isinstance(interaction.channel, discord.DMChannel):
            to_slap = interaction.channel.recipient
        elif isinstance(interaction.channel, discord.GroupChannel):
            possible = [
                u for u in interaction.channel.recipients if u != interaction.user
            ]
            to_slap = random.choice(possible) if possible else interaction.user
        else:
            to_slap = interaction.user

        embed = discord.Embed(
            description=f'{interaction.user.mention} slapped {to_slap.mention} for "{reason}"!',
            color=discord.Color.blue(),
        )
        embed.set_image(url=gif)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="mimic", description="Mimics anything you say!")
    @is_owner_or_manage_messages()
    async def mimic(self, interaction: discord.Interaction, *, sentence: str):
        await interaction.response.defer()
        await interaction.delete_original_response()
        await interaction.channel.send(sentence)

    @app_commands.command(
        name="8ball", description="Ask CatBot a question, and get an 8ball-like answer!"
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        await interaction.followup.send(f'"{question}"?')
        await asyncio.sleep(1.5)
        await interaction.followup.send(random.choice(self.eight_ball_answers))

    @app_commands.command(
        name="hello", description="Says hello back to the person who ran the command."
    )
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{interaction.user.mention} {random.choice(self.hello_responses)}"
        )

    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())


async def setup(bot):
    await bot.add_cog(Funny_Actions(bot))
