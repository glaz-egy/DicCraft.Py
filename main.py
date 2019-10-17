# -*- coding: utf-8 -*-

from discord.ext import commands
import configparser
import discord
import utils
import cogs

bot = commands.Bot(command_prefix=';')

if __name__ == '__main__':
    rconConf = utils.rconConfig('config.ini')
    botConf = utils.botConfig('config.ini')
    bot.add_cog(cogs.Minecraft(bot, ))
    bot.add_cog(cogs.Control(bot))
    bot.run('NjIyMDQ5NjIyOTIzNDExNTA2.XXuPGg.GYHm9a-4WNNeVw-uEOw3xYzMkK4')