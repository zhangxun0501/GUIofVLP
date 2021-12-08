# -*- coding: utf-8 -*-
#
# @Time    : 16/10/2018 14:54

# @FileName: rss_utils.py
#

from time import time
from random import randint
import numpy as np


def get_random_color():
    colorArr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = "#"
    for i in range(6):
        color += colorArr[randint(0, 15)]
    return color


class RxModel:

    def __init__(self, z, apd, real_x=None, real_y=None, time_stamp=None, ue_id=0):
        self.__REAL_X = real_x
        self.__REAL_Y = real_y
        self.__Z = z
        self.__APD = apd
        self.__UE_ID = ue_id
        self.__TIME_STAMP = time() if time_stamp == None else time_stamp

    def set_real_x(self, x):
        self.__REAL_X = x

    def set_real_y(self, y):
        self.__REAL_Y = y

    def set_real_z(self, z):
        self.__Z = z

    def set_effective_area(self, apd):
        self.__APD = apd

    def get_real_x(self):
        return self.__REAL_X

    def get_real_y(self):
        return self.__REAL_Y

    def get_effective_area(self):
        return self.__APD

    def get_real_z(self):
        return self.__Z


class TxModel:

    def __init__(self, x, y, z, m=None, pt=None, ue_id=0, rrlh_id=0, time_stamp=None):
        self.__X = x
        self.__Y = y
        self.__Z = z
        self.__M = m
        self.__PT = pt
        self.__UE_ID = ue_id
        self.__RRLH_ID = rrlh_id
        self.__TIME_STAMP = time() if time_stamp == None else time_stamp

    def set_x(self, x):
        self.__X = x

    def set_y(self, y):
        self.__Y = y

    def set_z(self, z):
        self.__Z = z

    def set_lambertain_factor(self, m):
        self.__M = m

    def set_transmitted_power(self, pt):
        self.PT = pt

    def get_x(self):
        return self.__X

    def get_y(self):
        return self.__Y

    def get_z(self):
        return self.__Z

    def get_lambertain_factor(self):
        return self.__M

    def get_transmitted_power(self):
        return self.__PT

    def get_position(self):
        return self.__X, self.__Y, self.__Z

    def get_time_stamp(self):
        return self.__TIME_STAMP

    def get_ue_id(self):
        return self.__UE_ID

    def get_rrlh_id(self):
        return self.__RRLH_ID


class Room:

    def __init__(self, lx, ly, lz, size):
        self.lx = lx
        self.ly = ly
        self.lz = lz
        self.x = np.linspace(0, self.lx, size)
        self.y = np.linspace(0, self.ly, size)
        self.wall1 = [np.ones((1, size) * 0), self.y]
        self.wall2 = [self.x, np.ones((1, size) * 0)]
        self.wall3 = [np.ones((1, size) * self.lx), self.y]
        self.wall4 = [self.x, np.ones((1, size) * self.y)]
        self.origin = None




