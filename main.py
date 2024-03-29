# bot.py
from multiprocessing.connection import deliver_challenge
import os
import random
import re
import time
import discord
import datetime
import pymongo
import pytz
import requests

from pytz import timezone
from discord.ext import commands
from dotenv import load_dotenv
from dadjokes import Dadjoke
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from pandas import describe_option




days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

ToDoList = [
  {"Monday" : [],'index':0},
  {"Tuesday" : [],'index':1},
  {"Wednesday" : [],'index':2},
  {"Thursday" : [], 'index':3},
  {"Friday" : [],'index':4},
  {"Saturday" : [],'index':5},
  {"Sunday" : [],'index':6}
]

load_dotenv()
MONGO_KEY = os.getenv('MONGO_KEY')
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='-')
client = pymongo.MongoClient(MONGO_KEY)
db = client.test
url = 'https://getpickuplines.herokuapp.com/lines/random'


if "To_Do" not in db.list_collection_names():
    db.create_collection("To_Do")
    toDo = db.To_Do
    toDo.insert_many(ToDoList)


toDo = db.To_Do


def is_user(ctx):
    return ctx.author.id == 759271189410873426

@bot.event
async def on_ready():
    channel = bot.get_channel(952400947823398955)
    print(f'{bot.user.name} has connected to Discord!')
    await channel.send("WTF Do You Want From Me")

@bot.command(name='Suby', help='Tells the Truth')
async def suby(ctx):
    Wisdom = [
        'Dumbass',
        'Indecisive Dimwit',
        'Why are you this way',
        'Kinda cool sometimes',
        'Dresses like an aunty lol',
        'Who?',
        'Imagine Being a BME defect lol',
        'Such a simp (Courtesy of Lucas)',
        'Silly Suby',
        'Pretty Pog <:poggy:934688467538030622>',
        '<:lmaocry:933424582805827634>'
    ]
    response = random.choice(Wisdom)
    await ctx.send(response)

@bot.command(name='Nuke', help='Nuke the Channel')
async def clear(ctx, amount = 120):
    await ctx.channel.purge(limit=amount)

