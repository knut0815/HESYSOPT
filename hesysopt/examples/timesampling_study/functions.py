# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def storage_energy_content(Tmax=90, Tmin=70, V=1000, rho=980, cp=4.182, k=3600):
    """
    param T_max : Maximum storage Temperature in celsius
    param T_min : Minimum storage temperature in celsius
    param V : volumen of storage content in m3
    param rho : density
    param cp: specfic heat capacity of storage content in kJ/kg C
    param k: factor to convert kJ -> kWh in kJ/kWh
    """
    U = V * rho * cp * (Tmax - Tmin) / k
    return(U)


def storage_investment_costs(V=1000, size='small'):
    coeff = investment_fit(size=size)
    I = coeff[0] * V**coeff[1] # * m
    return(I)

def investment_fit(spec_invest=None, size=None, plot=False):
    """
    Quelle: Oberhammer 2012, Fernwärmespeicher - Bauarten, Auslegung, Beispiele
            Präsentation Fernwärmetagung 2012
    """
    # m3
    # €/m3
    if size == 'large':
        spec_invest = np.array([[100,  250, 700, 15000, 50000],
                               [1250, 900, 543, 250, 100]])

    if size == 'small':
        spec_invest =  np.array([[35, 50,  100, 240, 260, 340,  380, 440, 590, 700],
                                 [2000, 1500, 1250, 1054, 988, 950, 873, 759, 696, 543]])


    def func(x, a, b):
        return (a * x**b)
    popt, pcov = curve_fit(func, spec_invest[0, :], spec_invest[1, :])

    if plot:
        plt.plot(spec_invest[0, :], spec_invest[1,:], 'ro',label="Original Data")
        plt.plot(range(0, max(spec_invest[0,:]), 10),
                 func(range(0, max(spec_invest[0,:]), 10), *popt))

    return(popt)

if __name__ == "__main__":

    U = storage_energy_content(Tmax=80, Tmin=50, V=390, cp=4.182, k=3600)
    print(str(U) +" kWh")

    volumen_discrete = np.arange(35, 1000, 100)
    U_discrete = [storage_energy_content(V=v)/1000 for v in volumen_discrete]
    c_spec_discrete = [storage_investment_costs(v) for v in volumen_discrete]

    volumen_cont =  np.arange(35, 1000, 1)
    U_cont = [storage_energy_content(V=v)/1000 for v in volumen_cont]
    c_spec_cont = [storage_investment_costs(v) for v in volumen_cont]
