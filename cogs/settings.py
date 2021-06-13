import discord
import json
from datetime import datetime
from discord.ext import commands
from configs import *


class SettingsCog(
    commands.Cog,
    name="Settings",
    description="Commands for changing settings of this bot in your server.",
):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        prefixes[str(guild.id)] = defaultPrefix
        json.dump(prefixes, open(prefixFile, "w"), indent=4)
        setup = await serverSettingsCollection.insert_one({
                "_id": guild.id,
                "name": guild.name,
                "disabled_commands": [],
                "blacklisted": []
            }
        )
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if setup.acknowledged:
            print(f"{now}: {guild.name} database was initiated.")
        else:
            print(f"{now}: Error: {guild.name} database cannot be initiated, but continue anyway.")
        introductionMessage = (
            f"Hello good people! I am **{self.bot.user.name}**\n"
            f"You can use my commands with `{defaultPrefix}` as a prefix.\n"
            f"For more info, send `{defaultPrefix}help`"
        )
        try:
            await guild.system_channel.send(introductionMessage)
        except:
            try:
                await guild.rules_channel.send(introductionMessage)
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        prefixes.pop(str(guild.id))
        json.dump(prefixes, open(prefixFile, "w"), indent=4)
        deleted = await serverSettingsCollection.delete_one({"_id": guild.id})
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if deleted.acknowledged:
            print(f"{now}: {guild.name} database was deleted.")
        else:
            print(f"{now}: Error: {guild.name} database cannot be deleted, but continue anyway.")

    @commands.group(
        name="setting",
        aliases=["set"],
        help="See the settings section of this bot.",
        usage="<option>",
        description=(
            "`option:` The option you want to change\n"
            "Each option require different permission to use.\n\n⠀"
        ),
    )
    @commands.guild_only()
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command("help"), "setting")
            if ctx.subcommand_passed is not None:
                await ctx.send(f"`{ctx.subcommand_passed}` is not a valid option for `{ctx.prefix}{ctx.invoked_with}`")

    @setting.command(
        name="prefix",
        brief=":exclamation: prefix",
        help="Change prefix for calling this bot.",
        usage="<new_prefix>",
        description=(
            "`new_prefix:` new prefix to use in this server\n"
            "If the new prefix include *space*, please put it in quotation marks (*Example:* `\"pls \"`)\n\n"
            "(default prefix for this bot is `!`)\n"
            "**Require __administrator__ permission.**\n⠀"
        ),
    )
    @commands.has_guild_permissions(manage_messages=True, manage_channels=True)
    async def prefix(self, ctx, newPrefix=None):
        if newPrefix == None:
            await ctx.invoke(self.bot.get_command("help"), "prefix")
            await ctx.send(f"Current prefix for this server is `{ctx.prefix}`")
        else:
            async with ctx.typing():
                prefixes[str(ctx.guild.id)] = newPrefix
                json.dump(prefixes, open(prefixFile, "w"), indent=4)
            await ctx.send(f"Prefix for {self.bot.user.mention} in this server was changed to `{newPrefix}`")

    @setting.command(
        name="toggle",
        brief=":play_pause: toggle",
        help="Enable/Disable specific command.",
        usage="<target_command>",
        description=(
            "`target_command:` target command to turn on/off\n"
            "**Require __administrator__ permission.**\n⠀"
        ),
    )
    @commands.has_guild_permissions(administrator=True)
    async def toggle(self, ctx, targetcmd: str):
        if "setting" in targetcmd.lower() or "settings" in targetcmd.lower():
            await ctx.send(
                "How are you gonna turn **settings section** back on if you disable it?"
            )
            return

    @setting.command(
        name="blacklist",
        brief=":no_entry_sign: blacklist",
        help="Enable/Disable text channel for using this bot.",
        usage="<mention_channel>",
        description=(
            "`mention_channel:` target channel to blacklist/whitelist\n"
            "**Require __manage channels__ permission.**\n⠀"
        ),
    )
    @commands.has_guild_permissions(manage_channels=True)
    async def blacklist(self, ctx, mention_channels: commands.Greedy[discord.TextChannel] = False):
        if not mention_channels:
            await ctx.invoke(self.bot.get_command("help"), "blacklist")
            return
        thisGuildBlacklist = blacklistedTextChannel[ctx.guild.id]
        result = ''
        for channel in mention_channels:
            if channel.id not in thisGuildBlacklist:
                thisGuildBlacklist.append(channel.id)
                result += f"{channel.mention} was **added** to the blacklist.\n"
            else:
                thisGuildBlacklist.remove(channel.id)
                result += f"{channel.mention} was **removed** from the blacklist.\n"
        savedBlacklist = await serverSettingsCollection.update_one({"_id": ctx.guild.id}, {"$set":{"blacklisted": thisGuildBlacklist}})
        if savedBlacklist.matched_count != 0:
            await ctx.send(result)
        else:
            await ctx.send("Umm, uhhhh... I'm dumb.")

    @prefix.error
    @setting.error
    async def setting_error(cog, ctx, error):
        await ctx.send(f"{error}")


def setup(bot):
    bot.add_cog(SettingsCog(bot))