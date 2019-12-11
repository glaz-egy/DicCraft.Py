# -*- coding: utf-8 -*-

import discord

def CreateEmbed(title, name, value, color):
    e = discord.Embed(title=title, colour=color)
    e.add_field(name=name, value=value)
    return e

def addEmbed(embed, name, value):
    embed.add_field(name=name, value=value)
    return embed