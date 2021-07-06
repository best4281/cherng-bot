import io
import discord
import numpy as np
from PIL import Image, ImageDraw

async def insert_profile(profile, base, pos:list):
    if type(base) is str:
        image = Image.open(base)
    else:
        image = base
    image.alpha_composite(profile, (int(image.size[0] - pos[0]), int(image.size[1] - pos[1])))
    return image

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

async def get_round_profile(user, diam=320):
    avatarAsset = user.avatar
    avatarBuffer = io.BytesIO()
    await avatarAsset.save(avatarBuffer)
    avatarBuffer.seek(0)
    userAvatar = Image.open(avatarBuffer)
    userAvatar = userAvatar.resize((diam, diam))
    mask = Image.new('1', (diam, diam), color = 255)
    drawMask = ImageDraw.Draw(mask)
    drawMask.ellipse((0, 0, diam, diam), fill=0)
    userAvatar = Image.composite(Image.new("RGBA", (diam, diam), (255, 0, 0, 0)), userAvatar.convert("RGBA"), mask=mask)
    return userAvatar

async def make_discord_image(image:Image, filename, ext="png", spoiler=False):
    with io.BytesIO() as buffer:
        image.save(buffer, format=ext)
        buffer.seek(0)
        return discord.File(buffer, filename, spoiler=spoiler)