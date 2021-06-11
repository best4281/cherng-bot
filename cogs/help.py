import asyncio
import math
import datetime
import discord
from discord.ext import commands
from configs import *

class HelpCog(commands.Cog, name = "Help"):

    def __init__(self, bot):
        self.bot = bot
        self.maxLength = 5

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
    @commands.max_concurrency(2, commands.BucketType.channel)
    async def help_command(self, ctx, *details):
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

            async with ctx.typing():
                if totalPages > 1:
                    embedHelp = discord.Embed(
                        title = f"{self.bot.user.name} Commands listed by category:",
                        description = (
                            f"Use `{prefix}help [category/command]` to get more detail\n"
                            f"Use `{prefix}help [page_number]` to go to specific page\n"
                            "Press :arrow_backward: below to navigate to previous page\n"
                            "Press :arrow_forward: below to navigate to next page\n"
                            "Press :x: below to delete this help message\n⠀"
                        ),
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
                
                helpPages=[]
                for currentPage in range(totalPages):
                    helpPage = embedHelp.copy()
                    cogsInPage = []
                    if currentPage == 0 and totalPages != 1:
                        helpPage.description = (
                            f"Use `{prefix}help [category/command]` to get more detail\n"
                            f"Use `{prefix}help [page_number]` to go to specific page\n"
                            "Press :arrow_forward: below to navigate to next page\n"
                            "Press :x: below to delete this help message\n⠀"
                        )
                    elif currentPage == totalPages - 1 and totalPages != 1:
                        helpPage.description = (
                            f"Use `{prefix}help [category/command]` to get more detail\n"
                            f"Use `{prefix}help [page_number]` to go to specific page\n"
                            "Press :arrow_backward: below to navigate to previous page\n"
                            "Press :x: below to delete this help message\n⠀"
                        )
                    for i in range(self.maxLength):
                        index = i + (currentPage) * self.maxLength
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
                            if command.parent == None:
                                cogDetail += f"`{prefix}{command.name}`\t- {command.help}\n"
                            
                        cogDetail += "⠀"
                        helpPage.add_field(name = cog, value = cogDetail, inline = False)
                    helpPage.set_footer(text = f"Page {currentPage + 1} of {totalPages}")
                    helpPages.append(helpPage)
                embedHelp = helpPages[page-1]
        else:
            async with ctx.typing():
                detaillow = detail.lower()
                checkCogs = [cog.lower() for cog in cogs]
                commands = {cmd.name:cmd for cmd in self.bot.walk_commands() if 'cog' not in cmd.cog_name.lower()}
                checkCommands = {}
                for cmd in commands.values():
                    checkCommands[cmd.name.lower()] = cmd.name
                    for alias in cmd.aliases:
                        checkCommands[alias] = cmd.name

                if detaillow in checkCommands:
                    command = commands[checkCommands[detaillow]]
                    parentCog = command.cog
                    parentCommands = command.full_parent_name
                    have_subcommands = False

                    if not parentCommands:
                        parentCommands = "Command"
                    embedHelp = discord.Embed(title = f"{parentCommands}: {command.name}", description = f"{command.help}\n⠀", color = botColor["Lime Green"])
                    embedHelp.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
                    embedHelp.set_footer(text = "/ - Or , <> - Required & [] - Optional")
                    usage = command.usage if command.usage is not None else ''
                    alias = ', '.join(command.aliases)
                    if parentCommands == "Command":
                        embedHelp.add_field(name = "Format", value = f"`{prefix}{command.name} {usage}`\n⠀", inline = True)
                    else:
                        embedHelp.add_field(name = "Format", value = f"`{prefix}{parentCommands} {command.name} {usage}`\n⠀", inline = True)
                    embedHelp.add_field(name = "Aliases", value = f"`{alias}`\n⠀" if command.aliases else "No other aliases.\n⠀", inline = True)
                    embedHelp.add_field(name = "Description", value = command.description if command.description else "No description (yet).", inline = False)
                    for cmd in parentCog.walk_commands():
                        if cmd.hidden:
                            continue
                        if cmd.parent == command:
                            desc = cmd.description if cmd.description else "No description (yet)."
                            usage = cmd.usage if cmd.usage is not None else ''
                            if not have_subcommands:
                                have_subcommands = True
                                embedHelp.add_field(name = f":gear: Options for **`{prefix}{command.name}`**", value = f"**{command.name}** is a group of commands, an option is required to execute this command.", inline = False)
                            embedHelp.add_field(name = f"**{cmd.brief}**", value = f"`{prefix}{command.name} {cmd.name} {usage}`\n{cmd.help}", inline = True)
                            #embedHelp.add_field(name = "Format", value = f"`{prefix}{command.name} {cmd.name} {usage}`\n{desc}", inline = True)
                            

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
        
        if "page" not in locals() or totalPages == 1:
            await ctx.send(content, embed = embedHelp)
        else:
            helpMessage = await ctx.send(content, embed = embedHelp)
            if page == 1:
                await helpMessage.add_reaction("\N{Cross Mark}")
                await helpMessage.add_reaction("\N{Black Right-Pointing Triangle}")
            elif page == totalPages:
                await helpMessage.add_reaction("\N{Cross Mark}")
                await helpMessage.add_reaction("\N{Black Left-Pointing Triangle}")
            else:
                await helpMessage.add_reaction("\N{Cross Mark}")
                await helpMessage.add_reaction("\N{Black Left-Pointing Triangle}")
                await helpMessage.add_reaction("\N{Black Right-Pointing Triangle}")
            react_check = lambda reaction,user: helpMessage.id == reaction.message.id and user != self.bot.user

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=react_check)

                    if reaction.emoji == "\N{Black Right-Pointing Triangle}":
                        page += 1
                        await helpMessage.edit(embed=helpPages[page-1])
                    elif reaction.emoji == "\N{Black Left-Pointing Triangle}":
                        page -= 1
                        await helpMessage.edit(embed=helpPages[page-1])
                    elif reaction.emoji == "\N{Cross Mark}":
                        await helpMessage.delete()
                        break
                    else:
                        await helpMessage.remove_reaction(reaction.emoji, user)
                    
                    if page == 1:
                        await helpMessage.clear_reaction("\N{Black Left-Pointing Triangle}")
                        await helpMessage.add_reaction("\N{Black Right-Pointing Triangle}")
                    elif page == totalPages:
                        await helpMessage.clear_reaction("\N{Black Right-Pointing Triangle}")
                        await helpMessage.add_reaction("\N{Black Left-Pointing Triangle}")
                    else:
                        if reaction.emoji == "\N{Black Right-Pointing Triangle}" and page == 2:
                            try:
                                await helpMessage.clear_reaction("\N{Black Right-Pointing Triangle}")
                                await helpMessage.add_reaction("\N{Black Left-Pointing Triangle}")
                                await helpMessage.add_reaction("\N{Black Right-Pointing Triangle}")
                            except Exception as e:
                                print(e)
                        else:
                            await helpMessage.remove_reaction(reaction.emoji, user)
                            await helpMessage.add_reaction("\N{Black Right-Pointing Triangle}")
                except asyncio.exceptions.TimeoutError:
                    try:
                        await helpMessage.clear_reactions()
                    except Exception as e:
                        print(e)
                    break
                except Exception as e:
                    print(e)
            timeoutEmbed = helpMessage.embeds[0]
            timeoutEmbed.description = f"Use `{prefix}help [category/command]` to get more detail\nUse `{prefix}help [page_number]` to go to specific page\n⠀"
            await helpMessage.edit(embed=timeoutEmbed)
    
    @help_command.error
    async def help_error(cog, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send("Only **two** interactive help command is allowed per channel at the same time. You can still use the old one.\nYou can also delete the existing one or wait until reactions on the existing one are removed *(20 seconds)*.")

def setup(bot):
    bot.add_cog(HelpCog(bot))
