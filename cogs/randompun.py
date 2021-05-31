import random
import io
import discord
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from discord.ext import commands
from configs import *


async def insert_profile(profile, pos):
    image = Image.open("./pictures/pun_bonk.png")
    alphaChannelImage = ImageOps.expand(profile, border=(5,5,5,5), fill="black")
    profile.convert("RGBA")
    alphaChannelImage = profile.getchannel('A')
    image.paste(profile, (int(image.size[0] - pos[0]), int(image.size[1] - pos[1])), mask=alphaChannelImage)
    return image

async def make_profile_round(userAvatar):
    userAvatar = userAvatar.resize((320, 320))
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
    #print(np.array(vertexMatrix))
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
    print(new_grid[0][0])
    print(new_grid[1][1])
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

class randomCog(commands.Cog, command_attrs = { "hidden" : True}):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = "toodpun", aliases = ["toodpoon"], help = "Randomly send emoji of Pun.")
    @commands.guild_only()
    async def toodpun(self,ctx,num=1):

        #if ctx.guild.id == 729527231386353716:
        if ctx.guild.id != 359593138408521728:
            return

        async with ctx.typing():
            bonk = None
            emojis = ctx.guild.emojis
            pun = []
            selected = ''
            for emoji in emojis:
                if "Pun" in emoji.name:
                    pun.append(emoji)
            try:
                cnt = int(num)
            except:
                cnt = 1

            for i in range(cnt):
                choice = str(random.choice(pun))
                if len(selected + choice) >= 2000:
                    if ctx.author.id == 116019639053451265:
                        selected = "Wait what??? Did <@116019639053451265> just tried to bonk himself ?"
                        bonk = discord.file("./pictures/pun_bonk_himself.png")
                        break
                    avatarAsset = ctx.author.avatar_url_as(format='png', size=1024)
                    avatarBuffer = io.BytesIO()
                    await avatarAsset.save(avatarBuffer)
                    avatarBuffer.seek(0)
                    userAvatar = Image.open(avatarBuffer)
                    profileImg = await make_profile_round(userAvatar)
                    strength = random.random()
                    if strength > 0.8:
                        selected = f"{ctx.author.mention} You asked for {num} ToodPun, so he thinks you are too horny and hit you with a **very effective** bonk."
                    elif strength < 0.2:
                        selected = f"{ctx.author.mention} You asked for {num} ToodPun, so he thinks you are too horny but his bonk was *not very effective*."
                    else:
                        selected = f"{ctx.author.mention} You asked for {num} ToodPun, It's too many and he thinks you should go to horny jail."
                    profileImg, x_step, y_step = await warp_profile(profileImg, strength)
                    gotBonked = await insert_profile(profileImg, [232 + strength*strength*x_step, 253 + strength*strength*y_step])
                    buffer = io.BytesIO()
                    gotBonked.save(buffer, format='png')
                    buffer.seek(0)
                    bonk = discord.File(buffer, f"{ctx.author.name}_got_bonked.png")
                    break
                selected = selected + choice
        await ctx.send(selected, file = bonk)

def setup(bot):
    bot.add_cog(randomCog(bot))
