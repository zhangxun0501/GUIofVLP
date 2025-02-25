# -*- coding: utf-8 -*-

from root import Root
from tx_model import TxModel
from rx_model import RxModel


def main():
    root = Root()
    root.mainloop()

def test_pr():
    t1 = TxModel(x=-0.5, y=0.25, z=2.195, pr=2.424162777141011e-06)
    t2 = TxModel(x=-0.5, y=0.6, z=2.195, pr=1.805735942220138e-06)
    t3 = TxModel(x=0.5, y=0.25, z=2.195, pr=8.324370247537219e-07)
    #t4 = TxModel(x=-1.5, y=-1.5, z=3, pr=0.4577E-3)
    txs = [t1, t2, t3]
    r = RxModel(-0.2, 0, 0.175, 7.0686e-2, txs, 0)
    print("Location : x =", r.x, ", y =", r.y)



if __name__ == "__main__":
    #test_pr()
    main()
