import discord
from dotenv import load_dotenv
from discord_utils import MorseBotCilent 
import os


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True

    load_dotenv()

    client = MorseBotCilent(intents=intents)
    token = os.getenv('DISCORD_TOKEN')
    client.run(token)