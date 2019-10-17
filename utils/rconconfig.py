# -*- coding: utf-8 -*-

import configparser

class rconConfig:
    def __init__(self, configFile):
        self.__config = configparser.ConfigParser()
        self.__config.read(configFile)
        self.__Addr = self.__config['rcon']['addr']
        self.__Port = int(self.__config['rcon']['port'])
        self.__Pass = self.__config['rcon']['pass']

    @property
    def Addr(self):
        return self.__Addr
    
    @property
    def Port(self):
        return self.__Port
    
    @property
    def Pass(self):
        return self.__Pass
    