# -*- coding: utf-8 -*-
#

# @FileName: database_q.py
#


import scipy as sp
import numpy as np
import os
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

"""
    A = [
            [[x1, y1], [x2, y1],...[xn, y1]],
            [[x1, y2], [x2, y2],...[xn, y2]],
            ...  ...   ...  ...   ...   ...,
            [[x1, yn], [x2, yn],...[xn, yn]]
    ]
        
    P1 = [
            [Pr(x1, y1), Pr(x2, y1),...Pr(xn, y1)],
            [Pr(x1, y2), Pr(x2, y2),...Pr(xn, y2)],
            ... ... ... ... ... ... ... ... ... ...,
            [Pr(x1, yn), Pr(x2, yn),...Pr(xn, yn)]
    ]
    
    P2 = ...
    ...
    PN = ...
    
    (xi, yi) => Pr_real
    qi = Pr_real / Pr(xi, yi)
    Q1 = [
            [q1, q2 .......,],
            [.....],
            ...
            [...qn]
    ]
    ...
    QN = ....
"""


def get_simulation_database(directory, txs):
    directory = "../generate_data/DATA/" + directory + "/"
    if not os.path.exists(directory):
        print("Directory \033[1;33m{}\033[0m doesn't exist!".format(directory))
        raise Exception
    datas = list()
    filenames = os.listdir(path=directory)
    for tx in txs:
        for file in filenames:
            filename = directory + file
            file = file[1:-5]
            positions = file.split(",")
            positions = [float(it) for it in positions]
            if tx.get_x() == positions[0] and tx.get_y() == positions[1]:
                tx_rss = list()
                with open(filename, 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for line in csv_reader:
                        line_rss = list()
                        for str_rss in line:
                            num_rss = float(str_rss)
                            line_rss.append(num_rss)
                        tx_rss.append(line_rss)
                datas.append(tx_rss)
    datas = np.array(datas)
    return datas


class Database_Q:
    def __init__(self, room_size=(5, 5, 3), test_shape = (10, 10), pt=2000, apd=1e-5, m=1.5):
        self.room_size = lx, ly, lz = room_size # (x, y, z) m
        self.test_shape = test_shape
        self.txs = None
        self.A = self.__get_matrix_A(lx, ly)
        self.leds_rss = None
        self.pt = pt
        self.m = m
        self.apd = apd
        self.real_rss = None
        self.Q = None

    def set_txs(self, txs):
        self.txs = txs
        self.real_rss = self.__get_real_rss()

    def generate_rss(self, directory, simulation=False):
        if not simulation:
            pass
        else:
            self.leds_rss = get_simulation_database(directory, self.txs)
        self.Q = self.__get_Q()

    def search_best_point(self, power_receive):
        self.Q_estimated = self.__compare_database(power_receive)
        return self.__minimum_defference_q()

    def __minimum_defference_q(self):
        min_point = float("inf")
        min_line = 0
        min_col = 0
        for line_index in range(self.test_shape[0]):
            for point_index in range(self.test_shape[1]):
                point_dif = 0
                for tx_index in range(len(self.txs)):
                    point_dif += abs(self.Q[tx_index][line_index][point_index] - self.Q_estimated[tx_index][line_index][point_index])
                if point_dif < min_point:
                    min_point = point_dif
                    min_line = line_index
                    min_col = point_index
        print("[{} {}]x = {}, y = {}, error = {}".format(min_line, min_col, self.A[min_line][min_col][0], self.A[min_line][min_col][1], min_point))
        return min_line, min_col

    def __compare_database(self, power_receive):
        datas = list()
        for tx_index in range(len(self.txs)):
            tx_q_estimated = list()
            for line in self.real_rss[tx_index]:
                line_estimated = list()
                for point in line:
                    q_estimated = point / power_receive[self.txs[tx_index]]
                    line_estimated.append(q_estimated)
                tx_q_estimated.append(line_estimated)
            datas.append(tx_q_estimated)
        return sp.array(datas)

    def __get_matrix_A(self, lx, ly):
        q_xs = sp.linspace(-lx/2, lx/2, self.test_shape[0])
        q_ys = sp.linspace(-ly/2, ly/2, self.test_shape[1])
        A = list()
        for q_y in q_ys:
            line = list()
            for q_x in q_xs:
                line.append((q_x, q_y))
            A.append(line)
        return sp.array(A)

    def __get_Q(self):
        datas = list()
        for tx_index in range(len(self.real_rss)):
            tx_q = list()
            for each_line in range(len(self.real_rss[tx_index])):
                line_q = list()
                for each_point in range(len(self.real_rss[tx_index][each_line])):
                    rss_real = self.real_rss[tx_index][each_line][each_point]
                    rss_received = self.leds_rss[tx_index][each_line][each_point]
                    q =  rss_real / rss_received
                    line_q.append(q)
                    ##if q > 1:
                        ##   print("Error! The real rss shold be biger than rss received")
                    ##   raise Exception
                tx_q.append(line_q)
            datas.append(tx_q)
        return np.array(datas)

    def __get_real_rss(self):
        datas = list()
        for tx in self.txs:
            tx_rss = list()
            for line in self.A:
                line_rss = list()
                for each_point in line:
                    x_1 = tx.get_x()
                    x_2 = each_point[0]
                    delta_x = x_1 - x_2
                    y_1 = tx.get_y()
                    y_2 = each_point[1]
                    delta_y = y_1 - y_2
                    h = self.room_size[2]
                    d_xy = sp.sqrt(((delta_x)**2 + (delta_y)**2))
                    d = sp.sqrt((d_xy**2 + h**2))
                    h_los = (self.apd * (self.m + 1)) / (2 * np.pi * sp.power(d, 2)) * sp.power((h / d), (self.m+1))
                    rss = h_los * self.pt
                    line_rss.append(rss)
                tx_rss.append(line_rss)
            datas.append(tx_rss)
        return sp.array(datas)


def plot_Q(Q, tx):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    X = sp.linspace(-2.5, 2.5, 10)
    Y = sp.linspace(-2.5, 2.5, 10)
    X, Y = sp.meshgrid(X, Y)
    Z = sp.array(Q)

    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    plt.title(str(tx.get_position()))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


def test_database(directory, pt=2000):
    from rss_model import TxModel
    from rss_model import RxModel
    M = 1.5
    PT = pt
    APD = 0.1 * 10 ** -4
    POSITIONS = [[1.5, 1.5, 3],
                 [1.5, -1.5, 3],
                 [-1.5, 1.5, 3],
                 [-1.5, -1.5, 3]
                 ]
    PRXS = {(0.30901699437494745, 0.9510565162951535, 0): [[0.00035507,
                                                            0.00013995,
                                                            0.00025289,
                                                            0.00011139]]}
    txs = list()
    for it in POSITIONS:
        x, y, z = it
        tx = TxModel(x, y ,z, M, PT)
        txs.append(tx)

    data_base_q = Database_Q(pt=pt)
    data_base_q.set_txs(txs)
    data_base_q.generate_rss(simulation=True, directory=directory)

    directory = "../generate_data/DATA/DATABASE_" + directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + "/Q_DATABASE.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        i = 0
        for it in data_base_q.Q:
            csv_writer.writerow("LED{}".format(i+1))
            for ii in it:
                csv_writer.writerow(ii)
            i+=1
    with open(directory + "/A_MATRIX.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        for it in data_base_q.A:
            csv_writer.writerow(it)
    with open(directory + "/real_pr.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        i = 0
        for it in data_base_q.real_rss:
            csv_writer.writerow("LED{}".format(i + 1))
            for ii in it:
                csv_writer.writerow(ii)
            i += 1

    for key in PRXS:
        for prs in PRXS[key]:
            power_receive = {txs[it]: prs[it] for it in range(len(txs))}
            print("*" * 20)
            print("Real location: {}".format(key))
            data_base_q.search_best_point(power_receive)

            filename = "/Q_DATABASE"+ str(key) +".csv"
            with open(directory + filename, "w") as csv_file:
                csv_writer = csv.writer(csv_file)
                i = 0
                for it in data_base_q.Q_estimated:
                    csv_writer.writerow("LED{}".format(i + 1))
                    for ii in it:
                        csv_writer.writerow(ii)
                    i += 1

    plot_Q(data_base_q.Q[0], txs[0])
    plot_Q(data_base_q.Q[1], txs[1])
    plot_Q(data_base_q.Q[2], txs[2])
    plot_Q(data_base_q.Q[3], txs[3])
    # plot_Q_estimated()


if __name__ == "__main__":
    test_database(directory="q_simulation_matlab_05_rho", pt=1000)
