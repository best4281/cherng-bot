import discord
import json
from discord.ext import commands
from configs import *

prefixFile = "./" + prefixFileName

class OptionsCog(commands.Cog, name = "Settings", description = "Commands for changing settings of this bot in your server."):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open(prefixFile, 'r') as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = defaultPrefix
        with open(prefixFile, 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open(prefixFile, 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open(prefixFile, 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.command(
        name = "prefix",
        help = "Change prefix for calling this bot.",
        usage = "<new_prefix>",
        description = (
            "`new_prefix:` new prefix to use in this server\n\n"
            "(default prefix for this bot is `!`)\n⠀"
        )
    )
    @commands.guild_only()
    async def prefix(self, ctx, newPrefix = None):
        if newPrefix == None:
            prefix = get_prefix(ctx)
            await ctx.send(f"Current prefix for this server is `{prefix}`")
            await ctx.invoke(self.bot.get_command('help'), "prefix")
        else:
            async with ctx.typing():
                prefixes = json.load(open(prefixFile, 'r'))
                prefixes[str(ctx.guild.id)] = newPrefix
                json.dump(prefixes, open(prefixFile, 'w'), indent=4)
            await ctx.send(f"Prefix for this bot in **{ctx.guild.name}** was changed to `{newPrefix}`")

def setup(bot):
    bot.add_cog(OptionsCog(bot))
