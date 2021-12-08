# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import StringVar, Entry, Label, Button, messagebox
import re


_NUMBER__REG = re.compile(r'^[+-]?\d+(\.\d+)?([eE][-+]?\d+)?$')
# _NUMBER__REG = re.compile(r'^-?\d+\.?\d*$')


def is_number(string):
    condition = _NUMBER__REG.search(string)
    if condition:
        return True
    return False


class TxSettingsFrame(Frame):

    __t1_settings_label: Label
    switch_label: Label
    position_label: Label
    m_label: Label
    pt_label: Label
    pr_label: Label

    x_input: Entry
    y_input: Entry
    z_input: Entry
    m_input: Entry
    pt_input: Entry
    pr_input: Entry

    switch: Checkbutton

    __status_text: StringVar
    __status: IntVar
    x: StringVar
    y: StringVar
    z: StringVar
    m: StringVar
    pt: StringVar
    pr: StringVar

    __comfirmer_button: Button

    def __init__(self, master, tx_model):
        super().__init__(master, bd=1, relief=GROOVE, padx=5, pady=5)
        self.__model = tx_model
        self.init_all()

    def status_change(self):
        if self.__model.get_status():
            self.__model.set_status(False)
            self.__status_text.set("OFF")
            self.__status.set(0)
            self.master.change_txs_map(self.__model.get_id(), False)
        else:
            self.__model.set_status(True)
            self.__status_text.set("ON")
            self.__status.set(1)
            self.master.change_txs_map(self.__model.get_id(), True)

    def save_change(self):
        if self.validate_input():
            self.__model.set_x(self.__convert_to_float(self.x.get()))
            self.__model.set_y(self.__convert_to_float(self.y.get()))
            self.__model.set_z(self.__convert_to_float(self.z.get()))
            self.__model.set_m(self.__convert_to_float(self.m.get()))
            self.__model.set_pt(self.__convert_to_float(self.pt.get()))
            self.__model.set_pr(self.__convert_to_float(self.pr.get()))

    def validate_input(self):
        if not is_number(self.x.get()):
            messagebox.showinfo("Warning!", "x input Error!")
            return False
        if not is_number(self.y.get()):
            messagebox.showinfo("Warning!", "y input Error!")
            return False
        if not is_number(self.z.get()):
            messagebox.showinfo("Warning!", "z input Error!")
            return False
        if not is_number(self.m.get()):
            messagebox.showinfo("Warning!", "m input Error!")
            return False
        if not is_number(self.pt.get()):
            messagebox.showinfo("Warning!", "Pt input Error!")
            return False
        if not is_number(self.pr.get()):
            messagebox.showinfo("Warning!", "Pr input Error!")
            return False
        return True

    def init_all(self):
        self.__t1_settings_label = Label(self, text="Settings for "+self.__model.get_name())
        self.__t1_settings_label.grid(row=1)

        self.__comfirmer_button = Button(
            self,
            text="Save data",
            command=self.save_change)
        self.__comfirmer_button .grid(row=2, padx=5, pady=5)

        self.__status_text = StringVar()
        self.__status = IntVar()
        if self.__model.get_status():
            self.__status_text.set("ON")
            self.__status.set(1)
        else:
            self.__status_text.set("OFF")
            self.__status.set(0)
        self.switch = Checkbutton(self,
                                  textvariable=self.__status_text,
                                  command=self.status_change,
                                  variable=self.__status)
        self.switch.grid(row=2, column=2, padx=5, pady=5)

        self.position_label = Label(self, text="X, Y, Z =(m)")
        self.position_label.grid(row=3, column=0, padx=5, pady=5)
        self.x = StringVar(self, str(self.__model.get_x()))
        self.x_input = Entry(self, textvariable=self.x, width=5)
        self.x_input.grid(row=3, column=1, padx=5, pady=5)
        self.y = StringVar(self, str(self.__model.get_y()))
        self.y_input = Entry(self, textvariable=self.y, width=5)
        self.y_input.grid(row=3, column=2, padx=5, pady=5)
        self.z = StringVar(self, str(self.__model.get_z()))
        self.z_input = Entry(self, textvariable=self.z, width=5)
        self.z_input.grid(row=3, column=3, padx=5, pady=5)

        self.m = StringVar(self, str(self.__model.get_m()))
        self.m_label = Label(self, text="Lambertain factor =")
        self.m_label.grid(row=4, column=1, padx=5, pady=5)
        self.m_input = Entry(self, textvariable=self.m, width=5)
        self.m_input.grid(row=4, column=2, padx=5, pady=5)

        self.pt = StringVar(self, str(self.__model.get_pt()))
        self.pt_label = Label(self, text="Pt   =")
        self.pt_label.grid(row=5, column=1, padx=5, pady=5)
        self.pt_input = Entry(self, textvariable=self.pt, width=5)
        self.pt_input.grid(row=5, column=2, padx=5, pady=5)

        self.pr = StringVar(self, str(self.__model.get_pr()))
        self.pr_label = Label(self, text="Pr   =")
        self.pr_label.grid(row=6, column=1, padx=5, pady=5)
        self.pr_input = Entry(self, textvariable=self.pr, width=20)
        self.pr_input.grid(row=6, column=2, padx=5, pady=5)

    def __convert_to_float(self, string):
        if string.find("e") != -1:
            data = string.split("e")
            res = float(data[0]) * 10 ** float(data[1])
        elif string.find("E") != -1:
            data = string.split("E")
            res = float(data[0]) * 10 ** float(data[1])
        else:
            res = float(string)
        print(res)
        return res
