from discord.ext import commands
from configs import *

update_message = "Beep boop, Now I will be available for 24 hours. Except for maintenance of course.\nBut it's so insecure right now, maybe even more than you at the moment."
special_message = "Toodpun/Toodpoon is also available here."

class updateCog(commands.Cog, command_attrs = {"hidden" : True}):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = "sendupdate", aliases = [])
    async def send_update(self, ctx):
        if ctx.author.id != 283765324401344514:
            return
        for guild in self.bot.guilds:
            await guild.system_channel.send(update_message)
            if guild.id == 359593138408521728:
                await guild.system_channel.send(special_message)

def setup(bot):
    bot.add_cog(updateCog(bot))
