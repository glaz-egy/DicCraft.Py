# -*- coding: utf-8 -*-

from discord.ext import commands
import configparser
import discord
import logging
import utils
import json
import cogs

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s]%(name)s: %(message)s'))
logger.addHandler(handler)

class MinecraftBot(commands.Bot):
    def __init__(self, config):
        super().__init__(command_prefix=config.prefix)
        self.botConf = config

    async def on_ready(self):
        print('bot booting')

    async def on_disconnect(self):
        print('disconnect')
        self.clear()
        self.run(self.botConf.bottoken)

with open('config.json') as f:
        j = json.load(f)

botConf = utils.botConfig(j['botconfig'])

bot = MinecraftBot(botConf)

if __name__ == '__main__':
    bot.add_cog(cogs.Minecraft(bot, botConf, j['servers']))
    #bot.add_cog(cogs.VPN(bot))
    bot.add_cog(cogs.Control(bot))
    #bot.add_cog(cogs.Music(bot, 'playlist.plf'))
    bot.run(botConf.bottoken)