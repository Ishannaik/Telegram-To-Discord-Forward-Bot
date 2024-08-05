import yaml
import sys
import logging
import discord
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

''' 
------------------------------------------------------------------------
    DISCORD CLIENT - Init the client
------------------------------------------------------------------------
'''

discord_client = discord.Client()

''' 
------------------------------------------------------------------------
    MESSAGE AS WE RECEIVE FROM FORWARDGRAM SCRIPT
------------------------------------------------------------------------
'''

message = sys.argv[1]

''' 
------------------------------------------------------------------------
    DISCORD SERVER START EVENT - We will kill this immaturely
------------------------------------------------------------------------
'''
@discord_client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discord_client))
    print('Awaiting Telegram Message')

    # Retrieve channels from Discord using IDs from environment variables
    channel_1 = discord_client.get_channel(int(os.getenv("DISCORD_1_CHANNEL")))
    channel_2 = discord_client.get_channel(int(os.getenv("DISCORD_2_CHANNEL")))
    channel_3 = discord_client.get_channel(int(os.getenv("DISCORD_3_CHANNEL")))
    channel_4 = discord_client.get_channel(int(os.getenv("DISCORD_4_CHANNEL")))

    # Send the message to the appropriate channel
    if 'Mario' in message:
        await channel_1.send(message)
    elif 'Zelda' in message:
        await channel_2.send(message)
    elif 'Minecraft' in message:
        await channel_3.send(message)
    elif 'Valhiem' in message:
        await channel_4.send(message)

    quit()

# Run the Discord client using the bot token from environment variables
discord_client.run(os.getenv("DISCORD_BOT_TOKEN"))
