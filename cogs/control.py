# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from discord.ext import commands
import sys

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def exit(self, ctx, *args):
        await self.bot.close()
        await sys.exit()