# -*- coding: utf-8 -*-
#
# @Time    : 03/07/2018 11:03

# @FileName: rss_model.py
#

from typing import List
from typing import Dict
from typing import Tuple
from numpy import matrix
from numpy import pi
import numpy as np
from database_q import Database_Q
from rss_utils import RxModel
from rss_utils import TxModel


class RSSModel:
    __rx: RxModel
    __txs: List[TxModel]
    __power_receive: Dict[TxModel, float]
    __estimated_x: float
    __estimated_y: float
    __estimated_distances: Dict[TxModel, float]
    __real_distances: Dict[TxModel, float]
    __distances_errors: Dict[TxModel, float]
    __positions_errors: Tuple[float, float, float]
    __algorithm: str

    def __init__(self, rx: RxModel, txs: List[TxModel], prs: List[float], q_test=True):
        self.__rx = rx
        self.__txs = txs
        self.__reset_attribute()
        self.__power_receive = {txs[it]: prs[it] for it in range(len(txs))}
        if q_test:
            self.__q_test()
        else:
            self.__best_Q_indice = None


    def run(self, debug=False):
        if self.__algorithm == "3":
            self.__run_3_max_tx_algo(debug)
        elif self.__algorithm == "ALL":
            self.__run_all_tx_algo(debug)
        pass # others options

    def set_algorithm(self, algo: str):
        self.__algorithm = algo

    def get_rx(self):
        return self.__rx

    def get_txs(self):
        return self.__txs

    def get_estimated_x(self):
        return self.__estimated_x

    def get_estimated_y(self):
        return self.__estimated_y

    def get_estimated_distances(self):
        return self.__estimated_distances

    def get_real_distances(self):
        return self.__real_distances

    def get_position_error(self):
        return self.__positions_errors

    def print_positions_error(self):
        print("\tError : {:.3f}".format(self.__positions_errors[2]))

    def print_estimated_position(self):
        print("\tLocation :(", self.__estimated_x, ",", self.__estimated_y, ",", self.__rx.get_real_z(), ")")

    def print_distances_errors(self, keys):
        print("\tDistance error: ")
        for tx in keys:
            print("\t\t", str(tx.get_position()), ":", self.__distances_errors[tx], " ( estimated distance:",
                  self.__estimated_distances[tx], "; real distance:", self.__real_distances[tx], ")")

    def print_real_location(self):
        if self.__rx.get_real_z() is not None:
            print("Real location (", self.__rx.get_real_x(), ",",
                  self.__rx.get_real_y(), ",", self.__rx.get_real_z(), "):")
        else:
            print("Real location (Unknown):")

    def __q_test(self):
        self.database_q = Database_Q()
        self.database_q.set_txs(self.__txs)
        self.database_q.generate_rss("q_simulation_matlab_05_rho" ,simulation=True)

        self.__best_Q_indice = self.database_q.search_best_point(self.__power_receive)

    def __reset_attribute(self, empty=True):
        self.__estimated_x = None
        self.__estimated_y = None
        self.__estimated_distances = None if empty else dict()
        self.__real_distances = None if empty else dict()
        self.__distances_errors = None if empty else dict()

    def __run_3_max_tx_algo(self, debug):
        if self.__best_Q_indice is not None:
            for tx_indice in range(len(self.__txs)):
                tx = self.__txs[tx_indice]
                best_q = self.database_q.Q[tx_indice][self.__best_Q_indice[0]][self.__best_Q_indice[1]]
                self.__power_receive[tx] = self.__power_receive[tx] * best_q
        self.__reset_attribute(False)
        keys = self.__sorting_power()
        self.__calculate_distances(keys)
        self.__calculate_position(keys, 3)
        self.__calculate_error(keys, 3)
        if debug:
            self.print_real_location()
            self.print_estimated_position()
            self.print_positions_error()
            self.print_distances_errors(keys)
            print("*"*79)

    def __run_all_tx_algo(self, debug):
        self.__reset_attribute(False)
        pass

    def __sorting_power(self):
        received_power_sorted = sorted(self.__power_receive.items(), key=lambda x: x[1], reverse=True)
        keys = list()
        for item in received_power_sorted:
            keys.append(item[0])

        return keys

    def __calculate_distances(self, keys):
        for tx in keys:
            # estimated distance
            h = tx.get_z() - self.__rx.get_real_z()
            m = tx.get_lambertain_factor()
            apd = self.__rx.get_effective_area()
            pt = tx.get_transmitted_power()
            pr = self.__power_receive[tx]
            x = (m + 1) * apd * h ** (m + 1) * pt / 2 / pi / pr
            d = pow(x, 1.0 / (m + 3))
            self.__estimated_distances[tx] = d

            # real distance
            if self.__rx.get_real_x() is not None and self.__rx.get_real_y() is not None:
                delta_x = tx.get_x() - self.__rx.get_real_x()
                delta_y = tx.get_y() - self.__rx.get_real_y()
                delta_z = tx.get_z() - self.__rx.get_real_z()
                d_xy = pow((delta_x ** 2 + delta_y ** 2), 1.0 / 2)
                d = pow((d_xy**2 + (delta_z**2)), 1.0/2)
                self.__real_distances[tx] = d

                # distance error
                self.__distances_errors[tx] = self.__estimated_distances[tx] - self.__real_distances[tx]
            else:
                self.__real_distances = None

    def __calculate_position(self, keys, tx_number):
        # Matrix A
        tmp = list()
        i = 0
        tx1 = None
        for tx in keys:
            if i == 0:
                tx1 = tx
                i += 1
                continue
            elif i == tx_number:
                break
            delta_x = tx.get_x() - tx1.get_x()
            delta_y = tx.get_y() - tx1.get_y()
            tmp.append([delta_x, delta_y])
            i += 1
        a = matrix(tmp)

        # Matrix B
        tmp = list()
        i = 0
        d1 = 0
        x1 = 0
        y1 = 0
        for tx in keys:
            if i == 0:
                d1: float = self.__estimated_distances[tx]
                x1: float = tx1.get_x()
                y1: float = tx1.get_y()
                i += 1
                continue
            elif i == tx_number:
                break
            d2 = self.__estimated_distances[tx]
            x2 = tx.get_x()
            y2 = tx.get_y()
            value = (d1 ** 2  - d2 ** 2 + x2 ** 2 + y2 ** 2 - x1 ** 2 - y1 ** 2) / 2.0
            tmp.append([value])
            i += 1
        b = matrix(tmp)

        xe = (a.T * a).I * a.T * b
        self.__estimated_x = float(xe[0])
        self.__estimated_y = float(xe[1])

    def __calculate_error(self, keys, tx_numbers):
        x = self.__rx.get_real_x() if self.__rx.get_real_x() is not None else None
        y = self.__rx.get_real_y() if self.__rx.get_real_y() is not None else None
        if x is not None and y is not None:
            delta_x = abs(self.__estimated_x - x)
            delta_y = abs(self.__estimated_y - y)
            error = np.sqrt(delta_x**2 + delta_y**2)
            self.__positions_errors = (delta_x, delta_y, error)
