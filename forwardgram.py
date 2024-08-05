from telethon import TelegramClient, events, sync
from telethon.tl.types import InputChannel
import yaml
import sys
import logging
import discord
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

''' 
------------------------------------------------------------------------
                LOGGING - Inititate logging for the Bot
------------------------------------------------------------------------
'''
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

''' 
------------------------------------------------------------------------
    BOT FUNCTION - Everything that happens, happens for a reason
------------------------------------------------------------------------
'''
def start(config):
    # Telegram Client Init
    client = TelegramClient(config["session_name"], 
                            config["api_id"], 
                            config["api_hash"])
    # Telegram Client Start
    client.start()

    # Input Messages Telegram Channels will be stored in these empty Entities
    input_channels_entities = []
    output_channel_entities = []

    # Iterating over dialogs and finding new entities and pushing them to our empty entities list above
    for d in client.iter_dialogs():
        if d.name in config["input_channel_names"] or d.entity.id in config["input_channel_ids"]:
            input_channels_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
        if d.name in config["output_channel_names"] or d.entity.id in config["output_channel_ids"]:
            output_channel_entities.append(InputChannel(d.entity.id, d.entity.access_hash))

    # Exit, don't wait for fire.        
    if not output_channel_entities:
        logger.error(f"Could not find any output channels in the user's dialogs")
        sys.exit(1)

    if not input_channels_entities:
        logger.error(f"Could not find any input channels in the user's dialogs")
        sys.exit(1)
    
    # Use logging and print messages on your console.     
    logging.info(f"Listening on {len(input_channels_entities)} channels. Forwarding messages to {len(output_channel_entities)} channels.")
    

    # TELEGRAM NEW MESSAGE - When new message triggers, come here

    @client.on(events.NewMessage(chats=input_channels_entities))
    async def handler(event):
        for output_channel in output_channel_entities:
            try:
                parsed_response = (event.message.message + '\n' + event.message.entities[0].url )
                parsed_response = ''.join(parsed_response)
            except:
                parsed_response = event.message.message

            # Start discord messenger script and send the message
            subprocess.call(["python", "discord_messager.py", str(parsed_response)])
            # Forward message to Telegram output channels
            await client.forward_messages(output_channel, event.message)  

    client.run_until_disconnected()

''' 
------------------------------------------------------------------------
          MAIN FUNCTION - Can't dream without a brain ...
------------------------------------------------------------------------
'''

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} {{CONFIG_PATH}}")
        sys.exit(1)
    
    # Load configuration from YAML file
    with open(sys.argv[1], 'rb') as f:
        config = yaml.safe_load(f)

    # Start the bot
    start(config)
