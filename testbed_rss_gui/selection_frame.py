# -*- coding: utf-8 -*-
from tkinter import *


class SelectionFrame(Frame):

    __canvas_width = 150
    __canvas_height = 150

    def __init__(self, master, tx_list):
        super().__init__(master, bd=1, relief=GROOVE, padx=5, pady=5)
        self.__tx_list = tx_list
        self.__canvas = Canvas(self, width=self.__canvas_width, height=self.__canvas_height)
        self.__piece_width = self.__canvas_width/3
        self.__piece_height = self.__canvas_height/3
        self.draw()
        self.__canvas.pack(fill=BOTH)
        self.__canvas.bind("<Button-1>", self.click)

    def draw(self):
        it = 0
        for i in range(3):
            for j in range(3):
                color = "yellow" if self.__tx_list[it].get_status() else "grey"
                self.__canvas.create_rectangle(j*self.__piece_width,
                                               i*self.__piece_height,
                                               (j+1)*self.__piece_width,
                                               (i+1)*self.__piece_height,
                                               fill=color)
                it += 1

    def click(self, event):
        it = 0
        for i in range(3):
            for j in range(3):
                if (j*self.__piece_width <= event.x < (j+1)*self.__piece_width) \
                        and (i*self.__piece_height <= event.y < (i+1)*self.__piece_height):
                    ii = self.master.get_active_list().index(1)
                    self.master.get_active_list()[ii] = -1
                    self.master.get_active_list()[it] = 1
                    self.master.change_tx_setting(it, ii)
                it += 1

    def get_canvas(self):
        return self.__canvas, self.__piece_width, self.__piece_height