@bot.command(name="Joke", help="Tells a Fantastic Dad Joke")
async def jokes(ctx):
    dadjoke = Dadjoke()
    embed=discord.Embed(title="Dad Jokes", description=dadjoke.joke, color=discord.Color.purple())
    embed.set_footer(text="Joke requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)

@bot.command(name="Flirt", help="Steals your heart")
async def flirt(ctx, name = 'nothing'):

    am = discord.AllowedMentions(
            users=False,
            roles=False,
            everyone=False
        )

    req = requests.get(url)
    if (name != 'nothing'):
        await ctx.send(name + ', ' + req.json()['line'], allowed_mentions = am)
    else:
        embed=discord.Embed(title="Dad Jokes", description=req.json()['line'], color=discord.Color.purple())
        embed.set_footer(text="Joke requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)

@bot.command(name="commands", help="Displays this list of Commands")
async def jokes(ctx):
    embed=discord.Embed(title="Commands", color=discord.Color.purple())
    embed.add_field(name="Joke", value="Tells A Great Dad Joke", inline=False)
    embed.add_field(name="Flirt", value="Steals Your Heart", inline=False)
    # embed.add_field(name="Suby", value="Tells The Cold Hard Truth",inline=False)
    # embed.add_field(name="DueToday", value="Lets You Know What's Due Today!", inline=False) 
    embed.add_field(name="Due", value="Lets You Know What's Due On A Given Day!",inline=False) 
    embed.set_footer(text="Help requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


@bot.command(name="ToDo", help="Shows What Is Due Today!")
@has_permissions(administrator=True)
async def ToDoThisWeek(ctx):
    embed=discord.Embed(title="What's Due This Week?", description=description, color=discord.Color.purple())
    tasks = []
    counter = 0
    for x in days:
        cursor = toDo.find()[counter]
        for y in range(0, len(cursor[x])):
            tasks.append(cursor[x][y])
        deliverables = '\n'.join(tasks)
        embed.add_field(name= str(x) + ":", value=deliverables, inline=False)
        tasks.clear()
        counter+=1

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    channel = bot.get_channel(886637950962659488)
    await channel.send("<@&826117559023435787>")
    await channel.send(embed=embed)

@ToDoThisWeek.error
async def error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await bot.send_message(ctx.message.channel, text)

@bot.command(name="Update", help="Shows What Is Due Today!")
@has_permissions(administrator=True)
async def ToDoThisWeek(ctx):
    embed=discord.Embed(title="What's Due This Week?", description=description, color=discord.Color.purple())
    tasks = []
    counter = 0
    for x in days:
        cursor = toDo.find()[counter]
        for y in range(0, len(cursor[x])):
            tasks.append(cursor[x][y])
        deliverables = '\n'.join(tasks)
        embed.add_field(name= str(x) + ":", value=deliverables, inline=False)
        tasks.clear()
        counter+=1

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    channel = bot.get_channel(886637950962659488)
    await channel.send(embed=embed)

@ToDoThisWeek.error
async def error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await bot.send_message(ctx.message.channel, text)

@bot.command(name="DescSet")
@commands.check(is_user)
async def desc(ctx, *args):
    global description
    description = ' '.join(args[0:])
    await ctx.send("Description set!")

@bot.command(name="Set", help="Set The Deliverables Due Each Day")
@commands.check(is_user)
async def ToDoSet(ctx, *args):
    day = args[0].title()
    counter = 0
    for x in days:
        if day == x:
            break
        counter +=1
    task = ' '.join(args[1:])
    toDo.update_one({'index': counter}, {'$push': {day: task}})
    cursor = toDo.find()[counter]
    print(cursor[day])
    await ctx.send("Done")

@bot.command(name="Clear", help="Clear deliverables")
@commands.check(is_user)
async def Clear(ctx, day = 'null'):
    if (day != 'null'):
        day = day.title()
        counter = 0
        for x in days:
            if day == x:
                break
            counter +=1
        toDo.update_one({'index': counter}, {'$set': {day: []}})
        cursor = toDo.find()[counter]
        print(cursor[day])
        await ctx.send("Done")
    else:
        counter = 0
        for x in days:
            toDo.update_one({'index': counter}, {'$set': {x: []}})
            counter +=1
        await ctx.send("Done")



@bot.command(name="DueToday", help="Shows What Is Due Today!")
async def Today(ctx):
    my_timezone=timezone('US/Pacific')
    day = datetime.date.today()
    print(day)
    # cursor = toDo.find()[day]
    # desc = []
    # for x in cursor[days[day]]:
    #     desc.append(x + '\n')
    # tasks = ' '.join(desc)
    
    # embed=discord.Embed(title="What's Due " + day + " ?", description = tasks, color=discord.Color.purple())
    # embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    # await ctx.send(embed=embed)
    

@bot.command(name="Due", help="Shows What Is Due On a Given Day!")
async def Today(ctx, day):
    day = day.title()
    counter = 0
    for x in days:
        if day == x:
            break
        counter +=1
    cursor = toDo.find()[counter]
    desc = []
    for x in cursor[day]:
        desc.append(x + '\n')
    description = ' '.join(desc)
    embed=discord.Embed(title="What's Due " + day + " ?", description = description, color=discord.Color.purple())
    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)

@bot.command(name='P', help='Hide your plays')
@has_permissions(administrator=True)
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=amount)

@bot.event
async def on_message(message):
    am = discord.AllowedMentions(
            users=False,
            roles=False,
            everyone=False
        )

    await bot.process_commands(message)
    if 'Gn zephy' in message.content.capitalize() :
        await message.reply('Gn ' + str(message.author.display_name) + "!", allowed_mentions = am)
    if '.move' in message.content:
        if message.author.guild_permissions.administrator == True:
            await message.channel.purge(limit=3)
    if '!move' in message.content:
        if message.author.guild_permissions.administrator == True:
                time.sleep(0.25)
                await message.channel.purge(limit=4)
    if 'Hi zephy' in message.content.capitalize() :
        await message.reply('Hi ' + str(message.author.display_name) + "! <:poggy:934688467538030622>", allowed_mentions = am)
    if 'Hey zephy' in message.content.capitalize() :
        await message.reply('Hey ' + str(message.author.display_name) + "! <:poggy:934688467538030622>", allowed_mentions = am)



bot.run(TOKEN)
