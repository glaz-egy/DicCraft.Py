# -*- coding: utf-8 -*-

import configparser

class botConfig:
    def __init__(self, conf):
        self.conf = conf
        self.__bottoken = self.conf['token']
        self.__botadmin = self.conf['botadmin']
        self.__prefix = self.conf['prefix']

    @property
    def bottoken(self):
        return self.__bottoken

    @property
    def prefix(self):
        return self.__prefix
    
    @property
    def botadmin(self):
        return self.__botadmin