import time
import re
import discord
import aiohttp
import motor.motor_asyncio as motor
from datetime import datetime
from discord.ext import commands
from googleapiclient.discovery import build
from steam import steamid
from configs import *

db = cluster["userData"]
steamCollection = db["steam"]
googleSearchService = build("customsearch", "v1", developerKey=googleToken)

async def user_search(appname:str, appid:int, members:list):
    dbquery = {
        "_id" : {"$in": members},
        "games.appid": appid
    }
    try:
        userData = steamCollection.find(dbquery , {"_id": True})
    except Exception as e:
        print(f"steamCog: {e}")
    ownedMembers = []
    try:
        async for member in userData:
            ownedMembers.append(member["_id"])
    except Exception as e:
        print(f"Steamcog: {e}")
    if not ownedMembers:
        return f"Sadly, nobody registered with me here has **{appname}** in their steam library.", None
    mentions = ' '.join(f"<@{user}>" for user in ownedMembers)
    embed = discord.Embed(title = f"Let's come together and play **{appname}**.", description = f"steam://run/{appid}", color = botColor["Sky Blue"])
    return mentions, embed

async def google_search(query, members, **kwargs):
    results = googleSearchService.cse().list(q=query, cx=CSEid, num=5, **kwargs).execute()
    if "items" not in results:
        return f"**{query}** does not match any app name or id on Steam, please try again with different keyword.", None
    items = results["items"]
    for item in items:
        if "videogame" in item["pagemap"]:
            appname = item["pagemap"]["videogame"][0]["name"]
            appid = item["pagemap"]["metatags"][0]["og:title"].partition("AppID: ")[2]
            if appid[-1] == '0':
                return await user_search(appname, int(appid), members)
        elif "product" in item["pagemap"]:
            appname = item["pagemap"]["product"][0]["name"]
            appid = re.search("/\d+", item["link"]).group().strip("/")
            if appid[-1] == '0':
                return await user_search(appname, int(appid), members)
    return f"**{query}** does not match any app name or id on Steam, please try again with different keyword.", None


class SteamInteractionCog(commands.Cog, name = "Steam", description = "Commands for interacting with Steam"):
    
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(
        name = "steamconnect",
        aliases = ["sc"],
        help = "Connect Steam Library data to Discord account",
        usage = "<steam_profile_link/disconnect/dc>",
        description = (
            "`steam_profile_link:` link to your steam profile (Steam library visibility must be set to public)\n"
            "`disconnect` or `dc:` unlink your linked steam profile\n"
            "(You have to connect it manually, since using bot to retrieve the connected Steam account is against Discord privacy policy)\n"
            "*By executing this commands and successfully connect your Steam account to this bot, you have fully agree to privacy policy of this bot (which we have none)*\n⠀"
        )
    )
    async def steam_connect(self, ctx, steamURL = None):
        if steamURL == None:
            await ctx.invoke(self.bot.get_command('help'), "steamconnect")
            return
        
        if steamURL.lower() in ["dc", "disconnect"]:
            deleted = await steamCollection.delete_one({"_id": ctx.author.id})
            if deleted.deleted_count == 0:
                await ctx.send(f"{ctx.author.mention} Your Steam Library data does not belong to us (yet). You can connect using `{get_prefix(ctx)}steamconnect <steam_profile_link>`.")
                print(f"steamCog: {ctx.author.name} file not found for deletion.")
                return
            await ctx.send(f"{ctx.author.mention} Your Steam Library data has been removed from this bot. To reconnect, use `{get_prefix(ctx)}steamconnect <steam_profile_link>`.")
            return
        
        async with ctx.typing():
            try:
                steamID = steamid.from_url(steamURL).as_64
            except Exception as e:
                print(e)
                await ctx.send(f"{ctx.author.mention} Your steam ID is irretrievable; the link may be invalid or Steam Web API might be down.")
                return
            if steamID == None:
                await ctx.send(f"{ctx.author.mention} Your steam ID is irretrievable; the link may be invalid or Steam Web API might be down.")
                return
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steamToken}&steamid={steamID}&include_played_free_games=1&format=json") as response:
                    if response.status != 200:
                        await ctx.send(f"Cannot retrieve game list from steam for {ctx.author.mention}. Is steam Web API down?")
                        return
                    ownedGames = await response.json()
                if type(ownedGames) is not dict:
                    await ctx.send(f"Cannot retrieve game list from steam for {ctx.author.mention}. Is steam Web API down?")
                    return
                if "response" not in ownedGames:
                    await ctx.send(f"Cannot retrieve game list from steam for {ctx.author.mention}. Is steam Web API down?")
                    return
                if "game_count" not in ownedGames["response"] or ownedGames["response"]["game_count"] <= 0:
                    await ctx.send(f"{ctx.author.mention} Steam library data is private, please change your privacy setting in Steam")
                    return
                
                ownedGames["_id"] = ctx.author.id
                ownedGames["steam_id"] = steamID
                ownedGames["game_count"] = ownedGames["response"].pop("game_count")
                ownedGames["games"] = []
                for game in ownedGames["response"]["games"]:
                    newInfo = {}
                    newInfo["appid"] = game["appid"]
                    newInfo["playtime_forever"] = game["playtime_forever"]
                    game.clear()
                    ownedGames["games"].append(newInfo)
                    del newInfo
                del(ownedGames["response"])

                async with session.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steamToken}&steamids={steamID}&format=json") as response:
                    if response.status != 200:
                        await ctx.send(f"{ctx.author.mention} Your Steam library was tied to your Discord account successfully.")
                        return
                    steamUser = await response.json()
        try:
            steamName = steamUser["response"]["players"][0]["personaname"]
        
        except:
            steamName = None
        
        ownedGames["steam_name"] = steamName
        saveData = await steamCollection.replace_one({"_id": ctx.author.id}, ownedGames, upsert=True, bypass_document_validation=True)
        if saveData.matched_count != 0:
            await ctx.send(f"{ctx.author.mention} Steam library from **{steamName}** was updated successfully.")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now}: {ctx.author.name} steam library was updated")
            return
        
        if steamName == None:
            await ctx.send(f"{ctx.author.mention} Steam library was tied to your Discord account successfully.")
            return
        await ctx.send(f"{ctx.author.mention} Steam library from **{steamName}** was tied to your Discord account successfully.")

    @commands.command(
        name = "tagbygame",
        aliases = ["tg","tag"],
        help = "Mention people with the game in their Steam library.",
        usage = "<search_keyword/appid>",
        description = (
            "`search_keyword:` keyword to search for game\n"
            "`appid:` application ID of application on steam\n\n"
            "This will only mention everyone who has connected Steam Library to this bot that has the game you searched for.\n⠀"
        )
    )
    @commands.guild_only()
    async def tag_steam(self, ctx, *args):
        prefix = get_prefix(ctx)
        if not args:
            await ctx.invoke(self.bot.get_command('help'), "tagbygame")
            return
        start_time = time.time()
        membersID = [member.id for member in ctx.channel.members if not member.bot]
        keyword = ' '.join(args)
        async with ctx.typing():
            content, embed = await google_search(keyword, membersID)
        await ctx.send(content, embed = embed)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now}: {ctx.author.name} search for {keyword}, and it took {time.time() - start_time} seconds to finish.")

def setup(bot):
    bot.add_cog(SteamInteractionCog(bot))
