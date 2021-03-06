# run `pip install -U discord.py` to install discord.py
# run `pip install -U python-dotenv` to install dotenv

from datetime import date
import os

import time
import discord
from dotenv import load_dotenv
from discord.ext import tasks, commands


load_dotenv()
# loads the token from the .env file

# GUILD = os.getenv('DISCORD_GUILD')

# get client object rom discord.py
intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!')



# A Client is an object that represents a connection to Discord. A Client handles events, tracks state, and generally interacts with Discord APIs.
# client = discord.Client()

# on_ready() will be called the message will be printed once client is ready for further action. (When bot switches from Offline to Online)
@bot.event
async def on_ready():
    # guild_count = 0
    #Here, you looped through the guild data that Discord has sent client, namely client.guilds. Then, you found the guild with the matching name and printed a formatted string to stdout.
    # for guild in bot.guilds:
    #     guild_count += 1
    #     if guild.name == GUILD:
    #         break
            
#    print(
#        f'{bot.user} is connected to {guild_count} guild/s:\n'
#        f'{guild.name}(id: {guild.id})'
#    )
    check_for_anniversary.start()
    # Output:
    # Mel's Bot#4009 is connected to the following guild:
    # League of Feminist Coders(id: 761684935949025290)


# Event listener for when a message is sent to a channel
# @bot.event
# async def on_message(message):
#     if message.author.id == 341022026636591114:
#         await message.channel.send("Shuddup Mel!")


@tasks.loop(hours=24)
async def check_for_anniversary():

    todays_date = date.today()
    channel_to_upload_to = bot.get_channel(941789786568548372)

    for guild in bot.guilds:
        for member in guild.members:
            joined = member.joined_at
            if joined.month == todays_date.month and joined.day == todays_date.day and joined.year != todays_date.year:
                length = todays_date.year - joined.year
                if length == 1:
                    await channel_to_upload_to.send("It's {member.mention}'s anniversary! They have been a **{guild.name}** member for **{length} year**! :tada:")
                elif length > 1:
                    await channel_to_upload_to.send("It's {member.mention}'s anniversary! They have been a **{guild.name}** member for **{length} years**! :tada:")


@bot.command()
async def anniversary(ctx, user: discord.User):
    todays_date = date.today()
    joined = user.joined_at

    #checks if already celebrated this year or not
    if joined.month >= todays_date.month:
        if joined.month == todays_date.month and joined.day > todays_date.day:
            has_celebrated = False
        elif joined.month == todays_date.month and joined.day < todays_date.day:
            has_celebrated = True
        else:
            has_celebrated = False
    else:
        has_celebrated = True

    if has_celebrated:
        anniversary = date(year=todays_date.year + 1, month=joined.month, day=joined.day)
        days_left = anniversary - todays_date
    else:
        anniversary = date(year=todays_date.year, month=joined.month, day=joined.day)
        days_left = anniversary - todays_date
    try:
        await ctx.send(f"{user.name} joined on {joined.strftime('%m/%d/%Y')}. Only {days_left.days} days left to celebrate! :partying_face:")
    except commands.errors.UserNotFoundUserNotFound:
        await ctx.send(f"{user} is invalid. Try again.")


# execute Bot
bot.run(process.env.DISCORD_TOKEN)
