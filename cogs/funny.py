import asyncio
import random
import io
import discord
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from discord.ext import commands
from configs import *


async def insert_profile(profile, base, pos:list):
    alphaChannel = profile.getchannel('A')
    if type(base) is str:
        image = Image.open(base)
    else:
        image = base
    try:
        image.paste(profile, (int(image.size[0] - pos[0]), int(image.size[1] - pos[1])), mask=alphaChannel)
    except Exception as e:
        print(e)
    return image

async def make_profile_round(userAvatar):
    mask = Image.new('1', (320, 320), color = 0)
    drawMask = ImageDraw.Draw(mask)
    drawMask.ellipse((0, 0, 320, 320), fill=255)
    profileImg = userAvatar.copy()
    profileImg.putalpha(mask)
    return profileImg

async def griddify(size, x_cut, y_cut):
    width = size[0]
    length = size[1]
    x_step = width / float(x_cut)
    y_step = length / float(y_cut)
    y = 0.0
    vertexMatrix = []
    for i in range(x_cut + 1):
        vertexMatrix.append([])
        x = 0.0
        for j in range(y_cut + 1):
            vertexMatrix[-1].append([int(x), int(y)])
            x += x_step
        y += y_step
    return np.array(vertexMatrix), x_step, y_step

async def bonk_distort(grid, strength, x_step, y_step):
    new_grid = np.copy(grid)
    x_move = x_step * strength
    y_move = y_step * strength
    new_grid[0][0] = [int(new_grid[0][0][0] - x_move), int(new_grid[0][0][1] - y_move)]
    new_grid[0][1] = [int(new_grid[0][1][0] - 1.2*x_move), int(new_grid[0][1][1] - 1.2*y_move)]
    new_grid[1][0] = [int(new_grid[1][0][0] - 1.2*x_move), int(new_grid[1][0][1] - 1.2*y_move)]
    new_grid[1][1] = [int(new_grid[1][1][0] - x_move), int(new_grid[1][1][1] - y_move)]
    new_grid[0][2] = [int(new_grid[0][2][0] - 0.6*x_move), int(new_grid[0][2][1] - 0.6*y_move)]
    new_grid[2][0] = [int(new_grid[2][0][0] - 0.6*x_move), int(new_grid[2][0][1] - 0.6*y_move)]
    new_grid[2][1] = [int(new_grid[2][1][0] - 0.8*x_move), int(new_grid[2][1][1] - 0.8*y_move)]
    new_grid[1][2] = [int(new_grid[1][2][0] - 0.8*x_move), int(new_grid[1][2][1] - 0.8*y_move)]
    return new_grid

async def quad_as_rect(quad):
    if quad[0] != quad[2]: return False
    if quad[1] != quad[7]: return False
    if quad[4] != quad[6]: return False
    if quad[3] != quad[5]: return False
    return True

async def quad_to_rect(quad):
    assert(len(quad) == 8)
    assert(await quad_as_rect(quad))
    return (quad[0], quad[1], quad[4], quad[3])

async def grid_to_mesh(distorted_grid, start_grid):
    assert(distorted_grid.shape == start_grid.shape)
    mesh = []
    for i in range(distorted_grid.shape[0] - 1):
        for j in range(distorted_grid.shape[1] - 1):
            src_quad = [distorted_grid[i    , j    , 0], distorted_grid[i    , j    , 1],
                        distorted_grid[i + 1, j    , 0], distorted_grid[i + 1, j    , 1],
                        distorted_grid[i + 1, j + 1, 0], distorted_grid[i + 1, j + 1, 1],
                        distorted_grid[i    , j + 1, 0], distorted_grid[i    , j + 1, 1]]
            dst_quad = [start_grid[i    , j    , 0], start_grid[i    , j    , 1],
                        start_grid[i + 1, j    , 0], start_grid[i + 1, j    , 1],
                        start_grid[i + 1, j + 1, 0], start_grid[i + 1, j + 1, 1],
                        start_grid[i    , j + 1, 0], start_grid[i    , j + 1, 1]]
            dst_rect = await quad_to_rect(dst_quad)
            mesh.append([dst_rect, src_quad])
    return mesh

async def warp_profile(profile, strength):
    start_grid, x_step, y_step = await griddify(profile.size, 4, 4)
    distorted_grid = await bonk_distort(start_grid, strength, x_step, y_step)
    mesh = await grid_to_mesh(distorted_grid, start_grid)
    profile = profile.transform(profile.size, Image.MESH, mesh)
    return profile, x_step, y_step

async def get_profile_pic(user):
    avatarAsset = user.avatar_url_as(format='png', size=1024)
    avatarBuffer = io.BytesIO()
    await avatarAsset.save(avatarBuffer)
    avatarBuffer.seek(0)
    userAvatar = Image.open(avatarBuffer)
    userAvatar = userAvatar.resize((320, 320))
    userAvatar = await make_profile_round(userAvatar)
    return userAvatar
    
async def create_bonk(ctx, bonker, bonked, strength, **kwargs):
    if bonker != None:
        bonkerName = bonker.name
        bonkerImg = await get_profile_pic(bonker)
        bonkedImg = await get_profile_pic(bonked)
        bonkedImg, x_step, y_step = await warp_profile(bonkedImg, strength)
        gotBonked = await insert_profile(bonkedImg, "./pictures/blank_bonk.png", [227 + strength*x_step, 251 + strength*y_step])
        gotBonked = await insert_profile(bonkerImg.rotate(-30), gotBonked, [575, 531])
    else:
        bonkerName = "Pun"
        bonkedImg = await get_profile_pic(bonked)
        bonkedImg, x_step, y_step = await warp_profile(bonkedImg, strength)
        gotBonked = await insert_profile(bonkedImg, "./pictures/pun_bonk.png", [227 + strength*x_step, 251 + strength*y_step])
    bonkedBuffer = io.BytesIO()
    gotBonked.save(bonkedBuffer, format='png')
    bonkedBuffer.seek(0)
    return discord.File(bonkedBuffer, f"{bonked.name}_got_bonked_by_{bonkerName}.png", **kwargs)


class FunnyCog(commands.Cog, name = "Funny", description = "Commands just for fun"):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(
        name = "bonk",
        aliases = ["getbonk", "getbonked"],
        help = "Bonk the tagged person/people with random strength.",
        usage = "<@user(s)>",
        description = (
            "`@user(s):` mention user(s) to bonk more than one user (please don't bonk too many people at the same time)\n"
        )
    )
    @commands.guild_only()
    async def bonk(self, ctx, *args, **kwargs):
        
        if "strength" in kwargs:
            strength = kwargs["strength"]
        else:
            strength = random.random()
        
        if "target" in kwargs:
            target = kwargs["target"]
        else:
            target = set(ctx.message.mentions)
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
            if len(target) >= 10:
                await ctx.send("Don't try to make **{len(target)}** enemies at the same time, my computational power cannot process that many bonk.")
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
        
        async with ctx.typing():
            bonk = []
            for i,person in enumerate(target):
                if i >= 1:
                    strength = random.random()
                if "toodpun" in kwargs:
                    bonk.append(await create_bonk(ctx, None, ctx.author, strength))
                else:
                    bonk.append(await create_bonk(ctx, ctx.author, person, strength))
        #print(bonk)
        await ctx.send(message, files=bonk)
        return

def setup(bot):
    bot.add_cog(FunnyCog(bot))