import asyncio
import datetime
import os
import json
import motor.motor_asyncio as motor


def get_prefix(ctx):
    try:
        return prefixes[str(ctx.guild.id)]
    except:
        return defaultPrefix


discordToken = os.environ["DISCORD_TOKEN"]
steamToken = os.environ["STEAM_WEB_API_KEY"]
mongoConnectionURL = os.environ["MONGO_CLUSTER"]
googleToken = os.environ["GOOGLE_API_KEY"]
redditClientID = os.environ["REDDIT_CLIENT_ID"]
redditClientSecret = os.environ["REDDIT_CLIENT_SECRET"]
redditScriptName = os.environ["REDDIT_SCRIPT_NAME"]

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
    guilds= col.find(projection={"_id": True, "blacklisted": True, "disabled_commands": True})
    blacklistedTextChannel = {}
    disabledCommandsDict = {}
    try:
        async for guild in guilds:
            blacklistedTextChannel[int(guild["_id"])] = [int(channel) for channel in guild["blacklisted"]]
            disabledCommandsDict[int(guild["_id"])] = [cmd for cmd in guild["disabled_commands"]]
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now}: configs.make_blacklist() {e}")
    return blacklistedTextChannel, disabledCommandsDict

blacklistedTextChannel, disabledCommandsDict = asyncio.get_event_loop().run_until_complete(make_blackList(serverSettingsCollection))

absDir = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    print(absDir)
    