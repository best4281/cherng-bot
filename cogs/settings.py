import discord
import json
from discord.ext import commands
from configs import *

prefixFile = "./" + prefixFileName

class SettingsCog(commands.Cog, name = "Settings", description = "Commands for changing settings of this bot in your server."):

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

    @commands.group(
        name = "setting",
        aliases = ["set"],
        help = "See the settings section of this bot.",
        usage = "<option>",
        description = (
            "`option:` The option you want to change\n"
            "Each option require different permission to use.\n\n⠀"
        )
    )
    @commands.guild_only()
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), "setting")

    @setting.command(
        name = "prefix",
        brief = ":exclamation: prefix",
        help = "Change prefix for calling this bot.",
        usage = "<new_prefix>",
        description = (
            "`new_prefix:` new prefix to use in this server\n"
            "(default prefix for this bot is `!`)\n"
            "**Require __administrator__ permission.**\n⠀"
        )
    )
    @commands.has_guild_permissions(manage_messages=True, manage_channels=True)
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
    
    @setting.command(
        name = "toggle",
        brief = ":play_pause: toggle",
        help = "Enable/Disable specific command.",
        usage = "<target_command>",
        description = (
            "`target_command:` target command to turn on/off\n"
            "**Require __administrator__ permission.**\n⠀"
        )
    )
    @commands.has_guild_permissions(administrator=True)
    async def toggle(self,ctx, targetcmd:str):
        if "setting" in targetcmd.lower() or "settings" in targetcmd.lower():
            await ctx.send("How are you gonna turn **settings section** back on if you disable it?")
            return
        
    @setting.command(
        name = "blacklist",
        brief = ":no_entry_sign: blacklist",
        help = "Enable/Disable text channel for using this bot.",
        usage = "<mention_channel>",
        description = (
            "`mention_channel:` target channel to blacklist/whitelist\n"
            "**Require __manage channels__ permission.**\n⠀"
        )
    )
    @commands.has_guild_permissions(manage_channels=True)
    async def blacklist(self,ctx, *mention_channel):
        pass

    #@prefix.error
    #@setting.error
    #async def prefix_error(cog, ctx, error):
    #    await ctx.send(f"**{cog}**: {error}")

def setup(bot):
    bot.add_cog(SettingsCog(bot))
