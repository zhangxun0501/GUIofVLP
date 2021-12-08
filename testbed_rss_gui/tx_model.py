# -*- coding: utf-8 -*-

class TxModel:

    def __init__(self,
                 number=0,
                 x=0,
                 y=0,
                 z=0,
                 status=True,
                 m=1.5,
                 pt=2000,
                 pr=0
                 ):
        self.__id = number
        self.__x = x
        self.__y = y
        self.__z = z
        self.__status = status
        self.__m = m
        self.__pt = pt
        self.__pr = pr
        self.__name = "T" + str(number+1)

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_z(self, z):
        self.__z = z

    def set_status(self, status):
        self.__status = status

    def set_m(self, m):
        self.__m = m

    def set_pt(self, pt):
        self.__pt = pt

    def set_pr(self, pr):
        self.__pr = pr

    def get_id(self):
        return self.__id

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_z(self):
        return self.__z

    def get_status(self):
        return self.__status

    def get_m(self):
        return self.__m

    def get_pt(self):
        return self.__pt

    def get_pr(self):
        return self.__pr

    def get_name(self):
        return self.__name
