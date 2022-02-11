# run `pip install -U discord.py` to install discord.py
# run `pip install -U python-dotenv` to install dotenv

import os

import discord
from dotenv import load_dotenv

load_dotenv()
# loads the token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# A Client is an object that represents a connection to Discord. A Client handles events, tracks state, and generally interacts with Discord APIs.
client = discord.Client()

# on_ready() will be called the message will be printed once client is ready for further action.
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)