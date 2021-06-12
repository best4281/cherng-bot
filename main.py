import os
import json
import asyncio
import logging
import discord
from discord.ext import commands
from configs import *

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()

def retrieve_prefix(bot, ctx):
    try:
        return prefixes[str(ctx.guild.id)]
    except:
        return defaultPrefix

activity = discord.Activity(type = discord.ActivityType.watching, name = "the world burn 🔥")
bot = commands.Bot(
    command_prefix = (retrieve_prefix),
    case_insensitive = True,
    intents = intents,
    activity = activity,
    help_command= None
)

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user.name} {bot.user.id}")
    for guild in bot.guilds:
        print(f"Belong to guild: {guild.name} {guild.id}")

@bot.event
async def on_message(message):
    if not message.guild:
        await message.author.send("I was not made ready to serve you in private chat, maybe one day I will.")
        return
    if message.content.replace('!','',1) == bot.user.mention:
        guild_prefix = retrieve_prefix(bot, message)
        await message.reply(f"**Are you lost or something?**\nMy current prefix in this server is `{guild_prefix}`\nRemember it, or change it by using `{guild_prefix}setting prefix <new_prefix>`")
    await bot.process_commands(message)

@bot.check_once
async def check_commands(ctx):
    if ctx.channel.id in blacklistedTextChannel[ctx.guild.id] and f"{ctx.prefix}{ctx.invoked_with} blacklist" not in ctx.message.content:
        await ctx.send(f"This channel was blacklisted, you can remove this text channel from blacklist using **{ctx.prefix}setting blacklist {ctx.channel.mention}**", delete_after=10.0)
        return False
    return True

if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in os.listdir(cogsDir) if os.path.isfile(os.path.join(cogsDir, f)) and not f.startswith('_')]:
        try:
            bot.load_extension("cogs." + extension)
            print(f"{extension} loaded.")
        except (discord.ClientException, ModuleNotFoundError):
            print(f"Failed to load extension {extension}.")

bot.run(discordToken)