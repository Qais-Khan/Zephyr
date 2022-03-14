# bot.py
from multiprocessing.connection import deliver_challenge
import os
import random
import sys
import time
import discord
import calendar

from datetime import date
from discord.ext import commands
from dotenv import load_dotenv
from dadjokes import Dadjoke
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from pandas import describe_option



days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

ToDoList = {
  "Monday" : [],
  "Tuesday" : [],
  "Wednesday" : [],
  "Thursday" : [],
  "Friday" : [],
  "Saturday" : [],
  "Sunday" : []
}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='~')



def is_user(ctx):
    return ctx.author.id == 759271189410873426

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
        'Kinda cool sometimes',
        'Dresses like an aunty lol',
        'Who?',
        'Imagine Being a BME defect lol'
    ]
    response = random.choice(Wisdom)
    await ctx.send(response)

# @bot.command(name='Nuke', help='Nuke the Channel')
# async def clear(ctx, amount = 100):
#     await ctx.channel.purge(limit=amount)

@bot.command(name="Joke", help="Tells a Fantastic Dad Joke")
async def jokes(ctx):
    dadjoke = Dadjoke()
    embed=discord.Embed(title="Dad Jokes", description=dadjoke.joke, color=discord.Color.purple())
    embed.set_footer(text="Joke requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


@bot.command(name="commands", help="Displays this list of Commands")
async def jokes(ctx):
    embed=discord.Embed(title="Commands", color=discord.Color.purple())
    embed.add_field(name="Joke", value="Tells A Great Dad Joke", inline=False)
    embed.add_field(name="Suby", value="Tells The Cold Hard Truth")
    embed.add_field(name="DueToday", value="Lets You Know What's Due Today!") 
    embed.add_field(name="Due", value="Lets You Know What's Due On A Given Day!") 
    embed.set_footer(text="Help requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


@bot.command(name="ToDo", help="Shows What Is Due Today!")
@has_permissions(administrator=True)
async def ToDoThisWeek(ctx):
    embed=discord.Embed(title="What's Due This Week?", description=description, color=discord.Color.purple())
    tasks = []
    for x in days:
        for y in range(0, len(ToDoList[x])):
            tasks.append(ToDoList[x][y])
        deliverables = '\n'.join(tasks)
        embed.add_field(name= str(x) + ":", value=deliverables, inline=False)
        tasks.clear()

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    channel = bot.get_channel(886637950962659488)
    await channel.send("<@&826117559023435787>")
    await channel.send(embed=embed)

@ToDoThisWeek.error
async def error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await bot.send_message(ctx.message.channel, text)



@bot.command(name="DescSet", help="Shows What Is Due Today!")
@commands.check(is_user)
async def desc(ctx, *args):
    global description
    description = ' '.join(args[0:])
    await ctx.send("Description set!")

@bot.command(name="ToDoSet", help="Set The Deliverables Due Each Day")
@commands.check(is_user)
async def ToDoSet(ctx, *args):
    day = args[0].title()
    task = ' '.join(args[1:])
    ToDoList[day].append(task)
    print(ToDoList[day])
    await ctx.send("Done")

@bot.command(name="ToDoClear", help="Set The Deliverables Due Each Day")
@commands.check(is_user)
async def ToDoSet(ctx, day):
    day = day.title()
    ToDoList[day].clear()
    await ctx.send("Done")


@bot.command(name="DueToday", help="Shows What Is Due Today!")
async def Today(ctx):
    day = calendar.day_name[date.today().weekday()]
    embed=discord.Embed(title="What's Due " + day + " ?", color=discord.Color.purple())
    counter = 1
    for x in range(len(ToDoList[day])):
        embed.add_field(name= str(counter) + ":", value=ToDoList[day][x], inline=False)
        counter+=1
    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
    

@bot.command(name="Due", help="Shows What Is Due On a Given Day!")
async def Today(ctx, day):
    day = day.title()
    embed=discord.Embed(title="What's Due " + day + " ?", color=discord.Color.purple())
    counter = 1
    for x in range(len(ToDoList[day])):
        embed.add_field(name= str(counter) + ":", value=ToDoList[day][x], inline=False)
        counter+=1
    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)

@bot.command(name="ToDoUpdate", help="Shows What Is Due Today!")
@has_permissions(administrator=True)
async def ToDoThisWeek(ctx):
    embed=discord.Embed(title="What's Due This Week?", description=description, color=discord.Color.purple())
    tasks = []
    for x in days:
        for y in range(0, len(ToDoList[x])):
            tasks.append(ToDoList[x][y])
        deliverables = '\n'.join(tasks)
        embed.add_field(name= str(x) + ":", value=deliverables, inline=False)
        tasks.clear()

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    channel = bot.get_channel(886637950962659488)
    await channel.send(embed=embed)

bot.run(TOKEN)