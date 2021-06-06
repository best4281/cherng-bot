import os
from discord.ext import commands
from configs import *

class DebugCog(commands.Cog, command_attrs = {"hidden" : True}):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = "reloadcog", aliases = ["rc"])
    async def reload_cog(self, ctx, cog:str, *args):
        if ctx.author.id != 283765324401344514:
            return
        if cog == "all":
            with ctx.typing():
                cnt = 0
                for extension in [f.replace('.py', '') for f in os.listdir(cogsDir) if os.path.isfile(os.path.join(cogsDir, f))]:
                    if "-i" in args or "--ignore" in args:
                        try:
                            self.bot.unload_extension(cogsDir + "." + extension)
                            print(f"{extension} was unloaded.")
                        except:
                            print(f"{extension} was ignored.")
                        try:
                            self.bot.load_extension(cogsDir + "." + extension)
                            print(f"{extension} was loaded.")
                            cnt += 1
                        except:
                            print(f"Failed to load extension {extension}.")
                    else:
                        try:
                            self.bot.reload_extension(cogsDir + "." + extension)
                            print(f"{extension} was reloaded.")
                            cnt += 1
                        except:
                            print(f"{extension} was ignored, or it was not loaded from the beginning.")
                print("--------------------")
            await ctx.send(f"**`SUCCESS:` {cnt}** cogs was reloaded")
            return
        try:
            self.bot.reload_extension("cogs." + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name = "unloadcog", aliases = ["uc"])
    async def unload_cog(self, ctx, cog:str):
        if ctx.author.id != 283765324401344514:
            return
        try:
            self.bot.unload_extension("cogs." + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name = "loadcog", aliases = ["lc"])
    async def load_cog(self, ctx, cog:str):
        if ctx.author.id != 283765324401344514:
            return
        try:
            self.bot.load_extension("cogs." + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

def setup(bot):
    bot.add_cog(DebugCog(bot))
