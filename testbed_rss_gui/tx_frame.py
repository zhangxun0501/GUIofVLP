# -*- coding: utf-8 -*-

from tkinter import *
from tx_settings import TxSettingsFrame
from selection_frame import SelectionFrame


class TxFrame(Frame):

    __selection_frame: SelectionFrame

    def __init__(self, master, tx_list):
        super().__init__(master, bd=1, relief=GROOVE, padx=5, pady=5)
        self.__tx_list = tx_list
        self.__tx_settings_frame = list()
        self.__tx_actives = list()
        self.init_all()

    def init_all(self):
        self.__selection_frame = SelectionFrame(self, self.__tx_list)
        self.__selection_frame.pack(side="top")

        for it in range(9):
            active = 1 if it == 0 else 0
            self.__tx_actives.append(active)
            t_settings_frame = TxSettingsFrame(self, self.__tx_list[it])
            self.__tx_settings_frame.append(t_settings_frame)
        self.__tx_settings_frame[0].pack(side='bottom')

    def change_tx_setting(self, i, j):
        self.__tx_settings_frame[j].pack_forget()
        self.__tx_settings_frame[i].pack(side='bottom')

    def change_txs_map(self, piece, status):
        i = piece//3
        j = piece % 3
        color = "yellow" if status else "grey"
        tuple_get = self.__selection_frame.get_canvas()
        canvas = tuple_get[0]
        piece_width = tuple_get[1]
        piece_height = tuple_get[2]
        canvas.create_rectangle(j*piece_width,
                                i*piece_height,
                                (j+1)*piece_width,
                                (i+1)*piece_height,
                                fill=color)

    def get_active_list(self):
        return self.__tx_actives
