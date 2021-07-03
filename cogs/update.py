from discord.ext import commands
from configs import *

update_message = "New command: `meme` is now available in this build of this bot. For more info, try it out or use `"
special_message = ""

def get_prefix_from_guild(guild):
    with open(prefixFile, 'r') as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(guild.id)]
    except:
        return defaultPrefix

class UpdateCog(commands.Cog, command_attrs = {"hidden" : True}):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = "sendupdate", aliases = [])
    @commands.is_owner()
    async def send_update(self, ctx):
        for guild in self.bot.guilds:
            await guild.system_channel.send(f"{update_message}{get_prefix_from_guild(guild)}help meme`\n{special_message}")

def setup(bot):
    bot.add_cog(UpdateCog(bot))
