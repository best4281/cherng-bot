import aiohttp
import asyncio
import json
from discord.ext import commands
from configs import *

discordAppID = {
    "poker"   : 755827207812677713,
    "fish"    : 814288819477020702,
    "YouTube" : 755600276941176913,
    "betrayal": 773336526917861400
}

async def fetch_invite(ctx, app):
    try:
        voice =  str(ctx.author.voice.channel.id)
    except Exception as e:
        await ctx.send("You are not in a valid voice channel.")
        print(e)
        return False

    body = json.dumps({"max_age":0, "target_type": 2, "target_application_id": discordAppID[app]})
    async with aiohttp.ClientSession() as client:
        async with client.request('POST', f'https://discord.com/api/v8/channels/{voice}/invites', headers = { 'authorization' : f'Bot {discordToken}', 'content-type': 'application/json' }, data = body) as response:
            if response.status != 200:
                await ctx.send(":robot: Beep Boop. Discord is not cooperating with me.\n`code:red`")
                return False
            try:
                resp = await response.json()
                code = resp["code"]
                if type(code) == str:
                    return code
                else:
                    await ctx.send(":robot: Beep Boop. Discord is not cooperating with me.\n`code:green`")
                    return False
            except:
                await ctx.send(":robot: Beep Boop. Discord is not cooperating with me.\n`code:blue`")
                return False


class SecretActivitiesCog(commands.Cog, command_attrs = { "hidden" : True}):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "poker")
    async def poker(self, ctx):
        invite = await fetch_invite(ctx, "poker")
        if not invite:
            return
        message = await ctx.send(f"https://discord.gg/{invite}")
        await message.pin()

    @commands.command(name = "fish")
    async def fish(self, ctx):
        invite = await fetch_invite(ctx, "fish")
        if not invite:
            return
        message = await ctx.send(f"https://discord.gg/{invite}")
        await message.pin()

    @commands.command(name = "yt")
    async def youtube(self, ctx):
        invite = await fetch_invite(ctx, "YouTube")
        if not invite:
            return
        message = await ctx.send(f"https://discord.gg/{invite}")
        await message.pin()

    @commands.command(name = "betrayal")
    async def betrayal(self, ctx):
        invite = await fetch_invite(ctx, "betrayal")
        if not invite:
            return
        message = await ctx.send(f"https://discord.gg/{invite}")
        await message.pin()

def setup(bot):
    bot.add_cog(SecretActivitiesCog(bot))
