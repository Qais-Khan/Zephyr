# bot.py
import os
import random
import sys
import time
import discord

from discord.ext import commands
from dotenv import load_dotenv
from dadjokes import Dadjoke



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
avatar = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwhatthechuck007.tumblr.com%2Fpost%2F642126554452967424&psig=AOvVaw1Qz16d8a_gjKog9UTpsctU&ust=1647322772511000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCMD8393xxPYCFQAAAAAdAAAAABAJ'
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    channel = bot.get_channel(944347370739605555)
    print(f'{bot.user.name} has connected to Discord!')
    await channel.send("WTF Do You Want From Me")

@bot.command(name='Suby', help='Tells the Truth')
async def suby(ctx):
    Wisdom = [
        'Dumbass',
        'Indecisive Dimwit',
        'Why are you this way',
        'Kinda cool sometimes'
    ]
    response = random.choice(Wisdom)
    await ctx.send(response)

# @bot.command(name='Nuke', help='Nuke the Channel')
# async def clear(ctx, amount = 100):
#     await ctx.channel.purge(limit=amount)
@bot.command(name="Speak", help="Nothing rn")
async def embed(ctx):
    embed=discord.Embed(title="Click Me!", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="Figuring out how embeds works so everything doesn't look like shit lol", color=discord.Color.blue())
    embed.set_thumbnail(url=avatar)
    embed.add_field(name="WORDS!", value="Apparently I can Put Text Here", inline=False) 
    embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))


    await ctx.send(embed=embed)

@bot.command(name="Joke", help="Tells a Fantastic Dad Joke")
async def jokes(ctx):
    dadjoke = Dadjoke()
    embed=discord.Embed(title="Dad Jokes", description=dadjoke.joke, color=discord.Color.purple())
    embed.set_thumbnail(url=avatar)
    embed.set_footer(text="Joke requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


    
bot.run(TOKEN)