from discord.ext import commands
from configs import *

update_message = "New command: `bonk` was added to this bot. For more info, try it out or use `"
special_message = "Message from developer: *My midterm exam is also tomorrow, why am I doing this now...*\n*Please wish me luck*"

def get_prefix_from_guild(guild):
    with open(prefixFileName, 'r') as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(guild.id)]
    except:
        return defaultPrefix

class UpdateCog(commands.Cog, command_attrs = {"hidden" : True}):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = "sendupdate", aliases = [])
    async def send_update(self, ctx):
        if ctx.author.id != 283765324401344514:
            return
        for guild in self.bot.guilds:
            await guild.system_channel.send(f"{update_message}{get_prefix_from_guild(guild)}help bonk`\n{special_message}")
            #if guild.id == 359593138408521728:
            #    await guild.system_channel.send(special_message)

def setup(bot):
    bot.add_cog(UpdateCog(bot))
