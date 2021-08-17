import math
import datetime
import discord
from discord.ext import commands
from configs import *

class InteractiveHelpButton(discord.ui.Button):

    def __init__(self, action:int, **kwargs):
        self.action = action
        super().__init__(**kwargs)
    
    async def callback(self, interaction:discord.Interaction):
        assert self.view is not None
        helpMenu:InteractiveHelp = self.view
        if self.action == 0:
            helpMenu.delete = True
            helpMenu.stop()
            return
        else:
            helpMenu.current_page += self.action
            if helpMenu.current_page == 1 and self.action == -1:
                self.disabled = True
                helpMenu.children[2].disabled = False
            elif helpMenu.current_page == len(helpMenu.help_pages) and self.action == 1:
                self.disabled = True
                helpMenu.children[0].disabled = False
            else:
                helpMenu.children[0].disabled = False
                helpMenu.children[2].disabled = False
        await interaction.response.edit_message(embed=helpMenu.help_pages[helpMenu.current_page-1], view=helpMenu)


class InteractiveHelp(discord.ui.View):

    def __init__(self, current_page, pages, timeout = 20.0):
        super().__init__(timeout=timeout)
        self.current_page = current_page
        self.help_pages = pages
        self.delete = False
        self.add_item(InteractiveHelpButton(-1, emoji="◀️" , disabled=True if current_page == 1 else False))
        self.add_item(InteractiveHelpButton(0, style=discord.ButtonStyle.danger, label="close"))
        self.add_item(InteractiveHelpButton(1, emoji="▶️" , disabled=True if self.current_page == len(self.help_pages) else False))
    
    async def on_timeout(self):
        self.stop()

class NewHelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.maxLength = 2
    
    @commands.command(
        name = "newhelp",
        aliases = ['nh','ncommands', 'ncommand'],
        help = "New help command that you are using now.",
        usage = "[page/category/command]",
        description = (
            "`page:` page number\n"
            "`category:` name of category\n"
            "`command:` command name\n\n"
            "When using without arguments, this will bring help up page 1 of help.\n⠀"
        )
    )
    @commands.max_concurrency(2, commands.BucketType.channel)
    async def new_help_command(self, ctx, *details):
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
                embedHelp = discord.Embed(
                    title = f"Commands listed by category:",
                    description = (
                        f"Use `{prefix}help [category/command]` to get more detail\n"
                        f"Use `{prefix}help [page_number]` to go to specific page\n"
                    ),
                    color = botColor["Spring Bud"],
                    timestamp = datetime.utcnow()
                )
                embedHelp.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar)
                
                helpPages=[]
                for currentPage in range(totalPages):
                    helpPage = embedHelp.copy()
                    cogsInPage = []
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
                            if command.parent is None:
                                cogDetail += f"`{prefix}{command.name}`\t- {command.help}\n"
                            
                        cogDetail += "⠀"
                        helpPage.add_field(name = cog, value = cogDetail, inline = False)
                    helpPage.set_footer(text = f"Page {currentPage + 1} of {totalPages}")
                    helpPages.append(helpPage)
                embedHelp = helpPages[page-1]
            if totalPages == 1:
                await ctx.send(embed=embedHelp)
            else:
                navigation = InteractiveHelp(page, helpPages)
                helpMessage = await ctx.send(embed=embedHelp, view=navigation)
                await navigation.wait()
                if navigation.delete:
                    await helpMessage.delete()
                    return
                else:
                    await helpMessage.edit(view=None)
                    return
        
        else:
            await ctx.send("bruh")
    
    @new_help_command.error
    async def new_help_error(cog, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send("Only **two** interactive help command is allowed per channel at the same time. You can still use the old one.\nYou can also delete the existing one or wait until reactions on the existing one are removed *(20 seconds)*.")
        else:
            print(error)

def setup(bot):
    bot.add_cog(NewHelpCog(bot))
