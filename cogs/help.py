import math
import datetime
import discord
from discord.ext import commands
from configs import *

class helpCog(commands.Cog, name = "Help"):

    def __init__(self, bot):
        self.bot = bot
        self.maxLength = 4

    @commands.command(
        name = "help",
        aliases = ['h','commands', 'command'],
        help = "Help command that you are using now.",
        usage = "[page/category/command]",
        description = (
            "`page:` page number\n"
            "`category:` name of category\n"
            "`command:` command name\n\n"
            "When using without arguments, this will bring help up page 1 of help.\n⠀"
        )
    )
    async def help_command(self, ctx, *details):

        async with ctx.typing():

            prefix = get_prefix(ctx)
            detail = ' '.join(details)
            cogs = [c for c in self.bot.cogs.keys() if 'cog' not in c.lower()]
            totalPages = math.ceil(len(cogs) / self.maxLength)
            content = ''

            if not details:
                detail = "1"

            if detail.isdecimal():
                page = int(detail)

                if page > totalPages or page < 1:
                    await ctx.send(f"There is no page **{detail}**. There are only **{totalPages}** in the help section.")
                    return

                if totalPages > 1:
                    embedHelp = discord.Embed(
                        title = f"{self.bot.user.name} Commands listed by category:",
                        description = f"Use `{prefix}help [category/command]` for more detail\nUse `{prefix}help [page_number]` for going to another page\n⠀",
                        color = botColor["Spring Bud"],
                        timestamp = datetime.datetime.utcnow()
                        )
                else:
                    embedHelp = discord.Embed(
                        title = f"{self.bot.user.name} Commands listed by category:",
                        description = f"Use `{prefix}help [category/command]` for more detail\n⠀",
                        color = botColor["Spring Bud"],
                        timestamp = datetime.datetime.utcnow()
                        )
                embedHelp.set_thumbnail(url = self.bot.user.avatar_url)
                embedHelp.set_footer(text = f"Page {page} of {totalPages}")

                cogsInPage = []
                for i in range(self.maxLength):
                    index = i + (page - 1) * self.maxLength
                    try:
                        cogsInPage.append(cogs[index])
                    except:
                        pass

                for cog in cogsInPage:
                    currentCog = self.bot.get_cog(cog)
                    if not currentCog.description:
                        cogDetail = ''
                    else:
                        cogDetail = "__" + currentCog.description + "__\n"
                    for command in currentCog.walk_commands():
                        if command.hidden:
                            continue
                        elif command.parent != None:
                            continue
                        cogDetail += f"`{prefix}{command.name}`\t- {command.help}\n"
                    cogDetail += "⠀"
                    embedHelp.add_field(name = cog, value = cogDetail, inline = False)
            else:
                detaillow = detail.lower()
                checkCogs = [cog.lower() for cog in cogs]
                commands = {cmd.name:cmd for cmd in self.bot.commands if 'cog' not in cmd.cog_name.lower()}
                checkCommands = {}
                for cmd in commands.values():
                    checkCommands[cmd.name.lower()] = cmd.name
                    for alias in cmd.aliases:
                        checkCommands[alias] = cmd.name

                if detaillow in checkCommands:
                    command = commands[checkCommands[detaillow]]
                    embedHelp = discord.Embed(title = f"Command: {command.name}", description = command.help + "\n⠀", color = botColor["Lime Green"])
                    embedHelp.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
                    embedHelp.set_footer(text = "/ - Or , <> - Required & [] - Optional")
                    usage = command.usage if command.usage is not None else ""
                    alias = ', '.join(command.aliases)
                    embedHelp.add_field(name = "Format", value = f"`{prefix}{command.name} {usage}`\n⠀", inline = True)
                    embedHelp.add_field(name = "Aliases", value = f"`{alias}`\n⠀" if command.aliases else "No other aliases.\n⠀", inline = True)
                    embedHelp.add_field(name = "Description", value = command.description if command.description else "No description (yet).", inline = False)

                elif detaillow in checkCogs:
                    index = checkCogs.index(detaillow)
                    currentCog = self.bot.get_cog(cogs[index])
                    embedHelp = discord.Embed(title = f"Category: {cogs[index]}", description = currentCog.description + "\n⠀" , color = botColor["Yellow Green"])
                    embedHelp.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
                    embedHelp.set_footer(text = "/ - Or , <> - Required & [] - Optional")
                    for command in currentCog.walk_commands():
                        if command.hidden:
                            continue
                        elif command.parent != None:
                            continue
                        embedHelp.add_field(name = command.name, value = command.help, inline = False)
                        usage = command.usage if command.usage is not None else ""
                        alias = ', '.join(command.aliases)
                        embedHelp.add_field(name = "Format", value = f"`{prefix}{command.name} {usage}`\n⠀", inline = True)
                        embedHelp.add_field(name = "Aliases", value = f"`{alias}`\n⠀" if command.aliases else "No other aliases.\n⠀", inline = True)

                else:
                    content = f"There is no category or command with name **{detail}**."
                    embedHelp = None

        await ctx.send(content, embed = embedHelp)

def setup(bot):
    bot.add_cog(helpCog(bot))
