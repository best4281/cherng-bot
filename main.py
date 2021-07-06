import datetime
import os
import traceback
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
    if message.author.bot:
        return
    if not message.guild:
        await message.author.send("I was not made ready to serve you in private chat, maybe one day I will.")
        return
    if message.content.replace('!','',1) == bot.user.mention:
        guild_prefix = retrieve_prefix(bot, message)
        await message.reply(f"**Are you lost or something?**\nMy current prefix in this server is `{guild_prefix}`\nRemember it, or change it by using `{guild_prefix}setting prefix <new_prefix>`")
    await bot.process_commands(message)

@bot.check_once
async def check_commands(ctx):
    try:
        if ctx.channel.id in blacklistedTextChannel[ctx.guild.id] and f"{ctx.prefix}{ctx.invoked_with} blacklist" not in ctx.message.content:
            await ctx.send(f"This channel was blacklisted, you can remove this text channel from blacklist using **{ctx.prefix}setting blacklist {ctx.channel.mention}**", delete_after=15.0)
            return False
        elif ctx.command.name in disabledCommandsDict[ctx.guild.id]:
            await ctx.send(f"`{ctx.prefix}{ctx.invoked_with}` is currently disabled in this server, you can enable it using **{ctx.prefix}setting toggle {ctx.invoked_with}**", delete_after=15.0)
            return False
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now}: {e}, you dumb developer.")
    return True

@bot.event
async def on_command_error(ctx, error):
    errorType = type(error)
    if errorType in [commands.errors.CheckFailure, commands.errors.CommandOnCooldown, commands.errors.MaxConcurrencyReached, commands.errors.CommandNotFound]:
        return
    if errorType is commands.errors.MissingPermissions:
        missing = [perm.replace('_', ' ').replace("guild", "server").title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = ", ".join(missing[:-1])
            fmt += f", and {missing[-1]}"
        else:
            fmt =" and ".join(missing)
        if ctx.invoked_parents:
            invoked = ' '.join(ctx.invoked_parents)
            invoked += f" {ctx.invoked_with}"
        else:
            invoked = ctx.invoked_with
        await ctx.send(f"`{ctx.prefix}{invoked}` cannot be used, because you are missing **{fmt}** permission(s).", delete_after=15.0)
        return
    await ctx.send("Some error happened behind the scene. You know my developer is slacking of, so shits can happen from time to time.", delete_after=10.0)
    traceback.print_exception(errorType, error, error.__traceback__)
    return

if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in os.listdir(cogsDir) if os.path.isfile(os.path.join(cogsDir, f)) and not f.startswith('_')]:
        try:
            bot.load_extension("cogs." + extension)
            print(f"{extension} loaded.")
        except (discord.ClientException, ModuleNotFoundError):
            print(f"Failed to load extension {extension}.")

bot.run(discordToken)