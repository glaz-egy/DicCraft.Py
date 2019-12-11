# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from utils.async_mcrcon import MinecraftClient
from discord.ext import commands
from subprocess import PIPE, Popen, run
from utils import *
import discord
import psutil
import socket
import utils
import time

def checkAdmin(id, botConf):
    return (id == botConf.botadmin)

async def ServerConnect(rconConf, cmd, check=False):
    try:
        async with MinecraftClient(rconConf[0], rconConf[1] ,rconConf[2]) as ser:
            if not check:
                res = await ser.send(cmd)
            else:
                pass
        return (True if check else res)
    except:
        return False

class Minecraft(commands.Cog):
    def __init__(self, bot, botConf, servers):
        self.bot = bot
        self.servers = servers
        self.botConf = botConf
    
    @commands.command()
    async def check(self, ctx, *args):
        """マイクラサーバの状況を取得します"""
        if args is ():
            s = ''
            for l in self.servers.values():
                if not await ServerConnect(l['rconconfig'], None, check=True): s += '{}: not running\n'.format(l['servername'])
                else: s += '{}: running\n'.format(l['servername'])
            await ctx.send(embed=CreateEmbed('Runnig List', 'server', s, 0x2f4fa5))
        elif args[0] in list(self.servers.keys()):
            if not await ServerConnect(self.servers[args[0]]['rconconfig'], None, check=True):
                await ctx.send("{}は起動していません".format(self.servers[args[0]]['servername']))
            else:
                await ctx.send("{}は起動中です".format(self.servers[args[0]]['servername']))
        else:
            await ctx.send('__**{}**__ is not exit.'.format(args[0]))

    @commands.command()
    async def boot(self, ctx, *args):
        """マイクラサーバを起動します"""
        if args is ():
            await ctx.send("引数が必要になります")
        elif args[0] in list(self.servers.keys()):
            if not await ServerConnect(self.servers[args[0]]['rconconfig'], None, check=True):
                Popen("screen -AmdS {} java -XX:+AggressiveOpts -Xmx6G -Xms6G -jar {}".format(args[0], self.servers[args[0]]['serverfile']), shell=True, cwd=self.servers[args[0]]['serverdir'])
                time.sleep(1)
                await ctx.send("{}を起動しました".format(self.servers[args[0]]['servername']))
            else:
                await ctx.send("{}はすでに起動中です".format(self.servers[args[0]]['servername']))
        else:
            await ctx.send('__**{}**__ is not exit.'.format(args[0]))
    
    @commands.command()
    async def shutdown(self, ctx, *args):
        """マイクラサーバを終了します（BOT管理者専用）"""
        if args is ():
            await ctx.send("引数が必要になります")
        elif args[0] in list(self.servers.keys()):
            if checkAdmin(ctx.author.id, self.botConf):
                if not await ServerConnect(self.servers[args[0]]['rconconfig'], None, check=True):
                    await ctx.send("{}が起動していないか、エラーが発生しました".format(self.servers[args[0]]['servername']))
                else:
                    await ServerConnect(self.servers[args[0]]['rconconfig'], 'stop')
                    await ctx.send("{}を終了しました".format(self.servers[args[0]]['servername']))
            else:
                await ctx.send("適正ユーザではありません")
        else:
            await ctx.send('__**{}**__ is not exit.'.format(args[0]))
    
    @commands.command()
    async def reboot(self, ctx, *args):
        """マイクラサーバを再起動します（BOT管理者専用）"""
        if args is ():
            await ctx.send("引数が必要になります")
        elif args[0] in list(self.servers.keys()):
            if checkAdmin(ctx.author.id, self.botConf):
                if not await ServerConnect(self.servers[args[0]]['rconconfig'], None, check=True):
                    await ctx.send("{}が起動していないか、エラーが発生しました".format(self.servers[args[0]]['servername']))
                else:
                    await ServerConnect(self.servers[args[0]]['rconconfig'], 'stop')
                    print('reboot shutdown process end')
                    time.sleep(5)
                    Popen("screen -AmdS {} java -XX:+AggressiveOpts -Xmx6G -Xms6G -jar {}".format(args[0], self.servers[args[0]]['serverfile']), shell=True, cwd=self.servers[args[0]]['serverdir'])
                    time.sleep(1)
                    await ctx.send("サーバを再起動しました")
                    print('reboot boot process end')
            else:
                await ctx.send("適正ユーザではありません")
        else:
            await ctx.send('__**{}**__ is not exit.'.format(args[0]))
    
    @commands.command()
    async def userlist(self, ctx, *args):
        """現在マイクラサーバにログインしている人の一覧を表示します"""
        if args is ():
            embed = discord.Embed(title='User List', colour=0x09e08d)
            for x in self.servers.values():
                s = ''
                if not await ServerConnect(x['rconconfig'], None, check=True): s = 'Not running'
                else:
                    userlist = await ServerConnect(x['rconconfig'], 'list')
                    users = userlist.split(':')[1]
                    if not users == ' ':
                        users = [x.strip() for x in  users.split(',')]
                        s = ''
                        for u in users:
                            s += u+'\n'
                    else: s = 'None'
                embed = addEmbed(embed, x['servername'], s)
            await ctx.send(embed=embed)
        elif args[0] in list(self.servers.keys()):
            s = ''
            if not await ServerConnect(self.servers[args[0]]['rconconfig'], None, check=True): s = 'Not running'
            else:
                userlist = await ServerConnect(self.servers[args[0]]['rconconfig'], 'list')
                users = userlist.split(':')[1]
                if not users == ' ':
                    users = [x.strip() for x in  users.split(',')]
                    for u in users:
                        s += u+'\n'
                else: s = 'None'
            await ctx.send(embed=CreateEmbed('User List', self.servers[args[0]]['servername'], s, 0xffffff))
        else:
            await ctx.send('__**{}**__ is not exit.'.format(args[0]))
    
    @commands.command()
    async def cmd(self, ctx, *args):
        """マイクラサーバのコマンドを実行します（BOT管理者専用）"""
        if args is ():
            await ctx.send("引数が必要になります")
        elif args[0] in list(self.servers.keys()):
            if checkAdmin(ctx.author.id, self.botConf):
                if not await ServerConnect(self.servers[args[0]]['rconconfig'], None, check=True):
                    await ctx.send("{}は起動していません".format(self.servers[args[0]]['servername']))
                else:
                    cmd = await ServerConnect(self.servers[args[0]]['rconconfig'], ' '.join(args[1:]))
                    await ctx.send(cmd)
            else:
                await ctx.send("適正ユーザではありません")
        else:
            await ctx.send('__**{}**__ is not exit.'.format(args[0]))
    
    @commands.command()
    async def serverlist(self, ctx):
        ss = ''
        for s in self.servers.keys():
            ss += s+'\n'
        await ctx.send(embed=CreateEmbed('Server List', 'list', ss, 0x202910))
