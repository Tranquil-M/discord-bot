from typing import Optional
import discord
from discord.ext import commands
import random
import asyncpraw as praw
import requests
import asyncio

class Funny_Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id='BhyUtvAUbIl2kazjgnFllA', client_secret='C0A-GwhXklnVHetor1ySMj1YJOBH3w', user_agent='script:Random_Meme:v1.0 (by u/Hot-Mind-4597)')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} is charged up!')

    @commands.command()
    async def meme(self, ctx: commands.Context):
        subreddit = await self.reddit.subreddit('memes')
        posts_list = []

        async for post in subreddit.hot(limit=60):
            if not post.over_18 and post.author is not None and any(post.url.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                author_name = post.author.name
                posts_list.append((post.url, author_name))
            if post.author is None:
                posts_list.append((post.url, 'N/A'))

        if posts_list:
            random_post = random.choice(posts_list)
            meme_embed = discord.Embed(color=discord.Color.blue())
            meme_embed.set_author(name=f'Meme request by {ctx.author.name}', icon_url=ctx.author.avatar.url)
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(text=f'Post created by {random_post[1]}.', icon_url=None)

            await ctx.send(embed=meme_embed)
        else:
            await ctx.send('Unable to fetch post, maybe the reddit server is down...?')

    @commands.command()
    async def cats(self, ctx: commands.Context, amount: Optional[int]):
        if amount == None:
            amount = 1
        elif amount > 10:
            await ctx.send('Please keep it under 10 cats at a time! I don\'t have enough food to get more than 10 cats to pose... 😭')
            await asyncio.sleep(1)
            await ctx.send('Here, take a picture of me instead!')
            await asyncio.sleep(1)
            embed = discord.Embed(colour = discord.Colour.blue())
            embed.set_image(url=self.bot.user.avatar.url) 
            embed.set_footer(text=f'Most beautiful cat alive... 😮‍💨')
            await ctx.send(embed=embed)
            return
            
        response = requests.get('https://api.thecatapi.com/v1/images/search?limit=10')
        data = response.json()
        embeds = []
        for i in range(amount):
            cat_image_url = data[i]['url']
            i = discord.Embed(colour = discord.Colour.blue())
            i.set_image(url=cat_image_url)
            i.set_footer(text=f'Cats requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
            embeds.append(i)
        
        for embed in embeds:
            await ctx.send(embed=embed)
            await asyncio.sleep(0.1)

    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())

async def setup(bot): 
    await bot.add_cog(Funny_Actions(bot))