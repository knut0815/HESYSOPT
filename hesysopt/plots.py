# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd


def pq_plot(df, chps=['extr_turbine_ext'],
            heat_balance='heat_balance',
            electrical_balance='electrical_balance'):
    """
    """
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,6))
    i = 0
    for c in chps:
        df_plot = pd.DataFrame()
        df_plot['P'] = df.loc[electrical_balance, 'input', c].val
        df_plot['Q'] = df.loc[heat_balance, 'input', c].val

        df_plot.plot(ax=axes[i], kind='scatter', x='Q', y='P',
                title='PQ-Diagramm '+c)
        i += 1

def sorted_duration_curve(df, obj_labels=slice(None), balance=slice(None),
                          type=slice(None)):
    """
    """
    idx = pd.IndexSlice
    df = df.loc[idx[balance, type, obj_labels,:]].unstack([0,1,2])
    # set new names for columns
    df.columns.droplevel()

    df.columns = [l for l in obj_labels]

    arr = df.values
    arr.sort(axis=0)
    df = pd.DataFrame(arr, index=df.index, columns=df.columns)

    df.plot(title=balance+type)



