import asyncio
import datetime
import typing
import random
import asyncpraw
import discord
from discord.ext import tasks, commands
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
        self.reddit = asyncpraw.Reddit(
            client_id=redditClientID,
            client_secret=redditClientSecret,
            user_agent=redditClientID,
        )
        self.max_submission = 300
        self.meme_list=[]
        self.fetch_meme.start()

    @tasks.loop(minutes=10.0)
    async def fetch_meme(self):
        subreddit_meme = await self.reddit.subreddit("memes+dankmemes+wholesomememes")
        async for submission in subreddit_meme.hot(limit=self.max_submission):
            if submission.stickied:
                continue
            if not submission.url.lower().endswith((".jpg", ".png", ".gif")):
                memeEmbed = None
                content = submission.url
                upvote = False
            else:
                memeEmbed = discord.Embed(
                    title=f"**{submission.title}**",
                    url=f"https://www.reddit.com{submission.permalink}",
                    timestamp = datetime.datetime.utcfromtimestamp(submission.created_utc),
                )
                memeEmbed.set_author(name=f"r/{submission.subreddit.display_name}", url=f"https://www.reddit.com/r/{submission.subreddit.display_name}")
                memeEmbed.set_footer(text=f"{submission.score}  |  💬   {submission.num_comments}", icon_url="attachment://upvote.png")
                memeEmbed.set_image(url=submission.url)
                content = None
                upvote = True
            if len(self.meme_list) >= self.max_submission:
                del self.meme_list[0]
            meme = {
                "embed": memeEmbed,
                "content": content,
                "upvote": upvote,
                "nsfw" : submission.over_18,
                "spoiler": submission.spoiler
            }
            self.meme_list.append(meme)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end=': ')
        print(f"Meme list updated.")

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
    
    @commands.command(
        name = "meme",
        aliases = ["redditmeme"],
        help = "Show random top new meme on reddit",
        usage="[help]",
        description = (
            "`help:` show the help of this command, but why tho??"
        )
    )
    @commands.cooldown(rate=10, per=30, type=commands.BucketType.user)
    @commands.guild_only()
    async def reddit_meme(self, ctx, h=None):
        try:
            if h.lower() == "help":
                await ctx.invoke(self.bot.get_command('help'), "meme")
                return
        except:
            pass
        memes = self.meme_list.copy()
        while memes:
            meme = random.choice(memes)
            if meme["nsfw"] and not ctx.channel.is_nsfw():
                memes.remove(meme)
                continue
            if meme["upvote"]:
                await ctx.send(content=meme["content"], embed=meme["embed"], file=discord.File("./pictures/upvote.png", filename="upvote.png"))
            else:
                await ctx.send(content=meme["content"], embed=meme["embed"])
            if meme["content"]:
                await ctx.send("I am working hard on delivering a video to you, but there are many difficulties on the Discord side. Only static images and .gif are available here for now.", delete_after=15.0)
            return
        if ctx.channel.is_nsfw():
            await ctx.send("There is no post that I can properly display right now, my maker can only offer you an apologize at the moment.", delete_after=15.0)
        else:
            await ctx.send("This channel is not a NSFW channel, I have filtered out all NSFW contents, and there are nothing left to display.", delete_after=15.0)
    
    '''@commands.command(
        name = "reddit",
        help = "Show random top post on specified subreddit(s)",
        usage = "<subreddit>",
    )
    @commands.guild_only()
    async def reddit(self, ctx, subreddit=None):
        if not subreddit:
            subreddit = await self.reddit.subreddit("all")
        else:
            subreddit = await self.reddit.subreddit(subreddit)
            try:
                await subreddit.load()
            except:
                await ctx.send("This subreddit does not exist, or reddit might be down.")
                return
            if subreddit.over18 and not ctx.channel.is_nsfw():
                await ctx.send("The specified subreddit(s) is NSFW. However, this channel is not marked as NSFW channel, so I cannot process your request.")
                return
        max_sub = 100
        memeEmbed = None
        async with ctx.typing():
            start = datetime.datetime.now()
            submissions = [submission async for submission in subreddit.hot(limit=max_sub) if not submission.stickied]
            print(f"Took: {datetime.datetime.now() - start} seconds to make list")
            cnt=0
            while submissions:
                print(f"{cnt=}")
                submission = random.choice(submissions)
                if not (submission.url.lower().endswith((".jpg", ".png", ".gif"))) or submission.url.startswith("https://v.redd.it/"):
                    print(f"{submission.url}")
                    submissions.remove(submission)
                    cnt += 1
                    continue
                if not(not(submission.over_18) or ctx.channel.is_nsfw()):
                    print(f"{submission.over_18}")
                    submissions.remove(submission)
                    cnt += 1
                    continue
                memeEmbed = discord.Embed(
                    title=f"**{submission.title}**",
                    url=f"https://www.reddit.com{submission.permalink}",
                    timestamp = datetime.datetime.utcfromtimestamp(submission.created_utc)
                )
                start = datetime.datetime.now()
                author = submission.author
                await author.load()
                print(f"Took: {datetime.datetime.now() - start} seconds to load author")
                print(f"{submission.url=}")
                memeEmbed.set_author(name=author.name, url=f"https://www.reddit.com/user/{author.name}", icon_url=author.icon_img)
                memeEmbed.set_image(url=submission.url)
                memeEmbed.set_footer(text=f"🔺 {submission.score} | 💬 {submission.num_comments}")
                break
        if memeEmbed:
            await ctx.send(embed=memeEmbed)
        else:
            await ctx.send("There is no post that I can properly display right now, my maker will make it display later when he want to.")'''
        
    @fetch_meme.error
    async def fetch_meme_error(*, error):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end=': ')
        print(f"Some error happened while fetching memes.")
    
    @reddit_meme.error
    async def reddit_meme_error(cog, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Scientist have found that requesting memes rapidly can cause headache to you and your friends. You need to calm down and try again in **{error.retry_after:.1f}** seconds.")
        else:
            print(error)

def setup(bot):
    bot.add_cog(FunnyCog(bot))