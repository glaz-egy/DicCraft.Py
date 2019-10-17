# -*- coding: utf-8 -*-

import configparser

class botConfig:
    def __init__(self, configFile):
        self.__config = configparser.ConfigParser()
        self.__config.read(configFile)
        self.__serverdir = self.__config['bot']['serverdir']
        self.__bottoken = self.__config['bot']['token']

    @property
    def serverdir(self):
        return self.__serverdir
    
    @property
    def bottoken(self):
        return self.__bottoken
    