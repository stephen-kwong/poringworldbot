import os

from poringworldbot.bot import bot

token = os.environ.get('DISCORD_TOKEN')

if not token:
    print('Please set the DISCORD_TOKEN environment variable.')
    exit(1)

bot.run(token)
