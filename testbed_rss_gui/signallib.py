import scipy as sp
import matplotlib.pylab as plt
from matplotlib.ticker import FuncFormatter


def read_rss_received(filename):
	print("filename: {}".format(filename))
	f = sp.fromfile(open(filename), dtype=sp.float32)
	return f


def fft(data, Fe, L, plotable):
	Xf = sp.absolute(sp.fft(data, L))
	if plotable:
		f = Fe * sp.linspace(0, L/2, int(L/2))/L
		P1 = Xf[0:int(L/2)]
		P1[1:-2] = 2*P1[1:-2]
		plt.figure()
		plt.plot(f, P1)
	return Xf


def split_signal_by_N(N, L_Rss, number_of_interval=None):
	N = int(N)
	if number_of_interval is None:
		number_of_interval = int(L_Rss / N) + 1
	else:
		number_of_interval = int(number_of_interval + 1)
	return N, range(N, number_of_interval*N, N)


def split_signal_by_time(t, L_Rss, number_of_interval=None):
	N = int(t * L_Rss)
	if number_of_interval is None:
		number_of_interval = int(L_Rss / N) + 1
	else:
		number_of_interval = int(number_of_interval + 1)
	return N, range(N, number_of_interval*N, N)


def formatnum(x, pos):
    return "%e" % (x)


def get_data_from_file(filename, duree, T_begin, T_end, Fe, fftsize, N1s, F_begin, F_end, R_PD=1.9E4, I_620=0.4, D_PD=3E-3, plotable=False):
    Rss = read_rss_received(filename)
    L_Rss = len(Rss)
    Te = 1 / Fe
    if plotable:
        plt.figure()
        ts = sp.linspace(Te, duree, duree/Te)
        plt.plot(ts, Rss)

    N = int(Fe/N1s)
    T = T_end - T_begin

    n_begin = Fe / N * T_begin + 1
    n_end = Fe / N * T_end
    n = Fe / N * T

    x_axe = sp.linspace(T_begin+1/n*T, T_end, n)
    Ns = sp.linspace(N*n_begin, n_end*N, n)

    llms = sp.zeros((3, len(Ns)))

    for i in range(len(Ns)):
        rss = Rss[int(Ns[i]-N) : int(Ns[i])]

        L = len(rss)*fftsize

        R = fft(rss, Fe, L, False)

        Ayy = R/(L/2)
        Ayy[0] = Ayy[0] / 2

        Ayy_lightW = Ayy / R_PD
        Ayy_lightlm = Ayy_lightW*I_620*683
        if plotable:
            P2 = Ayy_lightlm[0:int(L/2)]
            f = Fe * sp.linspace(0, L/2, int(L/2))/L
            fig, ax = plt.subplots(1, 1)
            ax.plot(f, P2)
            formatter = FuncFormatter(formatnum)
            ax.yaxis.set_major_formatter(formatter)
        
        llm1 = Ayy_lightlm[int(F_begin[0]*L/Fe):int(F_end[0]*L/Fe)].max()
        llm2 = Ayy_lightlm[int(F_begin[1]*L/Fe):int(F_end[1]*L/Fe)].max()
        llm3 = Ayy_lightlm[int(F_begin[2]*L/Fe):int(F_end[2]*L/Fe)].max()

        llms[0, i] = llm1
        llms[1, i] = llm2
        llms[2, i] = llm3

    lm_1_mean = llms[0, :].mean()
    lm_2_mean = llms[1, :].mean()
    lm_3_mean = llms[2, :].mean()
    lm_mean = [lm_1_mean, lm_2_mean, lm_3_mean]

    return Rss, llms, lm_mean