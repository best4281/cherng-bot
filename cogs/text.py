import discord
from discord.ext import commands
from configs import *

async def get_user_from_mention(ctx, filtered_args:tuple = None) -> list:
    userList = []
    for arg in filtered_args:
        try:
            arg = int(arg.strip('<@!>'))
            try:
                userList.append(await ctx.guild.fetch_member(arg))
            except:
                pass
        except:
            pass
    return userList

class textCommandsCog(commands.Cog, name = "Text", description = "Commands for managing text channel."):

    def __init__(self, bot):
        self.bot = bot

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

        prefix = get_prefix(ctx)

        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send(f"{ctx.author.mention} You does not have permission to manage messages in {ctx.channel.mention}.\nThis command cannot be used.")
            return

        if not ctx.message.mentions and '-i' in args or '--ignore' in args:
            check_func = lambda x: True
        elif ctx.message.mentions  and ctx.guild and '-i' in args or '--ignore' in args:
            tagged = await get_user_from_mention(ctx, args)
            check_func = lambda x: x.author in tagged
        elif ctx.message.mentions and ctx.guild:
            tagged = await get_user_from_mention(ctx, args)
            check_func = lambda x: x.author in tagged and not x.pinned
        else:
            check_func = lambda x: not x.pinned

        if num == None:
            await ctx.invoke(self.bot.get_command('help'), "clear")
            return
        if num == "all":
            async with ctx.typing():
                removedMessages = len(await ctx.channel.purge(limit = 1000, check = check_func))
            await ctx.send(f"**{removedMessages}** messages were removed from {ctx.channel.mention}", delete_after = 10)
            return
        try:
            async with ctx.typing():
                removedMessages = len(await ctx.channel.purge(limit = int(num), check = check_func))
            await ctx.send(f"**{removedMessages}** messages were removed from {ctx.channel.mention}", delete_after = 10)
        except:
            await ctx.invoke(self.bot.get_command('help'), "clear")
            await ctx.send("If you tried to use `clear` command without a number, it will __not__ work. Please always specify the number of messages to clear.")

def setup(bot):
    bot.add_cog(textCommandsCog(bot))
