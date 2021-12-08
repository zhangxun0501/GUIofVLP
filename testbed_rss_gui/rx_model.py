# -*- coding: utf-8 -*-
from numpy import matrix
from math import pi


class RxModel:
    def __init__(self, rx, ry, z, apd, txs, algo):
        self.rx = rx
        self.ry = ry
        self.x = None
        self.y = None
        self.z = z
        self.apd = apd * 10**-4
        self.txs = txs
        self.prs = list()
        self.txs = list()
        self.init_data_txs(txs)
        self.calculer_result(algo)
        self.d_error = self.get_delta_d()

    def init_data_txs(self, txs):
        for it in txs:
            if it.get_status():
                self.prs.append(it.get_pr())
                self.txs.append(it)

    def calculer_result(self, algo):
        if algo == 0:
            self.reordre()
            self.ds = self.get_ds()
            a = self.get_a()
            b = self.get_b(self.ds)
            xe = (a.T * a)
            xe = xe.I * a.T * b
            self.x = float(xe[0])
            self.y = float(xe[1])

    def reordre(self):
        res_txs = list()
        res_prs = list()
        txs_temp = self.txs[:]
        prs_temp = self.prs[:]
        for it in range(len(self.prs)):
            temp_max = max(prs_temp)
            max_index = prs_temp.index(temp_max)
            res_txs.append(txs_temp[max_index])
            res_prs.append(prs_temp[max_index])
            prs_temp.remove(prs_temp[max_index])
            txs_temp.pop(max_index)
        self.prs = res_prs
        self.txs = res_txs

    def get_txs(self):
        return self.txs

    def get_ds(self):
        ds = list()
        for i in range(len(self.txs)):
            h = self.txs[i].get_z() - self.z
            x = ((self.txs[i].get_m() + 1) * self.apd * pow(h, self.txs[i].get_m() + 1)
                 ) / (2 * pi) * (self.txs[i].get_pt() / self.txs[i].get_pr())
            d = pow(x, (1.0 / (self.txs[i].get_m() + 3)))
            ds.append(d)
        return ds

    def get_a(self):
        a = list()
        for i in range(1, 3):
            delta_x = self.txs[i].get_x() - self.txs[0].get_x()
            delta_y = self.txs[i].get_y() - self.txs[0].get_y()
            temp = [delta_x, delta_y]
            a.append(temp)
        matrix_a = matrix(a)
        return matrix_a

    def get_b(self, ds):
        b = list()
        for i in range(1, 3):
            temp = list()
            valeur = (ds[0] ** 2 - ds[i] ** 2 + self.txs[i].get_x() ** 2 + self.txs[i].get_y()
                      ** 2 - self.txs[0].get_x() ** 2 - self.txs[0].get_y() ** 2) / 2
            temp.append(valeur)
            b.append(temp)
        matrix_b = matrix(b)
        return matrix_b

    def get_delta_d(self):
        res = ""
        for it in range(len(self.ds)):
            delta_x = self.txs[it].get_x() - self.x
            delta_z = self.txs[it].get_z() - self.z
            de = pow((delta_x**2 + delta_z**2), 1.0/2)
            delta_d = self.ds[it] - de
            print(" * ", end="\t")
            name = "delta d" + str(it+1)
            res += "%s = %.3fm; estimated: %.3fm; real: %.3fm\n" % (name, delta_d, de, self.ds[it])
        return res
