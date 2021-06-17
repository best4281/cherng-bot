import random
import io
import discord
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from discord.ext import commands
from configs import *


class RandomCog(commands.Cog, command_attrs = {"hidden" : True}):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = "toodpun", aliases = ["toodpoon"], help = "Randomly send emoji of Pun.")
    @commands.guild_only()
    async def toodpun(self,ctx,num=1):

        #if ctx.guild.id == 729527231386353716:
        if ctx.guild.id != 359593138408521728:
            return

        async with ctx.typing():
            emojis = ctx.guild.emojis
            pun = []
            selected = ''
            for emoji in emojis:
                if "Pun" in emoji.name:
                    pun.append(emoji)
            try:
                cnt = int(num)
            except:
                cnt = 1

            for i in range(cnt):
                choice = str(random.choice(pun))
                if len(selected + choice) >= 2000:
                    if ctx.author.id == 116019639053451265:
                        await ctx.send("Wait what??? Did <@116019639053451265> just tried to request too many emoji to bonk himself?", file = discord.File("./pictures/pun_bonk_himself.png"))
                        return
                    
                    strength = random.random()
                    if strength > 0.8:
                        selected = f"{ctx.author.mention} You asked for {num} ToodPun, so he thinks you are too horny and hit you with a **very effective** bonk."
                    elif strength < 0.2:
                        selected = f"{ctx.author.mention} You asked for {num} ToodPun, so he thinks you should go to horny jail but his bonk was *not very effective*."
                    else:
                        selected = f"{ctx.author.mention} You asked for {num} ToodPun, It's too many and he thinks you should go to horny jail."
                    await ctx.invoke(self.bot.get_command('bonk'), strength=strength, target={ctx.author}, message=selected, toodpun=True)
                    selected = None
                    break
                selected = selected + choice
        await ctx.send(selected)
    
    @toodpun.error
    async def randompun_error(cog, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            return
        await ctx.send(f"{error}")

def setup(bot):
    bot.add_cog(RandomCog(bot))