import asyncio
import typing
import random
import discord
from discord.ext import commands
from configs import *
from .utils import image as im
    
async def create_bonk(ctx, bonker, bonked, strength, spoiler=False):
    if bonker != None:
        bonkerName = bonker.name
        bonkerImg = await im.get_round_profile(bonker)
        bonkedImg = await im.get_round_profile(bonked)
        bonkedImg, x_step, y_step = await im.warp_profile(bonkedImg, strength)
        gotBonked = await im.insert_profile(bonkedImg, "./pictures/blank_bonk.png", [227 + strength*x_step, 251 + strength*y_step])
        gotBonked = await im.insert_profile(bonkerImg.rotate(-30), gotBonked, [575, 531])
    else:
        bonkerName = "Pun"
        bonkedImg = await im.get_round_profile(bonked)
        bonkedImg, x_step, y_step = await im.warp_profile(bonkedImg, strength)
        gotBonked = await im.insert_profile(bonkedImg, "./pictures/pun_bonk.png", [227 + strength*x_step, 251 + strength*y_step])
    return await im.make_discord_image(gotBonked, f"{bonked.name}_got_bonked_by_{bonkerName}.png", spoiler=spoiler)


class FunnyCog(commands.Cog, name = "Funny", description = "Commands just for fun"):

    def __init__(self,bot):
        self.bot = bot
        self.max_bonk = 8

    @commands.command(
        name = "bonk",
        aliases = ["getbonk", "getbonked"],
        help = "Bonk the tagged person/people with random strength.",
        usage = "<@user(s)> [reason]",
        description = (
            "`@user(s):` mention user(s) to bonk more than one user (please don't bonk too many people at the same time)\n"
            "`reason`: The reason why you bonk those people\n\n"
            "`@everyone` and `@here` is not allowed for this command, in order to prevent abusive usage."
        )
    )
    @commands.guild_only()
    async def bonk(self, ctx, tagged:commands.Greedy[typing.Union[discord.Member, discord.Role]]=None, *, reason=None, **kwargs):
        if ctx.message.mention_everyone:
            await ctx.send(f"Bonking `@everyone` and `@here` is not allowed, do not wake up everyone here with this stupid command.\nIf you want to tag everyone, please do it without using `{ctx.prefix}{ctx.invoked_with}`.", delete_after=10.0)
            await asyncio.sleep(3.0)
            await ctx.message.delete()
            return
        if "strength" in kwargs:
            strength = kwargs["strength"]
        else:
            strength = random.random()
        
        if "target" in kwargs:
            target = kwargs["target"]
        else:
            target = set()
            for tag in tagged:
                if isinstance(tag, discord.Role):
                    target.update(tag.members)
                else:
                    target.add(tag)
            if not target:
                await ctx.invoke(self.bot.get_command('help'), "bonk")
                return
        
        if self.bot.user in target:
                bonk = await create_bonk(ctx, self.bot.user, ctx.author, 0.99, spoiler=True)
                await ctx.send(f"{ctx.author.mention} Who do you think you are? Parry **this** you filthy casual!", file = bonk)
                return

        if ctx.author in target and "toodpun" not in kwargs:
                await ctx.send(f"{ctx.author.mention} No need to bonk yourself, trust me. You should not hurt yourself while hurting other people.")
                return

        if "message" not in kwargs:
            if len(target) >= self.max_bonk:
                await ctx.send(f"Don't try to make **{len(target)}** enemies at the same time, my computational power cannot process that many bonk.")
                return
            elif len(target) > 1:
                message = f"{ctx.author.mention} Trying to make **{len(target)}** enemies at the same time!? Daring today, aren't you?\nAnyway, here you go."
            elif strength > 0.8:
                message = f"{ctx.author.mention} hit {next(iter(target)).mention} with a **very effective** bonk!!"
            elif strength < 0.2:
                message = f"{ctx.author.mention} tried to bonk {next(iter(target)).mention}, but {next(iter(target)).mention} almost dodge it so your bonk was *not very effective*."
            else:
                message = f"{ctx.author.mention} bonked {next(iter(target)).mention}"
        else:
            message = kwargs["message"]
        
        if reason:
            message = f"Because {reason},\n{message}"

        async with ctx.typing():
            bonk = []
            for i,person in enumerate(target):
                if i >= 1:
                    strength = random.random()
                if "toodpun" in kwargs:
                    bonk.append(await create_bonk(ctx, None, ctx.author, strength))
                else:
                    bonk.append(await create_bonk(ctx, ctx.author, person, strength))

        await ctx.send(message, files=bonk)
        return


def setup(bot):
    bot.add_cog(FunnyCog(bot))