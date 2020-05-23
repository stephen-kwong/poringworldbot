import logging
import os

from poringworldbot.bot import bot

logging.basicConfig()
logging.getLogger('poringworldbot').setLevel(logging.INFO)

token = os.environ.get('DISCORD_TOKEN')

if not token:
    print('Please set the DISCORD_TOKEN environment variable.')
    exit(1)

bot.run(token)
