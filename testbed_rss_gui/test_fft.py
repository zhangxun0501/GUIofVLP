from signallib import *

filename = "data/-20x0.pos"
Fe = 3E6
fftsize = 2

R_PD = 1.9E4
I_620 = 0.4
D_PD = 3E-3

T = 10
T_begin = 5
T_end = 10
N1s = 100
F_begin = [4.9e5, 6.9e5, 8.9e5]
F_end = [5.1e5, 7.1e5, 9.1e5]

datas, llms, lm_mean = get_data_from_file(filename, T, T_begin, T_end, Fe, fftsize, N1s, F_begin, F_end, plotable=False)

print(lm_mean)
