import os
import json
import motor.motor_asyncio as motor
from dotenv import load_dotenv

def get_prefix(ctx):
    with open(prefixFileName, 'r') as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(ctx.guild.id)]
    except:
        return defaultPrefix

prefixFileName = "prefixes.json"
cogsDir = "cogs"
defaultPrefix = '!'
botColor = 0xafff00
CSEid = "49fac5d937f302021"

load_dotenv()
discordToken = os.getenv("DISCORD_TOKEN")
steamToken = os.getenv("STEAM_WEB_API_KEY")
mongoConnectionURL = os.getenv("MONGO_CLUSTER")
googleToken = os.getenv("GOOGLE_API_KEY")

cluster = motor.AsyncIOMotorClient(mongoConnectionURL)
absDir = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    print(absDir)