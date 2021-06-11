import os
import json
import motor.motor_asyncio as motor
from dotenv import load_dotenv


def get_prefix(ctx):
    try:
        return prefixes[str(ctx.guild.id)]
    except:
        return defaultPrefix


botColor = {
    "Spring Bud": 0xAFFF00,
    "Yellow Green": 0x95C728,
    "Lime Green": 0x4CC936,
    "Sky Blue": 0x1BE7FF,
    "Orange": 0xF08700,
}

prefixFile = "./prefixes.json"
prefixes = json.load(open(prefixFile, "r"))
cogsDir = "cogs"
defaultPrefix = "!"
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