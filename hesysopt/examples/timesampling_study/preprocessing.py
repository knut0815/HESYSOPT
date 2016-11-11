# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import functions as func


# Costs:
# https://www.ffe.de/download/wissen/349_Flexibilisierung_KWK/Schmid_FfE_KWK-Infotag.pdf
#
# m3
# €/m3
#spec_invest =  np.array([[590, 700,  250, 15000, 35000, 50000],
#                         [696, 543,  900, 250, 129, 100]])

#sizes = [100, 150, 200, 240, 300, 360, 450]

spec_invest =  np.array([[35, 50,  100, 240, 340, 440, 590, 700],
                         [2000, 1500, 1250, 1054, 873, 759, 696, 543]])

df = pd.DataFrame(spec_invest).transpose()
df.columns = ['volume_m3', 'costs_m3']
df = df.sort_values(['volume_m3'])

# calculate storage content
df['U_kWh'] = df.apply(lambda row:
                            func.storage_volume2energy(V=row['volume_m3'],
                                                       Tmax=95, Tmin=60),
                            axis=1)
df['U_MWh'] = df['U_kWh'] / 1e3
df['costs'] = df['volume_m3'] * df['costs_m3']

# plot
if False:
    df.plot(x=['U_MWh'], y=['costs_m3'])

# calculate equivalent (annual) investment costs
n = 20
wacc = 0.07
df['eq_annual_costs'] = df['costs'] * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)
#df['specific_ep_costs'] = df['specific_costs'] * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)
# import this into the app as basepoints for the optimization
basepoints = [(0,0)]
basepoints.extend([(np.floor(df['U_MWh'].loc[i]), df['eq_annual_costs'].loc[i])
                  for i in df.index])

if False:
    func.investment_fit(spec_invest=spec_invest, plot=True)

