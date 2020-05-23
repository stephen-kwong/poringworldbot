import logging
import os

import poringworldbot
from poringworldbot.bot import bot

logging.basicConfig(
    level=logging.WARNING,
    handlers=[logging.StreamHandler()],
)
logging.getLogger(poringworldbot.__name__).setLevel(logging.INFO)

token = os.environ.get('DISCORD_TOKEN')

if not token:
    print('Please set the DISCORD_TOKEN environment variable.')
    exit(1)

bot.run(token)
