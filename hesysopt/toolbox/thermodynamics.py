# -*- coding: utf-8 -*-

def storage_energy_content(Tmax=90, Tmin=70, V=1000, rho=980, cp=4.182, k=3600):
    """ Function calculates average storage energy content

    Parameters
    ----------
    T_max : float
        Maximum storage Temperature
    T_min : float
        Minimum storage temperature
    V : float
        Volumen of storage content in m^3
    rho : float
        Density
    cp: float
        Specfic heat capacity of storage content in kJ/kg C
    k: float
        Factor to convert kJ -> kWh in kJ/kWh
    """
    U = V * rho * cp * (Tmax - Tmin) / k

    return U