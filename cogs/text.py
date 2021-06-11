import asyncio.exceptions
import discord
from discord.ext import commands
from configs import *

async def confirm_clear(bot, ctx, msgCount:int, msgList:list):
    confirm = await ctx.send(f":bangbang: {ctx.author.mention} You are about to delete {msgCount} messages in {ctx.channel.mention}.\nSend **yes** to confirm. Send **no** to cancel.", delete_after=30.0)
    del_check = lambda message: message.author == ctx.author and message.content.lower() in ["yes", "no"]

    try:
        message = await bot.wait_for('message', timeout=20.0, check=del_check)
        if message.content.lower() == "no":
            await confirm.edit(content="Message deletion was aborted.")
            await message.delete()
            return
        await ctx.channel.delete_messages(msgList)
        await confirm.edit(content=f"**{msgCount}** messages were removed from {ctx.channel.mention}")
        await message.delete()
        return
    except asyncio.exceptions.TimeoutError:
        await confirm.edit(content="You did not gave me any confirmation in 20 seconds.")
        return

class TextCog(commands.Cog, name = "Text", description = "Commands for managing text channel."):

    def __init__(self, bot):
        self.bot = bot
        self.too_many_deletion = 50

    @commands.command(
        name = "clear",
        aliases = ["c", "cl", "clearchat"],
        help = "Remove messages in the text channel.",
        usage = "<number/all> [@user(s)] [-i]",
        description = (
            "`number:` number of the messages to be deleted, can be replaced with `all`\n"
            "`all:` is for removing maximum of 1000 messages at a time\n"
            "`@user(s):` mention a user to remove messages from this specific user\n"
            "`-i` or `--ignore` also delete the pinned messages\n\n"
            "**Require __manage message__ permission.**\n⠀"
        )
    )
    async def clear(self, ctx, num = None, *args):

        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send(f"{ctx.author.mention} You does not have permission to manage messages in {ctx.channel.mention}.\nThis command cannot be used.")
            return

        if not ctx.message.mentions and '-i' in args or '--ignore' in args:
            check_func = lambda x: True
        elif ctx.message.mentions  and ctx.guild and '-i' in args or '--ignore' in args:
            check_func = lambda x: x.author in ctx.message.mentions
        elif ctx.message.mentions and ctx.guild:
            check_func = lambda x: x.author in ctx.message.mentions and not x.pinned
        else:
            check_func = lambda x: not x.pinned

        if num == None:
            await ctx.invoke(self.bot.get_command('help'), "clear")
            return

        if num == "all":
            msgCount = 0
            msgList = []
            async with ctx.typing():
                async for msg in ctx.channel.history(limit=1000):
                    if check_func(msg):
                        msgCount += 1
                        msgList.append(msg)
            await confirm_clear(self.bot, ctx, msgCount, msgList)

        else:
            try:
                num = int(num)
            except:
                await ctx.invoke(self.bot.get_command('help'), "clear")
                await ctx.send(f"If you tried to use `clear` command without a number, it will __not__ work. Please always specify the number of messages to clear or use `{get_prefix(ctx)}clear all`.")
                return

            msgCount = -1
            msgList = []
            async with ctx.typing():
                async for msg in ctx.channel.history(limit=None):
                    if check_func(msg):
                        msgCount += 1
                        msgList.append(msg)
                    if msgCount == num:
                        break
            if msgCount >= self.too_many_deletion:
                await confirm_clear(self.bot, ctx, msgCount, msgList)
            else:
                await ctx.channel.delete_messages(msgList)
                await ctx.send(f"**{msgCount}** messages were removed from {ctx.channel.mention}", delete_after=10.0)

def setup(bot):
    bot.add_cog(TextCog(bot))