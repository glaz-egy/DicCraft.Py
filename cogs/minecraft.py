# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from discord.ext import commands
from subprocess import PIPE
import discord
import psutil
import mcrcon
import socket
import utils
import json

class Minecraft(commands.Cog):
    def __init__(self, bot, rconConf, botConf):
        self.bot = bot
        self.server = None
        self.rconConf = rconConf
        self.botConf = botConf
        self.sock = sokect.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    @commands.command()
    async def check(self, ctx, *args):
        try:
            self.sock.connect((self.rconConf.Addr, self.rconConf.Port))
        except:
            await ctx.send("サーバは起動していません")
        else:
            self.sock.close()
            await ctx.send("サーバは起動中です")
        
    @commands.command()
    async def boot(self, ctx):
        try:
            self.sock.connect((self.rconConf.Addr, self.rconConf.Port))
        except:
            self.server = psutil.Popen([self.botConf.serverdir], stdout=PIPE)
            await ctx.send("サーバを起動しました")
        else:
            self.sock.close()
            await ctx.send("サーバはすでに起動中です")
    
    @commands.command()
    async def shutdown(self, ctx):
        try:
            self.server.kill()
        except:
            await ctx.send("サーバが起動していないか、エラーが発生しました")
        else:
            await ctx.send("サーバを終了しました")
            self.sock.colse()
    
    @commands.command()
    async def userlist(self, ctx):
        try:
            self.sock.connect((self.rconConf.Addr, self.rconConf.Port))
            rcon = mcrcon.login(self.sock, self.rconConf.Pass)
        except:
            await ctx.send("サーバは起動していません")
        else:
            userlist = rcon.command(self.sock, "/list")
            await ctx.send(userlist)
            self.sock.close()