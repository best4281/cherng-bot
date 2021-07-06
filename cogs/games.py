import random
import discord
from typing import List, Union
from discord.ext import commands
from configs import *

class TicTacToeButton(discord.ui.Button):

    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
    
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if interaction.user not in view.players:
            await interaction.response.send_message("This is not your TicTacToe match, go play something somewhere else.", tts=True, ephemeral=True)
            return
        
        if view.current_player == view.X and interaction.user.id == view.players[0].id:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"It is now {view.players[1].mention}'s (O) turn"
        elif view.current_player == view.O and interaction.user.id == view.players[1].id:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"It is now {view.players[0].mention}'s (X) turn"
        else:
            await interaction.response.send_message("It is not your turn yet, relax", tts=True, ephemeral=True)
            return
        
        winner = view.check_winner()
        if winner is not None:
            if winner == view.X:
                content = f"{view.players[0].mention} (X) won!"
            elif winner == view.O:
                content = f"{view.players[1].mention} (O) won!"
            else:
                content = "It's a tie!"
            for child in view.children:
                child.disabled = True
            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, p1:discord.Member, p2:discord.Member, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.players = [p1, p2]
        self.current_player = random.choice((self.X, self.O))
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x,y))
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
    
    def check_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X
        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X
        if all(i != 0 for row in self.board for i in row):
            return self.Tie
        return None


class GamesCog(commands.Cog, name="Games"):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="tictactoe", aliases=["xo", "ox"])
    @commands.max_concurrency(5, commands.BucketType.guild)
    async def tic_tac_toe(self, ctx:commands.Context, opponent:commands.Greedy[Union[discord.Member, discord.Role]]=None):
        if not opponent:
            await ctx.invoke(self.bot.get_command('help'), "tictactoe")
            return
        elif len(opponent) > 1:
            await ctx.send("You can only choose to play TicTacToe with one opponent at a time.")
            return
        else:
            if isinstance(opponent[0], discord.Role):
                if len(opponent[0].members) != 1:
                    await ctx.send("You can only choose to play TicTacToe with one opponent at a time.")
                    return
                else:
                    player2 = opponent[0].members[0]
            else:
                player2 = opponent[0]
        if player2.bot:
            await ctx.send("You can only choose to play TicTacToe with a real person (for now). I think you should try to interact with people more.")
            return
        if player2 is ctx.author:
            extra = "I think you are kinda lonely now, but enjoy a round of TicTacToe with yourself.\n"
        else:
            extra = ''
        game = TicTacToe(ctx.author, player2)
        first_move = ctx.author.mention if game.current_player == -1 else player2.mention
        first_sign = 'X' if game.current_player == -1 else 'O'
        game_message = await ctx.send(f"{extra}Tic Tac Toe: {first_move} ({first_sign}) goes first!", view=game)
        timeout = await game.wait()
        if timeout:
            for child in game.children:
                child.disabled = True
            abandoner = ctx.author.mention if game.current_player == -1 else player2.mention
            try:
                await game_message.edit(content=f"{abandoner} has abandoned the game. The game session was stopped to save bot resources.", view=game)
            except:
                pass
    
    @tic_tac_toe.error
    async def tic_tac_toe_error(cog, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send("Only **five** Tic Tac Toe session is allowed per guild at the same time. You can still use the old one.\nYou can also delete the existing one or wait until the existing one are timeout *(3 minutes)*.")
        else:
            print(error)


def setup(bot):
    bot.add_cog(GamesCog(bot))
