# -*- coding: utf-8 -*-

from subprocess import Popen
import discord

def createEmbed(title, name, value, color):
    e = discord.Embed(title=title, colour=color)
    e.add_field(name=name, value=value)
    return e

def addEmbed(embed, name, value):
    embed.add_field(name=name, value=value)
    return embed

def bootServer(serverName, serverConfig):
    Popen("screen -AmdS {} java -XX:+AggressiveOpts -Xms{}G -Xmx{}G -jar {} {}"\
        .format(serverName, serverConfig[serverName]['serverfile'],\
        serverConfig[serverName]['minMemory'], serverConfig[serverName]['maxMemory'],\
        "nogui" if serverConfig[serverName]['isNoGUI'] else "")\
        , shell=True, cwd=serverConfig[serverName]['serverdir'])