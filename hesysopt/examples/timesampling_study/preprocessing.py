# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import functions as func


# Costs:
# https://www.ffe.de/download/wissen/349_Flexibilisierung_KWK/Schmid_FfE_KWK-Infotag.pdf
#
# m3
# €/m3
spec_invest =  np.array([[590, 700,  250, 15000, 35000, 50000],
                         [696, 543,  900, 250, 129, 100]])

df = pd.DataFrame(spec_invest).transpose()
df.columns = ['volume', 'specific_costs']
df = df.sort_values(['volume'])

# calculate storage content
df['U_kWh'] = df.apply(lambda row:
                            func.storage_energy_content(V=row['volume'],
                                                        Tmax=95, Tmin=60),
                            axis=1)
df['U_MWh'] = df['U_kWh'] / 1e3
df['abs_costs'] = df['volume'] * df['specific_costs']

# plot
if False:
    df.plot(x=['U_MWh'], y=['specific_costs'])

# calculate equivalent (annual) investment costs
n = 20
wacc = 0.07
df['ep_costs'] = df['abs_costs'] * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)
#df['specific_ep_costs'] = df['specific_costs'] * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)
# import this into the app as basepoints for the optimization
basepoints = [(0,0)]
basepoints.extend([(np.floor(df['U_MWh'].loc[i]), df['ep_costs'].loc[i])
                  for i in df.index])

if False:
    func.investment_fit(spec_invest=spec_invest, plot=True)
