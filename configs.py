import asyncio
import os
import json
import motor.motor_asyncio as motor
from dotenv import load_dotenv


def get_prefix(ctx):
    try:
        return prefixes[str(ctx.guild.id)]
    except:
        return defaultPrefix


load_dotenv()
discordToken = os.getenv("DISCORD_TOKEN")
steamToken = os.getenv("STEAM_WEB_API_KEY")
mongoConnectionURL = os.getenv("MONGO_CLUSTER")
googleToken = os.getenv("GOOGLE_API_KEY")

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

cluster = motor.AsyncIOMotorClient(mongoConnectionURL)
serverSettingsCollection = cluster["server"]["settings"]

async def make_blackList(col):
    blacklisted = col.find(projection={"_id": True, "blacklisted": True})
    blacklistedTextChannel = {}
    async for guild in blacklisted:
        blacklistedTextChannel[int(guild["_id"])] = [int(channel) for channel in guild["blacklisted"]]
    return blacklistedTextChannel

blacklistedTextChannel = asyncio.get_event_loop().run_until_complete(make_blackList(serverSettingsCollection))
print(blacklistedTextChannel)

absDir = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    print(absDir)
    